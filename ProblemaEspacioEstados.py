#===============================================
# PARTE I. REPRESENTACIÓN DE ESPACIOS DE ESTADOS
#===============================================

# Recuérdese que según lo que se ha visto en clase, la implementación de la
# representación de un problema de espacio de estados consiste en:

# * Representar estados y acciones mediante una estructura de datos.
# * Definir: estado_inicial, es_estado_final(_), acciones(_), aplica(_,_) y
#   coste_de_aplicar_accion, si el problema tiene coste.

# La siguiente clase Problema representa este esquema general de cualquier
# problema de espacio de estados. Un problema concreto será una subclase de
# Problema, y requerirá implementar acciones, aplica y eventualmente __init__,
# es_estado_final y  coste_de_aplicar_accion.

class Problema(object):
    """Clase abstracta para un problema de espacio de estados. Los problemas
    concretos habría que definirlos como subclases de Problema, implementando
    acciones, aplica y eventualmente __init__, es_estado_final y
    coste_de_aplicar_accion. Una vez hecho esto, se han de crear instancias de
    dicha subclase, que serán la entrada a los distintos algoritmos de
    resolución mediante búsqueda."""

    def __init__(self, estado_inicial, n, estado_final=None ):
        """El constructor de la clase especifica el estado inicial y
        puede que un estado_final, si es que es único. Las subclases podrían
        añadir otros argumentos"""

        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.n = n
        

    def acciones(self, estado):
        """Devuelve las acciones aplicables a un estado dado. Lo normal es
        que aquí se devuelva una lista, pero si hay muchas se podría devolver
        un iterador, ya que sería más eficiente."""
        raise NotImplementedError

    def aplica(self, estado, accion):
        """Devuelve el estado resultante de aplicar accion a estado. Se
        supone que accion es aplicable a estado (es decir, debe ser una de las
        acciones de self.acciones(estado)."""
        raise NotImplementedError

    def es_estado_final(self, estado):
        """Devuelve True cuando estado es final. Por defecto, compara con el
        estado final, si éste se hubiera especificado al constructor. Si se da
        el caso de que no hubiera un único estado final, o se definiera
        mediante otro tipo de comprobación, habría que redefinir este método
        en la subclase."""
        return estado == self.estado_final

    def coste_de_aplicar_accion(self, estado, accion):
        """Devuelve el coste de aplicar accion a estado. Por defecto, este
        coste es 1. Reimplementar si el problema define otro coste"""
        return 1
