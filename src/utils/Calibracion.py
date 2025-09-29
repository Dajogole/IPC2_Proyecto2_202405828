
import os

class Calibracion:
   
    def __init__(self, env_key: str = "IPC2_TIEMPO_OVERHEAD_S"):
        self._env_key = env_key

    def overhead_cierre_segundos(self) -> int:
        valor = os.environ.get(self._env_key, "1")  
        try:
            n = int(valor)
            return n if n >= 0 else 0
        except Exception:
            return 1
