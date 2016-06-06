class Ocho_Puzzle(Problema):
    """Problema a del 8-puzzle.  Los estados serán tuplas de nueve elementos,
    permutaciones de los números del 0 al 8 (el 0 es el hueco). Representan la
    disposición de las fichas en el tablero, leídas por filas de arriba a
    abajo, y dentro de cada fila, de izquierda a derecha. Por ejemplo, el
    estado final será la tupla (1, 2, 3, 8, 0, 4, 7, 6, 5). Las cuatro
    acciones del problema las representaremos mediante las cadenas:
    'Mover hueco arriba', 'Mover hueco abajo', 'Mover hueco izquierda' y
    'Mover hueco derecha', respectivamente."""

    def __init__(self, tablero_inicial):
        super().__init__(estado_inicial=tablero_inicial,
                         estado_final=(1, 2, 3, 8, 0, 4, 7, 6, 5))

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

# >>> p8p_1 = Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# >>> p8p_1.estado_inicial
# (2, 8, 3, 1, 6, 4, 7, 0, 5)
# >>> p8p_1.estado_final
# (1, 2, 3, 8, 0, 4, 7, 6, 5)
# >>> p8p_1.acciones(p8p_1.estado_inicial)
# ['Mover hueco arriba', 'Mover hueco izquierda', 'Mover hueco derecha']
# >>> p8p_1.aplica(p8p_1.estado_inicial,"Mover hueco arriba")
# (2, 8, 3, 1, 0, 4, 7, 6, 5)
# >>> p8p_1.coste_de_aplicar_accion(p8p_1.estado_inicial,"Mover hueco arriba")
# 1
