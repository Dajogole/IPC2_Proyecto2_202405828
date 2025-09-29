from .Scheduler import Scheduler

class Simulador:
    def __init__(self, sistema):
        self.sistema = sistema

    def simular_plan(self, invernadero_nombre: str, plan_nombre: str):
        inv = self.sistema.obtener_invernadero(invernadero_nombre)
        if inv is None:
            raise ValueError("Invernadero no encontrado")
        
        drones = self.sistema.clonar_drones_para_invernadero(inv)
        sch = Scheduler(inv, drones)
        return sch.ejecutar(plan_nombre)
