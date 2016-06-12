from N_Crepes import *
from N_Puzzle import *
from Utilidades import *
import time

"""Metodo llamado desde el metodo busquedaHazBacktracking en el caso que se deba hacer backTracking"""


def aplicaBacktrackingDiscrepancias(memoria, bASeleccionarDict, memoriaLlena):
    global coste
    global bAExplorar
    global discrepancias

    """Si hemos llenado la memoria sin encontar solucion aumentamos las discrepancias"""
    if memoriaLlena:
        # caso base
        if (discrepancias == 0):
            discrepancias += 1
            """Dejamos en la memoria solo con el estado inicial"""
            """ El estado inicial lo ponemos en la memoria por si hay que volver atras para generar sucesores con el backtraking """
            memoria = []
            aux = [estadoInicial]
            memoria.append(aux)
            nivelSiguienteAExplorar = 1
            bAExplorar = memoria[len(memoria) - 1]
            bASeleccionarDict[1] = [0, 1]
            for i in range(nivelSiguienteAExplorar + 1, len(bASeleccionarDict) + 1):
                bASeleccionarDict[i] = [0, 0]


        else:
            diccionarioAux = bASeleccionarDict.copy()
            for nivel, datos in diccionarioAux:
                """buscamos el primer estado con discrepancia"""
                if (datos[1] == 1):
                    """Vemos si la discrepancia esta aplicada es decir si estamos buscando en un bloque que no es el primero"""
                    if (datos[0] != 0):
                        """Limpiamos los datos de la memoria desde el nivel en adelante, es decir solo dejamos lo previo al nivel"""
                        memoria=memoria[0:nivel]
                        auxDatos = datos[:]
                        auxDatos[0] = datos[0] + 1
                        bASeleccionarDict[nivel] = auxDatos

                        discrepanciasPorSetear = discrepancias - 1
                        for i in range(nivel + 1, len(bASeleccionarDict) + 1):
                            if (discrepanciasPorSetear > 0):
                                bASeleccionarDict[i] = [0, 1]
                            else:
                                bASeleccionarDict[i] = [0, 0]
                        break

            memoria.pop()  # borramos de la memoria el ultimo bloque explorado

            """"El bloque B de estados a analizar es en este caso el ultimo almacenado en la memoria tras haber borrado
                el que estabamos visitando, no hay que ordenarlos por heuristica ni nada porque en la memoria ya se introducen ordenados"""
            bAExplorar = memoria[len(memoria) - 1]

            """"Llamamos recursivamente Con el B anterior almacenado pero habra que indicar que de sus sucesores no coja el primer bloque B sino el que le toque debido al backtraking"""
            nivelSiguienteAExplorar = len(memoria)
            bASeleccionarDict[nivelSiguienteAExplorar] = bASeleccionarDict[nivelSiguienteAExplorar] + 1

            """Cada vez que subimos con backtraking un nivel debemos indicar que los niveles de abajo vuelva a buscar a partir del bloque 0"""
            for i in range(nivelSiguienteAExplorar + 1, len(bASeleccionarDict) + 1):
                bASeleccionarDict[i] = [0, 0]

    print("Hacemos backtraking debido a que se han explorado todos los sucesores del nivel: " + str(
        nivelSiguienteAExplorar) + str(bAExplorar))

    """"hay que ver como va lo de resetear el coste x comienzo x discrepancias"""
    coste -= 1


def busquedaHazBacktrackingDiscrepancias(anchuraHaz, tamMemoria, memoria, problema, bASeleccionarDict):
    global bAExplorar
    global coste
    global discrepancias
    # inicialmente empezamos con 0 discrepancias es decir nos iremos guiando por los bloques mejor clasificados por la heuristica
    discrepancias = 0
    """la siguiente variable sera para ir bien cuantas discrepancias de las iniciales hemos usado ya, y saber cuantas nos quedan"""
    discrepanciasUsadas = 0
    tiempoInicio=time.clock()


    while (1):

        """Limpiamos los sucesores de la anterior iteracion"""
        # Todos los estados que van a generarse apartir del bloque actual B que estamos visitando
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

                """Comprobamos si alguno de los nuevos estados generados son final"""
                if (problema.es_estado_final(list(estadoGenerado))):
                    tiempoFinal = time.clock()

                    return "\nSe ha encontrado el estado final: " + str(
                        list(estadoGenerado)) + " con coste del algoritmo: " + str(
                        coste) + "\nEl tiempo de ejecución ha sido: " + str(tiempoFinal - tiempoInicio) + " segundos."

        # No hacemos restriccion di los estados generados no completan la anchura del haz, seguimos con los que haya en el haz

        """Comprobamos si la memoria esta llena"""
        if (len(memoria) == tamMemoria):
            if (tamMemoria <= 1):
                raise Exception(
                    'Si se elige 0 o 1 de tamaño de memoria solo puede almacenarse a lo sumo el estado incial, y no podemos continuar el algoritmo')

            memoriaLlena = 1
            aplicaBacktrackingDiscrepancias(memoria, bASeleccionarDict, memoriaLlena)
            continue

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

            """"Vemos que haya un bloque B con indice que nos toca buscar con el backtraking en los sucesores, si se han acabado hay que subir un nivel como cuando la memoria esta llena"""
            #ESTE CASO NO ESTA MUY CONTEMPLADO QUE DIGAMOS
            if (len(estadosSucesoresEnBloques) <= bASeleccionarDict[len(memoria)][0]):
                if (len(memoria) <= 1):
                    raise Exception(
                        'Mediante el backtraking hemos llegado al estado inicial sin encontrar solucion en ninguno de sus estados sucesores ')
                memoriaLlena = 0
                aplicaBacktrackingDiscrepancias(memoria, bASeleccionarDict, memoriaLlena)
                continue

            else:
                """Si tiene marcada para usar discrepancia en dicho nivel y hay un posible cantidad de bloques generados suficientes """
                if (bASeleccionarDict[len(memoria)][1] and len(estadosSucesoresEnBloques) > bASeleccionarDict[len(memoria)][0] + 1):

                    discrepanciasUsadas += 1
                    bAExplorar = estadosSucesoresEnBloques[bASeleccionarDict[len(memoria)][0] + 1]

                else:
                    """Si tiene marcada discrepancia para el proximo nivel pero no hay ya bloques a los que visitar tras esa discrepancia entonces seleccionamos el primero y recuperamos esa discrepancia"""
                    if (bASeleccionarDict[len(memoria)][1]):
                        """Pregunta para tutoria si no hay tal cantidad de bloques como indica la  discrepancia se guarda para el proximo que lo permita"""

                        aux = bASeleccionarDict[len(memoria)]
                        # marcamos que ya para ese nivel no usamos discrepancia
                        aux[1] = 0
                        bASeleccionarDict[len(memoria)] = aux
                        bAExplorar = estadosSucesoresEnBloques[0]
                        memoria=memoria[0:len(memoria)-1]


                    else:
                        """No tiene discrepancias y hay disponible un B para el indice indicado en el nivel siguiente"""
                        bAExplorar = estadosSucesoresEnBloques[bASeleccionarDict[len(memoria)][0]]

            # si no cumple el tamaño del haz no pasa nada se explora lo que haya dentro

            """El B que usamos es el indicado por el algoritmo siempre sera el primero hasta que haya backtracking y haya que coger otro"""
            memoria.append(bAExplorar)

            """Si es la primera vez que se llega a un nivel nuevo se indica que la b siguiente a buscar es la pimera"""
            if (len(memoria) not in bASeleccionarDict):
                bASeleccionarDict[len(memoria)] = [0, 0]

            if (discrepancias - discrepanciasUsadas > 0):
                """Si quedan discrepancias sin usar la marcamos para usar en el siguiente nivel"""
                aux = bASeleccionarDict[len(memoria)]
                # marcamos que para ese nivel usamos discrepancia
                aux[1] = 1
                bASeleccionarDict[len(memoria)] = aux

            print(bAExplorar)
            coste += 1


""" Metodo para inicializar la busqueda iterativa """


def inicializaBusquedaHazBacktrackingDiscrepancias(anchuraHaz, tamMemoria, tipoProblema, estadoInicial):
    global bAExplorar
    global coste
    """ El estado inicial lo ponemos en la memoria por si hay que volver atras para generar sucesores con el backtraking """
    memoria = []
    aux = [estadoInicial]
    memoria.append(aux)

    """" El coste inicial del algoritmo es 0"""
    coste = 0

    """" Para saber que B debe seleccionar en cada nivel, usaremos un diccionario que tenga como clave el nivel y como valor el b para ese nivel que debe seleccionar,
     el segundo parametro indicara 0-> no usa discrepancias 1-> usa discrepancias para ese nivel """
    bASeleccionarDict = dict()
    # Es decir para el nivel 1 (el que surge de explorar el estado inicial) tenemos que se va explorar incialmente el primer bloque b sin discrepancias
    bASeleccionarDict[1] = [0, 0]

    """" bAExplorar es la B actual que estamos visitando incialmente solo el estado inicial """
    bAExplorar = [estadoInicial]

    """ Elegimos entre los dos tipos de problemas """
    if (tipoProblema == 'N-Crepes'):
        problema = N_Crepes(estadoInicial)

    elif (tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)

    """ Iniciamos el algortimo iterativo de busqueda """
    return busquedaHazBacktrackingDiscrepancias(anchuraHaz, tamMemoria, memoria, problema, bASeleccionarDict)


# Iniciamos el problema declarando los datos
""" Aqui inicializamos el problema que vamos a probar """
anchoDelHaz = 20
tamDeMemoria = 33
tipoProblema = 'N-Puzzle'  # dos tipos: N-Puzzle o N-Crepes
estadoInicial = (8, 7, 6, 5, 4, 3, 2, 1, 0)
discrepancias = 0

print(inicializaBusquedaHazBacktrackingDiscrepancias(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))
