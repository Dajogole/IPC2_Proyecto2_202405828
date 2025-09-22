from core.Scheduler import Scheduler

class Simulador:
    def __init__(self): self._sched = Scheduler()

    def simular_invernadero_plan(self, invernadero, plan):
       
        for dr in invernadero.drones():
            dr.set_pos(0)
            dr._litros=0.0; dr._gramos=0.0
          
            while not dr.objetivos().esta_vacia(): dr.objetivos().desencolar()
            dr._fin_empleado=False
        return self._sched.simular(invernadero, plan)
