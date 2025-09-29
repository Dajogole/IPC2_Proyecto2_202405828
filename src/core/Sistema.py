from ..tda.Mapa import Mapa

class Sistema:
    def __init__(self):
        self.drones_global = Mapa()      
        self.invernaderos = None          

    def reset(self):
        self.drones_global = Mapa()
        self.invernaderos = None

    def obtener_invernadero(self, nombre: str):
        if self.invernaderos is None:
            return None
        for inv in self.invernaderos:
            if inv.nombre == nombre:
                return inv
        return None

    def clonar_drones_para_invernadero(self, inv):

        from ..tda.Mapa import Mapa as _Mapa
        mapa = _Mapa()
        for par in inv.asignaciones:
            dr = par.v
            clon = type(dr)(dr.id, dr.nombre)
            clon.hilera = dr.hilera
            clon.posicion = 0
            clon.terminado = False
            clon.agua_acum = 0.0
            clon.fert_acum = 0.0
            mapa.set(clon.nombre, clon)
        return mapa
