""""Distancia Manhattan de N-Puzzle: se va a calcular la suma de las distancias de la posicion de cada ficha hasta la suya original"""
def calculaDistanciaManhattan(estado, longitudFila):

    distancias=0
    for i in range(len(estado)):
        #fila y columnas donde debe estar el valor i
        filaEnLaActualEnQueSeEncuentra = int(i/longitudFila);#nos quedamos la parte entera

        if(filaEnLaActualEnQueSeEncuentra==0):
            columnaEnLaActualEnQueSeEncuentra = i
        else:
            columnaEnLaActualEnQueSeEncuentra = i % (longitudFila * filaEnLaActualEnQueSeEncuentra)

        #Fila y columna en la que debe estar el valor almacenado en la posicion i actualmente
        filaEnLaActualEnLaQueDebeEstar = int(estado[i] / longitudFila);  # nos quedamos la parte entera

        if (filaEnLaActualEnLaQueDebeEstar==0):
             columnaEnLaActualEnLaQueDebeEstar = estado[i]
        else:
             columnaEnLaActualEnLaQueDebeEstar = estado[i] % (longitudFila * filaEnLaActualEnLaQueDebeEstar)

        distancias+=(abs(filaEnLaActualEnLaQueDebeEstar-filaEnLaActualEnQueSeEncuentra)+abs(columnaEnLaActualEnLaQueDebeEstar-columnaEnLaActualEnQueSeEncuentra))

    return distancias

def heuristicaManhattan(estado1, estado2, longitudFila):
    res = 1
    sumaDistanciasErroneasE1 = calculaDistanciaManhattan(estado1, longitudFila)
    sumaDistanciasErroneasE2 = calculaDistanciaManhattan(estado2, longitudFila)

    if (sumaDistanciasErroneasE1 < sumaDistanciasErroneasE2):
        res = -1
    elif (sumaDistanciasErroneasE1 == sumaDistanciasErroneasE2):
        res = 0
    return res


def obtenerGapEstadoNCrepe(estado):
    gap=0
    for i in range(len(estado)):
        if(estado[i]-estado[i+1]>1):
            gap+=1
    return gap


""""Metodo para obtener los gap Asociados a un estado de N-crepes"""
def heuristicaGap(estado1, estado2):
    res = 1
    gapEstado1 = obtenerGapEstadoNCrepe(estado1)
    gapEstado2 = obtenerGapEstadoNCrepe(estado2)

    if (gapEstado1 < gapEstado2):
        res = -1
    elif (gapEstado1 == gapEstado2):
        res = 0
    return res


"""Comparator versiones 3.X python"""
def comparatorGap(heuristicaGap):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return heuristicaGap(self.obj, other.obj) < 0
        def __gt__(self, other):
            return heuristicaGap(self.obj, other.obj) > 0
        def __eq__(self, other):
            return heuristicaGap(self.obj, other.obj) == 0
        def __le__(self, other):
            return heuristicaGap(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return heuristicaGap(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return heuristicaGap(self.obj, other.obj) != 0
    return K

def comparatorManhattan(heuristicaManhattan, longitudFila):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return heuristicaManhattan(self.obj, other.obj, longitudFila) < 0
        def __gt__(self, other):
            return heuristicaManhattan(self.obj, other.obj), longitudFila > 0
        def __eq__(self, other):
            return heuristicaManhattan(self.obj, other.obj, longitudFila) == 0
        def __le__(self, other):
            return heuristicaManhattan(self.obj, other.obj, longitudFila) <= 0
        def __ge__(self, other):
            return heuristicaManhattan(self.obj, other.obj, longitudFila) >= 0
        def __ne__(self, other):
            return heuristicaManhattan(self.obj, other.obj, longitudFila) != 0
    return K