from tda.Lista import ListaEnlazada

class Estadisticas:
    @staticmethod
    def resumen_por_dron(resultado):
       
        out = ListaEnlazada()
        for s in resultado.por_dron:
            out.append(s)  
        return out
