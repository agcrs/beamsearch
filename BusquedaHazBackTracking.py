from N_Crepes import *
from N_Puzzle import *
from Utilidades import *
import sys

"""Metodo para inicializar la recursividad nos valdra para compartir variables y no tener que meterlas en la ram en cada recursion"""


def inicializaBusquedaHazBacktracking(anchHaz, tamMem, tipoProblema, estadoInicial):
    """"Preparamos los datos para la llamada la algoritmo de busqueda"""
    problema = None
    global estadosSucesores
    global bAExplorar
    global bASeleccionarDict
    global nivelSiguienteAExplorar
    global accionesAplicables
    global estadoGenerado
    global memoriaAplanada
    global estadosSucesoresEnBloques
    global problema

    anchuraHaz = anchHaz
    tamMemoria = tamMem
    memoria = []
    estadosSucesores = []
    costeInicial = 0

    # El estado inicial lo ponemos en la memoria por si hay que volver atras para generar sucesores con el backtraking
    aux = [estadoInicial]
    memoria.append(aux)

    """"Problema realmente es saber que B debe seleccionar en cada momento, yo pienso que lo mejor es un diccionaria que tenga como clave cada nivel y como valor el b para ese nivel que debe seleccionar"""
    bASeleccionarDict = dict()
    bASeleccionarDict[1] = 0  # es decir para el nivel 1 (el que surge de explorar el estado inicial) tenemos que se va explorar incialmente el primer bloque b

    """"bAExplorar es la B actual que estamos visitando incialmente solo el estado inicial"""
    bAExplorar = [estadoInicial]

    # elegimos entre los dos tipos de problemas
    if (tipoProblema == 'N-Crepes'):
        problema = N_Crepes(estadoInicial)

    elif (tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)



    """Metodo llamado desde el metodo busquedaHazBacktracking en el caso que se deba hacer backTracking"""
    def llamadaRecursivaConBacktracking(coste):
        global bAExplorar
        global bASeleccionarDict
        global nivelSiguienteAExplorar

        memoria.pop() #borramos de la memoria el ultimo bloque explorado

        """"El bloque B de estados a analizar es en este caso el ultimo almacenado en la memoria tras haber borrado
            el que estabamos visitando, no hay que ordenarlos por heuristica ni nada porque en la memoria ya se introducen ordenados"""
        bAExplorar = memoria[len(memoria) - 1]

        """"Llamamos recursivamente Con el B anterior almacenado pero habra que indicar que de sus sucesores no coja el primer bloque B sino el que le toque debido al backtraking"""
        nivelSiguienteAExplorar = len(memoria)
        bASeleccionarDict[nivelSiguienteAExplorar] = bASeleccionarDict[nivelSiguienteAExplorar] + 1

        """Cada vez que subimos con backtraking un nivel debemos indicar que los niveles de abajo vuelva a buscar a partir del bloque 0"""
        for i in range(nivelSiguienteAExplorar + 1, len(bASeleccionarDict) + 1):
            bASeleccionarDict[i] = 0

        print("Hacemos backtraking debido a que se han explorado todos los sucesores del nivel: " + str(nivelSiguienteAExplorar) + str(bAExplorar))
        return busquedaHazBacktracking(coste - 1)


    def busquedaHazBacktracking(coste):
        """Todos los estados que van a generarse apartir del bloque actual que estamos visitando"""
        global estadosSucesores
        global bAExplorar
        global bASeleccionarDict
        global nivelSiguienteAExplorar
        global accionesAplicables
        global estadoGenerado
        global memoriaAplanada
        global estadosSucesoresEnBloques
        global problema

        """Limpiamos los sucesores de la anterior iteracion"""
        estadosSucesores = []

        """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
        for estado in bAExplorar:
            accionesAplicables = problema.acciones(estado)
            for accion in accionesAplicables:
                estadoGenerado = problema.aplica(estado, accion)

                """"Preguntar en  tutoria si eso es asi, es decir si el estado esta en memoria no se añade a sucesores"""
                # Aplanamos todos los estados contenidos en cada bloque de la memoria para comprobar si esta contenido el estado observado actual en algun bloque
                memoriaAplanada = sum(memoria, [])
                if (not (estadoGenerado in memoriaAplanada) and not (estadoGenerado in estadosSucesores)):
                    estadosSucesores.append(estadoGenerado)

                """Comprobamos si los nuevos estados generados son estado final"""
                if (problema.es_estado_final(list(estadoGenerado))):
                    return "Se ha encontrado el estado final: " + str(
                        list(estadoGenerado)) + " con coste del algoritmo: " + str(coste)

        # No hacemos restriccion di los estados generados no completan la anchura del haz, seguimos con los que haya en el haz

        """Comprobamos si la memoria ya esta llena"""
        if (len(memoria) == tamMemoria):
            if (tamMemoria <= 1):
                raise Exception(
                    'Si se elige 0 o 1 de tamaño de memoria solo puede almacenarse a lo sumo el estado incial, y no podemos continuar el algoritmo')

            llamadaRecursivaConBacktracking(coste)

        else:
            """"Ordenamos por heuristica"""
            if (type(problema) is N_Crepes):
                estadosSucesores = sorted(estadosSucesores, key=comparatorGap(heuristicaGap))
            else:
                estadosSucesores = sorted(estadosSucesores,
                                          key=comparatorManhattan(heuristicaManhattan, problema.longitudFila))

            """"Dividimos todos los estados sucesores en B bloques en funcion de la anchura del haz"""
            estadosSucesoresEnBloques = [estadosSucesores[i:i + anchuraHaz] for i in
                                         range(0, len(estadosSucesores), anchuraHaz)]

            """"Vemos que haya un bloque B con indice que nos toca buscar con el backtraking en los sucesores si se han acabado hay que subir un nivel como cuando la memoria esta llena"""
            if (len(estadosSucesoresEnBloques) <= bASeleccionarDict[len(memoria)]):
                if (len(memoria) <= 1):
                    raise Exception(
                        'Mediante el backtraking hemos llegado al estado inicial sin encontrar solucion en ninguno de sus estados sucesores ')

                llamadaRecursivaConBacktracking(coste)

            else:
                bAExplorar = estadosSucesoresEnBloques[bASeleccionarDict[len(memoria)]]

            # si no cumple el tamaño del haz no pasa nada se explora lo que haya dentro

            """El B que usamos es el indicado por el algoritmo siempre sera el primero hasta que se llene la memoria y volvamos al de atras y haya que coger otro"""
            memoria.append(bAExplorar)

            """Si es la primera vez que se llega a un nivel nuevo se indica que la b siguiente a buscar es la pimera"""
            if (len(memoria) not in bASeleccionarDict):
                bASeleccionarDict[len(memoria)] = 0

            print(bAExplorar)
            """"Llamamos recursivamente"""
            return busquedaHazBacktracking(coste + 1)




    """Iniciamos el algortimo recursivo de busqueda"""
    return busquedaHazBacktracking(costeInicial)


# Iniciamos el problema declarando los datos
"""Aqui inicializamos el problema que vamos a probar"""
anchoDelHaz = 20
tamDeMemoria = 33
tipoProblema = 'N-Puzzle'  # dos tipos: N-Puzzle o N-Crepes
estadoInicial = (8, 7, 6, 5, 4, 3, 2, 1, 0)

sys.setrecursionlimit(15000)

print(inicializaBusquedaHazBacktracking(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))
