""""Metodo para obtener el numero de fichas colocadas correctamentes en un estadod de N-puzzle"""
def fichasEnOrdenNPuzzle(estado):
    fichasEnOrden=[]
    for i in range(len(estado)):
        if(estado[i]== i):
            fichasEnOrden.append(i)

def heuristicaManhattan(estado1, estado2):
    res = 1
    fichasEnOrdenEstado1 = fichasEnOrdenNPuzzle(estado1)
    fichasEnOrdenEstado2 = fichasEnOrdenNPuzzle(estado2)

    if (fichasEnOrdenEstado1 < fichasEnOrdenEstado2):
        res = -1
    elif (fichasEnOrdenEstado1 == fichasEnOrdenEstado2):
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

