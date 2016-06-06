import math

from pip._vendor.colorama import ansi

from ProblemaEspacioEstados import Problema

def heuristica(elemento1, elemento2):
    """"
    if ........:
        return -1
    elif .....:
        return 1
    else:
        return 0
    """
def busquedaHaz(anchuraHaz,tamMemoria,memoria, problema, bloqueEstadosActual):
    estadosSucesores = []
    for estado in bloqueEstadosActual:
        accionesAplicables = problema.acciones(estado)
        for accion in accionesAplicables:
            estadoGenerado=problema.aplica(estado)
            estadosSucesores.append(estadoGenerado)
            """Comprobamos si los nuevos estados generados son estado final"""
            if(problema.estado_final(estadoGenerado)):
                return

    if (len(estadosSucesores)<anchuraHaz):
        # En este caso debemos lanzar error en la aplicacion
        raise Exception('La generacion de sucesores no ha completado el tamaño del bloque B = ' + anchuraHaz)

    """"Ordenamos por heuristica"""
    estadosSucesores=sorted(estadosSucesores, key=heuristica)

    """Ponemos el primer bloque en memoria"""
    memoria.append(estadosSucesores[0])
    if(len(memoria)>tamMemoria):
        raise Exception('El tamaño de la memoria:+ ' + tamMemoria + ' ha llegado a su limite no caben mas bloques B.')

    """"Llamamos recursivamente"""
    return busquedaHaz(anchuraHaz,tamMemoria,memoria, problema,estadosSucesores)
