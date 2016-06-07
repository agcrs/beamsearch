from N_Crepes import *
from N_Puzzle import *
from Utilidades import *

""""bloqueEstadosActual es la B actual que estamos visitando"""


def busquedaHazBacktracking(anchuraHaz, tamMemoria, memoria, problema, bloqueEstadosActual, coste, bASeleccionarDict):
    """Todos los estados que van a generarse apartir del bloque actual que estamos visitando"""
    estadosSucesores = []

    """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
    for estado in bloqueEstadosActual:
        accionesAplicables = problema.acciones(estado)
        for accion in accionesAplicables:
            estadoGenerado = problema.aplica(estado)
            if not (memoria.contains(estadoGenerado)):
                estadosSucesores.append(estadoGenerado)

            """Comprobamos si los nuevos estados generados son estado final"""
            if (problema.estado_final(estadoGenerado)):
                return coste

    """Pendiente de preguntar en tutoria y pendiente de pensar en backtracking como debe de funcionar"""
    if (len(estadosSucesores) < anchuraHaz):
        # En este caso debemos lanzar error en la aplicacion
        raise Exception('La generacion de sucesores no ha completado el tamaño del bloque B = ' + anchuraHaz)

    """Comprobamos si la memoria ya esta llena"""
    if (len(memoria) == tamMemoria):
        """En caso de tener la memoria ya llena sacamos el ultimo elemento introducido"""
        memoria.pop()

        """"El bloque B de estados a analizar es en este caso el ultimo almacenado en la memoria tras haber borrado
        el que estabamos visitando, no hay que ordenarlos por heuristica ni nada porque en la memoria ya se introducen ordenados"""
        bSiguienteAExplorar=memoria[len(memoria)-1]

        """"Llamamos recursivamente Con el B anterior almacenado pero habra que indicar que de sus sucesores no coja el primer bloque B sino el que le toque debido al backtraking"""
        nivelSiguienteQueSeVaAExplorar=len(memoria)+1 #el mas 1 es porque en memoria se guardan los niveles desde el 1 el estado inicial no se guarda
        bASeleccionarDict[nivelSiguienteQueSeVaAExplorar]= bASeleccionarDict[nivelSiguienteQueSeVaAExplorar]+1
        return busquedaHazBacktracking(anchuraHaz, tamMemoria, memoria, problema, bSiguienteAExplorar, coste-1, bASeleccionarDict)

    else:
        """"Ordenamos por heuristica"""
        if (type(problema) is N_Crepes):
            estadosSucesores = sorted(estadosSucesores, key=heuristicaGap)
        else:
            estadosSucesores = sorted(estadosSucesores, key=heuristicaManhattan)

        """"Dividimos todos los estados sucesores en B bloques en funcion de la anchura del haz"""

        estadosSucesoresEnBloques=[estadosSucesores[i:i+anchuraHaz] for i in range(0, len(estadosSucesores), anchuraHaz)]

        """"Vemos que haya un bloque B con indice que nos toca buscar con el backtrakign en los sucesores se se han acabado hay que subir un nivel creo"""
        if(len(estadosSucesoresEnBloques)<=bASeleccionarDict[len(memoria)+1]):
            """En ESTE CASO REPETIMOS LO MISMO QUE CUANDO LA MEMORIA ESTABA LLENA"""
            memoria.pop()
            bSiguienteAExplorar = memoria[len(memoria) - 1]
            nivelSiguienteQueSeVaAExplorar = len(memoria) + 1  # el mas 1 es porque en memoria se guardan los niveles desde el 1 el estado inicial no se guarda
            bASeleccionarDict[nivelSiguienteQueSeVaAExplorar] = bASeleccionarDict[nivelSiguienteQueSeVaAExplorar] + 1
            return busquedaHazBacktracking(anchuraHaz, tamMemoria, memoria, problema, bSiguienteAExplorar, coste - 1, bASeleccionarDict)

        else:
            bSiguienteAExplorar=estadosSucesoresEnBloques[bASeleccionarDict[len(memoria)+1]]

        """"No se que habria que hacer si no cumple el tamaño del haz supongo que volver a tras y porbar uno anterior, preguntar tutoria"""
        if (len(bSiguienteAExplorar) < anchuraHaz):
            # En este caso debemos lanzar error en la aplicacion
            raise Exception('La generacion de sucesores no ha completado el tamaño del bloque B = ' + anchuraHaz)


        """El B que usamos es el indicado por el algoritmo siempre sera el primero hasta que se llene la memoria y volvamos al de atras y haya que coger el siguiente"""
        memoria.append(bSiguienteAExplorar)

        """Si es la primera vez que se llega a un nivel nuevo se indica que la b siguiente a buscar es la pimera"""
        if (len(memoria) == len(bASeleccionarDict)):
            bASeleccionarDict[len(memoria)]=0;



        """"Llamamos recursivamente"""
        return busquedaHazBacktracking(anchuraHaz, tamMemoria, memoria, problema, bSiguienteAExplorar, coste + 1, bASeleccionarDict)


def inicializaBusquedaHazBacktracking(anchuraHaz, tamMemoria, tipoProblema, estadoInicial):
    if (tipoProblema == 'N-Crepes'):
        problema = N_Crepes(estadoInicial)

    elif (tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)

    """"El primer bloque a explorar solo lleva el estado incial"""
    Binicial = []
    Binicial.append(estadoInicial)

    """"Problema realmente es saber que B debe seleccionar en cada momento, yo pienso que lo mejor es un mapa que tenga como clave cada nivel y como valor el b para ese nivel que debe seleccionar"""
    mapaBASeleccionarPorNivel = dict()
    mapaBASeleccionarPorNivel[0] = 0
    mapaBASeleccionarPorNivel[1] = 0


    return busquedaHazBacktracking(anchuraHaz, tamMemoria, [], problema, Binicial, 0, 0,mapaBASeleccionarPorNivel)

    # print(inicializaBusquedaHaz(anchuraHaz, tamMemoria, tipoProblema, estadoInicial))
