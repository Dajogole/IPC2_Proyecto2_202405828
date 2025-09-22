from tda.Lista import ListaEnlazada
from domain.PlanRiego import PlanPaso

class AccionDron:
    def __init__(self, dron_nombre:str, accion:str):
        self.dron = dron_nombre
        self.accion = accion

class Segundo:
    def __init__(self, t:int):
        self.t = t
        self.acciones = ListaEnlazada()  

class ResultadoSim:
    def __init__(self, tiempo:int, timeline:ListaEnlazada, totL:float, totG:float, porDron:ListaEnlazada):
        self.tiempo = tiempo
        self.timeline = timeline
        self.total_litros = totL
        self.total_gramos = totG
        self.por_dron = porDron  

class Scheduler:
    def __init__(self):
        pass

    def _drone_por_hilera(self, inv, hilera_num):
        for d in inv.drones():
            if d.hilera()==hilera_num:
                return d
        return None

    def _plant_info(self, inv, hil, pos):
        h = inv.hilera(hil)
        pl = h.planta_en(pos) if h else None
        if pl: return pl.litros(), pl.gramos()
        return 0.0,0.0

    def simular(self, invernadero, plan):
       
        for paso in plan.pasos():
            d = self._drone_por_hilera(invernadero, paso.hilera)
            if d: d.objetivos().encolar(paso.posicion)

        timeline = ListaEnlazada()
        porDron = ListaEnlazada()
        t = 0
        ultimo_riego_t = 0

      
        nodo_paso = plan.pasos()._cabeza


        def actualizar_por_dron(nombre, l, g):
           
            i=0
            encontrado = False
            for s in porDron:
               
                p1 = s.split("|")
                if p1[0]==nombre:
                    l0 = float(p1[1]); g0 = float(p1[2])
                    nuevo = f"{nombre}|{l0+l}|{g0+g}"
                    porDron.remove_at(i)
                    porDron.prepend(nuevo)
                    encontrado = True
                    break
                i+=1
            if not encontrado:
                porDron.append(f"{nombre}|{l}|{g}")

        def todos_fin():
            for d in invernadero.drones():
                if not d.fin_empleado(): return False
            return True

        while nodo_paso is not None or not todos_fin():
            t += 1
            seg = Segundo(t)
           
            rego_este_segundo = False
            if nodo_paso is not None:
                paso:PlanPaso = nodo_paso.valor
                dr = self._drone_por_hilera(invernadero, paso.hilera)
                if dr is not None:
               
                    objetivo = dr.objetivos().frente()
                    if objetivo == paso.posicion and dr.pos()==objetivo:
                        
                        seg.acciones.append(AccionDron(dr.nombre(),"Regar"))
                        l,g = self._plant_info(invernadero, paso.hilera, paso.posicion)
                        dr.sumar(l,g)
                        actualizar_por_dron(dr.nombre(), l, g)
                        dr.objetivos().desencolar()
                        nodo_paso = nodo_paso.siguiente
                        rego_este_segundo = True
                        ultimo_riego_t = t
           
            for dr in invernadero.drones():
               
                ya = False
                for a in seg.acciones:
                    if a.dron == dr.nombre() and a.accion=="Regar":
                        ya = True
                        break
                if ya: continue

                if dr.objetivos().esta_vacia():
                    if not dr.fin_empleado():
                        seg.acciones.append(AccionDron(dr.nombre(),"FIN"))
                        dr.marcar_fin()
                    else:
                       
                        pass
                else:
                    objetivo = dr.objetivos().frente()
                    if dr.pos() < objetivo:
                        dr.set_pos(dr.pos()+1)
                        seg.acciones.append(AccionDron(dr.nombre(), f"Adelante (H{dr.hilera()}P{dr.pos()})"))
                    elif dr.pos() > objetivo:
                        dr.set_pos(dr.pos()-1)
                        seg.acciones.append(AccionDron(dr.nombre(), f"Atrás (H{dr.hilera()}P{dr.pos()})"))
                    else:
                    
                        seg.acciones.append(AccionDron(dr.nombre(),"Esperar"))
            timeline.append(seg)

            
            if nodo_paso is None:
                done = True
                for d in invernadero.drones():
                    if not d.fin_empleado(): done = False
                if done: break

      
        totalL=0.0; totalG=0.0
        for d in invernadero.drones():
            totalL += d.litros(); totalG += d.gramos()

        return ResultadoSim(ultimo_riego_t, timeline, totalL, totalG, porDron)
