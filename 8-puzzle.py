class Problema(object):
    """Clase abstracta para un problema de espacio de estados. Los problemas
    concretos habría que definirlos como subclases de Problema, implementando
    acciones, aplica y eventualmente __init__, es_estado_final y
    coste_de_aplicar_accion. Una vez hecho esto, se han de crear instancias de
    dicha subclase, que serán la entrada a los distintos algoritmos de
    resolución mediante búsqueda."""

    def __init__(self, estado_inicial, n,  estado_final=None):
        """El constructor de la clase especifica el estado inicial y
        puede que un estado_final, si es que es único. Las subclases podrían
        añadir otros argumentos"""

        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

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
    
class Ocho_Puzzle(Problema):
    """Problema a del 8-puzzle.  Los estados serán tuplas de nueve elementos,
    permutaciones de los números del 0 al 8 (el 0 es el hueco). Representan la
    disposición de las fichas en el tablero, leídas por filas de arriba a
    abajo, y dentro de cada fila, de izquierda a derecha. Por ejemplo, el
    estado final será la tupla (1, 2, 3, 8, 0, 4, 7, 6, 5). Las cuatro
    acciones del problema las representaremos mediante las cadenas:
    'Mover hueco arriba', 'Mover hueco abajo', 'Mover hueco izquierda' y
    'Mover hueco derecha', respectivamente."""

    def __init__(self, tablero_inicial, n):
        super().__init__(estado_inicial=tablero_inicial, n=self.n,
                         estado_final=list(range(8)))

    def acciones(self, estado):
        pos_hueco = estado.index(0)
        acciones_aplicables = []
        if pos_hueco not in [0, 1, 2]:
            acciones_aplicables.append('Mover hueco arriba')
        if pos_hueco not in [6, 7, 8]:
            acciones_aplicables.append('Mover hueco abajo')
        if pos_hueco not in [0, 3, 6]:
            acciones_aplicables.append('Mover hueco izquierda')
        if pos_hueco not in [2, 5, 8]:
            acciones_aplicables.append('Mover hueco derecha')
        return acciones_aplicables

    def aplica(self, estado, accion):
        pos_hueco = estado.index(0)
        if accion == 'Mover hueco arriba':
            nueva_pos = pos_hueco - 3
        elif accion == 'Mover hueco abajo':
            nueva_pos = pos_hueco + 3
        elif accion == 'Mover hueco izquierda':
            nueva_pos = pos_hueco - 1
        else:  # Mover hueco derecha
            nueva_pos = pos_hueco + 1
        ficha = estado[nueva_pos]
        estado_como_lista = list(estado)
        estado_como_lista[pos_hueco], estado_como_lista[nueva_pos] = ficha, 0
        return tuple(estado_como_lista)

# Ejemplos que se pueden ejecutar una vez se ha definido la clase:

p8p_1 = Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5),8)
p8p_1.estado_inicial
# (2, 8, 3, 1, 6, 4, 7, 0, 5)
# >>> p8p_1.estado_final
# (1, 2, 3, 8, 0, 4, 7, 6, 5)
# >>> p8p_1.acciones(p8p_1.estado_inicial)
# ['Mover hueco arriba', 'Mover hueco izquierda', 'Mover hueco derecha']
# >>> p8p_1.aplica(p8p_1.estado_inicial,"Mover hueco arriba")
# (2, 8, 3, 1, 0, 4, 7, 6, 5)
# >>> p8p_1.coste_de_aplicar_accion(p8p_1.estado_inicial,"Mover hueco arriba")
# 1