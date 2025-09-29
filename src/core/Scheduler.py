from ..tda.ListaSimple import ListaSimple
from ..tda.Mapa import Mapa, Par
from ..domain import InstruccionDron, InstruccionesTiempo, PasoPlan, ParNumeros, ResultadoPlan
from ..utils.Calibracion import Calibracion


class Scheduler:
   
    def __init__(self, invernadero, drones_mapa):
        self.inv = invernadero
        self.drones = drones_mapa                    
        self._agua_total = 0.0
        self._fert_total = 0.0
        self._por_dron = Mapa()                     
        self._timeline = ListaSimple()                


    def _fmt_mov(self, accion: str, hilera: int, pos_actual: int) -> str:
        """Devuelve 'Adelante(H#P#)' o 'Atras(H#P#)' usando la POSICIÓN ALCANZADA en ese segundo."""
        return f"{accion}(H{hilera}P{pos_actual})"

    def _buscar_plan(self, plan_nombre: str):
        if self.inv is None or self.inv.planes is None:
            return None
        for p in self.inv.planes:
            if p.nombre == plan_nombre:
                return p
        return None

    def _dron_por_hilera(self, hilera_num: int):
        asign = self.inv.asignaciones.get(hilera_num)
        if asign is None:
            return None
        dron = self.drones.get(asign.nombre)
        if dron is not None:
            return dron
        return self.drones.get(getattr(asign, "id", None))

    def _planta(self, h: int, p: int):
        hil = self.inv.hileras.get(h)
        if hil is None:
            return None
        if hasattr(hil, "plantas"):
            return hil.plantas.get(p)
        return None

    def _len_lista(self, lista):
        try:
            return len(lista)
        except TypeError:
            c = 0
            for _ in lista:
                c += 1
            return c

    def _validar_plan(self, plan):
        n = self._len_lista(plan.pasos)
        if n == 0:
            raise ValueError("El plan no contiene pasos.")
        i = 0
        for paso in plan.pasos:
            if paso.hilera < 1 or paso.hilera > self.inv.numero_hileras:
                raise ValueError(f"Paso #{i+1}: hilera {paso.hilera} fuera de 1..{self.inv.numero_hileras}.")
            if paso.posicion < 1 or paso.posicion > self.inv.plantas_x_hilera:
                raise ValueError(f"Paso #{i+1}: posición {paso.posicion} fuera de 1..{self.inv.plantas_x_hilera}.")
            if self._dron_por_hilera(paso.hilera) is None:
                raise ValueError(f"Paso #{i+1}: la hilera {paso.hilera} no tiene dron asignado.")
            if self._planta(paso.hilera, paso.posicion) is None:
                raise ValueError(f"Paso #{i+1}: no existe la planta H{paso.hilera}-P{paso.posicion}.")
            i += 1

    def _init_por_dron(self):
        for par in self.drones:
            self._por_dron.set(par.k, ParNumeros(0.0, 0.0))

    def _siguiente_objetivo_para_hilera(self, plan, idx_actual, hilera):

        i = idx_actual
        while True:
            try:
                paso = plan.pasos.obtener(i)
            except Exception:
                j = 0
                paso = None
                for pp in plan.pasos:
                    if j == i:
                        paso = pp
                        break
                    j += 1
            if paso is None:
                return None
            if paso.hilera == hilera:
                return paso.posicion
            i += 1


    def ejecutar(self, plan_nombre: str):
        plan = self._buscar_plan(plan_nombre)
        if plan is None:
            raise ValueError("Plan no encontrado en el invernadero seleccionado.")

        self._validar_plan(plan)
        self._init_por_dron()

        total_pasos = self._len_lista(plan.pasos)
        watchdog_max = total_pasos * (self.inv.plantas_x_hilera + 2) + 100

        idx = 0
        tiempo = 0

        while idx < total_pasos:
            tiempo += 1
            if tiempo > watchdog_max:
                raise RuntimeError("La simulación excedió el límite de seguridad. "
                                   "Revise asignaciones y pasos del plan (posiciones alcanzables).")

            acciones_seg = ListaSimple()


            try:
                paso = plan.pasos.obtener(idx)
            except Exception:
                j = 0
                paso = None
                for pp in plan.pasos:
                    if j == idx:
                        paso = pp
                        break
                    j += 1
            if paso is None:
                break

            hilera_obj = paso.hilera
            pos_obj    = paso.posicion


            dron_riego = self._dron_por_hilera(hilera_obj)
            if dron_riego is None:
                raise RuntimeError(f"No hay dron asignado para la hilera {hilera_obj}.")

            if dron_riego.posicion < pos_obj:
                dron_riego.posicion += 1
                acciones_seg.append(InstruccionDron(
                    dron_riego.nombre, self._fmt_mov("Adelante", hilera_obj, dron_riego.posicion)))
            elif dron_riego.posicion > pos_obj:
                dron_riego.posicion -= 1
                acciones_seg.append(InstruccionDron(
                    dron_riego.nombre, self._fmt_mov("Atras", hilera_obj, dron_riego.posicion)))
            else:
                acciones_seg.append(InstruccionDron(dron_riego.nombre, "Regar"))
                self._aplicar_riego(dron_riego, paso)
                idx += 1 


            for par in self.drones:
                dr = par.v
                if dr is dron_riego:
                    continue
                if getattr(dr, "terminado", False):
                    acciones_seg.append(InstruccionDron(dr.nombre, "Fin"))
                    continue

                objetivo = self._siguiente_objetivo_para_hilera(plan, idx, dr.hilera)
                if objetivo is None:
                    dr.terminado = True
                    acciones_seg.append(InstruccionDron(dr.nombre, "Fin"))
                    continue

                if dr.posicion < objetivo:
                    dr.posicion += 1
                    acciones_seg.append(InstruccionDron(
                        dr.nombre, self._fmt_mov("Adelante", dr.hilera, dr.posicion)))
                elif dr.posicion > objetivo:
                    dr.posicion -= 1
                    acciones_seg.append(InstruccionDron(
                        dr.nombre, self._fmt_mov("Atras", dr.hilera, dr.posicion)))
                else:
                    acciones_seg.append(InstruccionDron(dr.nombre, "Esperar"))


            self._timeline.append(InstruccionesTiempo(tiempo, acciones_seg))


        cal = Calibracion()
        over = cal.overhead_cierre_segundos()
        if over > 0:

            for par in self.drones:
                setattr(par.v, "terminado", True)

            for _ in range(over):
                acciones_seg = ListaSimple()
                for par in self.drones:
                    dr = par.v
                    acciones_seg.append(InstruccionDron(dr.nombre, "Fin"))
                tiempo += 1
                self._timeline.append(InstruccionesTiempo(tiempo, acciones_seg))


        return ResultadoPlan(
            tiempo_optimo=tiempo,      
            agua_total=self._agua_total,
            fert_total=self._fert_total,
            por_dron_mapa=self._por_dron,
            timeline_lista=self._timeline
        )

    def _aplicar_riego(self, dron, paso):
        planta = self._planta(paso.hilera, paso.posicion)
        if planta is None:
            return
        dron.agua_acum = getattr(dron, "agua_acum", 0.0) + planta.litros
        dron.fert_acum = getattr(dron, "fert_acum", 0.0) + planta.gramos
        self._agua_total += planta.litros
        self._fert_total += planta.gramos

        par = self._por_dron.get(dron.nombre)
        if par is None:
            self._por_dron.set(dron.nombre, ParNumeros(planta.litros, planta.gramos))
        else:
            par.a += planta.litros
            par.b += planta.gramos
