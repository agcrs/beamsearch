from N_Crepes import *
from N_Puzzle import *

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



""""bloqueEstadosActual es la B actual que estamos visitando"""
def busquedaHaz(anchuraHaz,tamMemoria,memoria, problema, bloqueEstadosActual, coste):
    """Todos los estados que van a generarse apartir del bloque actual que estamos visitando"""
    estadosSucesores = []

    """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
    for estado in bloqueEstadosActual:
        accionesAplicables = problema.acciones(estado)
        for accion in accionesAplicables:
            estadoGenerado=problema.aplica(estado)
            if not(memoria.contains(estadoGenerado)):
                estadosSucesores.append(estadoGenerado)

            """Comprobamos si los nuevos estados generados son estado final"""
            if(problema.estado_final(estadoGenerado)):
                return coste

    """Pendiente de preguntar en tutoria"""
    if (len(estadosSucesores)<anchuraHaz):
        # En este caso debemos lanzar error en la aplicacion
        raise Exception('La generacion de sucesores no ha completado el tamaño del bloque B = ' + anchuraHaz)

    """"Ordenamos por heuristica"""
    if(type(problema) is N_Crepes):
        estadosSucesores=sorted(estadosSucesores, key=heuristicaGap)
    else:
        estadosSucesores=sorted(estadosSucesores, key=heuristicaManhattan)


    """Ponemos el primer bloque en memoria"""
    memoria.append(estadosSucesores[0])
    if(len(memoria)>tamMemoria):
        raise Exception('El tamaño de la memoria:+ ' + tamMemoria + ' ha llegado a su limite no caben mas bloques B.')

    """"Llamamos recursivamente"""
    return busquedaHaz(anchuraHaz,tamMemoria,memoria, problema, estadosSucesores, coste+1)




def inicializaBusquedaHaz(anchuraHaz, tamMemoria, tipoProblema, estadoInicial):
    if (tipoProblema == 'N-Crepes'):
        problema =  N_Crepes(estadoInicial)

    elif(tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)

    """"El primer bloque a explorar solo lleva el estado incial"""
    Binicial=[]
    Binicial.append(estadoInicial)
    return busquedaHaz(anchuraHaz, tamMemoria, None, problema, Binicial, 0)