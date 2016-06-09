import math
from ProblemaEspacioEstados import Problema


class N_Puzzle(Problema):
    """Problema a del N-puzzle.  Los estados serán tuplas de n+1 elementos,
    permutaciones de los números del 0 al n (el 0 es el hueco). Representan la
    disposición de las fichas en el tablero, leídas por filas de arriba a
    abajo, y dentro de cada fila, de izquierda a derecha. Por ejemplo, el
    estado final será la tupla (1,2). Las cuatro
    acciones del problema las representaremos mediante las cadenas:
    'Mover hueco arriba', 'Mover hueco abajo', 'Mover hueco izquierda' y
    'Mover hueco derecha', respectivamente."""
    
 
    
    def __init__(self, tablero_inicial):
        tam=len(tablero_inicial)
        super().__init__(estado_inicial=tablero_inicial, n=tam, estado_final=list(range(tam)))
        self.longitudFila=int(math.sqrt(self.n))
        

    def acciones(self, estado):
       
        pos_hueco = estado.index(0)
        acciones_aplicables = []
        posPrimeraFila=range(0, self.longitudFila)
        posUltimaFila=range(self.n-self.longitudFila, self.n)
        posPimeraColumna=range(0, self.n, self.longitudFila)
        posUltimaColumna=range(self.longitudFila-1, self.n, self.longitudFila)


        
        if pos_hueco not in posPrimeraFila:
            acciones_aplicables.append('Mover hueco arriba')
        if pos_hueco not in posUltimaFila:
            acciones_aplicables.append('Mover hueco abajo')
        if pos_hueco not in  posPimeraColumna:
            acciones_aplicables.append('Mover hueco izquierda')
        if pos_hueco not in  posUltimaColumna:
            acciones_aplicables.append('Mover hueco derecha')
        return acciones_aplicables

    def aplica(self, estado, accion):
        pos_hueco = estado.index(0)
        if accion == 'Mover hueco arriba':
            nueva_pos = pos_hueco - self.longitudFila
        elif accion == 'Mover hueco abajo':
            nueva_pos = pos_hueco + self.longitudFila
        elif accion == 'Mover hueco izquierda':
            nueva_pos = pos_hueco - 1
        else:  # Mover hueco derecha
            nueva_pos = pos_hueco + 1
        '''Ficha que se encontraba donde ahora hemos movido el hueco'''
        ficha = estado[nueva_pos]
        estado_como_lista = list(estado)
        '''Actualizamos el estado, ponemos el hueco en su nuevo sitio y la ficha donde estaba el hueco'''
        estado_como_lista[pos_hueco], estado_como_lista[nueva_pos] = ficha, 0
        return tuple(estado_como_lista)

""""
#Ejemplos que se pueden ejecutar una vez se ha definido la clase:
p8p_1 = N_Puzzle((0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15))
print(p8p_1.estado_inicial)
# (2, 8, 3, 1, 6, 4, 7, 0, 5)
print(p8p_1.estado_final)
# (1, 2, 3, 8, 0, 4, 7, 6, 5)
print(p8p_1.acciones(p8p_1.estado_inicial))
# ['Mover hueco arriba', 'Mover hueco izquierda', 'Mover hueco derecha']
print(p8p_1.aplica(p8p_1.estado_inicial,"Mover hueco arriba"))
# (2, 8, 3, 1, 0, 4, 7, 6, 5)
print(p8p_1.coste_de_aplicar_accion(p8p_1.estado_inicial,"Mover hueco arriba"))
# 1
"""""