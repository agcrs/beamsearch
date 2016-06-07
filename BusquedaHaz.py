from N_Crepes import *
from N_Puzzle import *
from Utilidades import *


""""bloqueEstadosActual es la B actual que estamos visitando"""
def busquedaHaz(anchuraHaz,tamMemoria,memoria, problema, bloqueEstadosActual, coste):
    """Todos los estados que van a generarse apartir del bloque actual que estamos visitando"""
    estadosSucesores = []

    """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
    for estado in bloqueEstadosActual:
        accionesAplicables = problema.acciones(estado)
        for accion in accionesAplicables:
            estadoGenerado=problema.aplica(estado)
            """"Preguntar en  tutoria si eso es asi, es decir si el estado esta en memoria no se añade a sucesores"""
            if not(memoria.contains(estadoGenerado)):
                estadosSucesores.append(estadoGenerado)

            """Comprobamos si los nuevos estados generados son estado final"""
            if(problema.estado_final(estadoGenerado)):
                return coste

    """"Ordenamos por heuristica"""
    if(type(problema) is N_Crepes):
        estadosSucesores=sorted(estadosSucesores, key=heuristicaGap)
    else:
        estadosSucesores=sorted(estadosSucesores, key=heuristicaManhattan)


    """"Dividimos todos los estados sucesores en B bloques en funcion de la anchura del haz"""
    estadosSucesoresEnBloques = [estadosSucesores[i:i + anchuraHaz] for i in range(0, len(estadosSucesores), anchuraHaz)]

    """"Cogemos el primer bloque ya que en este algoritmo sin backtracking siempre se explorará el primero"""
    bSiguienteAExplorar = estadosSucesoresEnBloques[0]

    """Pendiente de preguntar en tutoria"""
    if (len(bSiguienteAExplorar) < anchuraHaz):
        # En este caso debemos lanzar error en la aplicacion
        raise Exception('La generacion de sucesores no ha completado el tamaño del bloque B = ' + anchuraHaz)

    """Lo ponemos en memoria en memoria"""
    memoria.append(bSiguienteAExplorar)

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
    return busquedaHaz(anchuraHaz, tamMemoria, [], problema, Binicial, 0)

#print(inicializaBusquedaHaz(anchuraHaz, tamMemoria, tipoProblema, estadoInicial))