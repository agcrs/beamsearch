import time

from N_Crepes import *
from N_Puzzle import *
from Utilidades import *

"""Metodo llamado desde el metodo busquedaHazBacktracking en el caso que se deba hacer backTracking"""


def aplicaBacktrackingDiscrepancias(memoria, bASeleccionarDict, memoriaLlena):
    global bAExplorar
    global discrepancias

    """Si hemos llenado la memoria sin encontar solucion aumentamos las discrepancias"""
    if memoriaLlena:
        # caso base
        if (discrepancias == 0):
            discrepancias += 1
            bAExplorar = [estadoInicial]
            """Dejamos en la memoria solo con el estado inicial"""
            """ El estado inicial lo ponemos en la memoria por si hay que volver atras para generar sucesores con el backtraking """
            memoria = []
            memoria.append(bAExplorar)
            bASeleccionarDict[1] = [0, 1 , 0]
            """esto se peude ahorrar para discrepencias cero siempre seran 0,0
            for i in range(nivelSiguienteAExplorar + 1, len(bASeleccionarDict) + 1):
                bASeleccionarDict[i] = [0, 0]
        """

        else:
            """Quitamos el ultimo bloque de estados que lleno la memoria"""
            memoria.pop()

            algunoConDiscrepanciaActiva=0
            """Ahora recorrermos los nodos que ahi en la memoria desde abajo arriba buscamos el ultimo con discrepancia y este lo movemos hasta que llegue al final"""
            for i in range(len(memoria),0, -1):
                datosNivel = bASeleccionarDict[i]

                # FIXME: creo que no hace falta puesto que cuando llega al tope uno abajo en el algoritmo de busqueda se setea  datosNivel[1] = 0 de modo que abajo entrara solo en la que pueda avanzar
                """si lo primero que encontramos por abajo es un nodo que tiene ya usada su discrepancia sin encontrar estado final para la capacidad de memoria,
                 debemos subir hasta que encontremos el ultimo que aun puede moverse
                if (datosNivel[0] == 0 and datosNivel[2] == 1):
                    """

                if (datosNivel[1] == 1):
                    algunoConDiscrepanciaActiva = 1
                    """Vemos si la discrepancia esta aplicada es decir si estamos buscando en un bloque que no es el primero"""
                    """Limpiamos los datos de la memoria desde el nivel en adelante, es decir solo dejamos lo previo al nivel"""
                    # Lo hacemos hasta i porque empiezan en 0 los niveles guardado en memoria en cambio en el diccionario empiezan desde el 1 es decir siempre la len de la memoria indica el proximo a selccionar del diccionario
                    memoria = memoria[0:i]
                    datosNivel[0] = datosNivel[0] + 1
                    bASeleccionarDict[len(memoria)] = datosNivel
                    actualizaInforNivelesSucesores(len(memoria)+1, bASeleccionarDict)
                    break

            if not algunoConDiscrepanciaActiva:
                # FIXME: Creo que esto es el final del algoritmo

                #  FIXME: Pienso que si hay discrepancias para cada nivel de memoria y encima ya se han usado, ha terminado el algoritmo
                if (len(memoria)<=discrepancias):
                    return "-1"
                else:
                    discrepancias += 1
                    bAExplorar = [estadoInicial]
                    """Dejamos en la memoria solo con el estado inicial"""
                    """ El estado inicial lo ponemos en la memoria por si hay que volver atras para generar sucesores con el backtraking """
                    memoria = []
                    memoria.append(bAExplorar)
                    for i in range(1 , discrepancias+1):
                        bASeleccionarDict[i] = [0, 1, 0]
                    print(str(bAExplorar) + " con discrepancis:" + str(discrepancias))

            bAExplorar = memoria[len(memoria) - 1]



    return memoria


"""Metodo llamado cada vez que nos movamos en un nivel de arriba para indicar la nueva infromacion de los siguientes sucesores"""
def actualizaInforNivelesSucesores(nivelSiguienteAExplorar, bASeleccionarDict):
    global discrepancias
    """buscamos las discrepancias usadas por arriba de este nivel obsrvado para asi saber cuantas quedan por asociar"""
    discrepanciasLibres = discrepancias
    for nivel in range(1, nivelSiguienteAExplorar):
        datosNivel = bASeleccionarDict[nivel]
        if (datosNivel[1] == 1):
            discrepanciasLibres -= 1

    for nivel in range(nivelSiguienteAExplorar, len(bASeleccionarDict) + 1):
        datosNivel = bASeleccionarDict[nivel]
        """Ponemos que todos los estados a partir de este empiezan a buscar desde el nodo 0 , con sus discrepancias correspondientes a parte"""
        datosNivel[0] = 0
        """indicamos que para ninguno de los sucesores se ha usado discrepancia"""
        datosNivel[2] = 0

        if (discrepanciasLibres > 0):
            # marcamos que ya para ese nivel no usamos discrepancia
            datosNivel[1] = 1
            discrepanciasLibres -= 1

        """Actualizamos la informacion del nivel"""
        bASeleccionarDict[nivel] = datosNivel

    """Si no hemos conseguido repartir todas las discrepancias que nos quedan entre los sucesores del diccionario las tendremos que repartir creando nuevos posibles niveles"""
    if (discrepanciasLibres > 0):
        for i in range(len(bASeleccionarDict) + 1, discrepanciasLibres + 1):
            bASeleccionarDict[i] = [0, 1, 0]



def busquedaHazBacktrackingDiscrepancias(anchuraHaz, tamMemoria, memoria, problema, bASeleccionarDict):
    global bAExplorar
    global discrepancias
    # inicialmente empezamos con 0 discrepancias es decir nos iremos guiando por los bloques mejor clasificados por la heuristica
    discrepancias = 0
    """la siguiente variable sera para ir bien cuantas discrepancias de las iniciales hemos usado ya, y saber cuantas nos quedan"""
    # discrepanciasUsadas = 0
    tiempoInicio=time.clock()

    while (1):

        """Limpiamos los sucesores de la anterior iteracion"""
        # Todos los estados que van a generarse apartir del bloque actual B que estamos visitando
        estadosSucesores = []

        nivelSiguienteAExplorar = len(memoria) + 1

        # Aplanamos todos los estados contenidos en cada bloque de la memoria para comprobar si esta contenido el estado observado actual en algun bloque
        memoriaAplanada = sum(memoria, [])

        """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
        for estado in bAExplorar:
            accionesAplicables = problema.acciones(estado)
            for accion in accionesAplicables:
                estadoGenerado = problema.aplica(estado, accion)

                """"Preguntar en  tutoria si eso es asi, es decir si el estado esta en memoria no se añade a sucesores"""
                if (not (estadoGenerado in memoriaAplanada) and not (estadoGenerado in estadosSucesores)):
                    estadosSucesores.append(estadoGenerado)

                """Comprobamos si alguno de los nuevos estados generados son final"""
                if (problema.es_estado_final(list(estadoGenerado))):
                    tiempoFinal = time.clock()

                    #El coste finalmente es la profundidad, por lo que es igual a la cantidad de elementos que hay en la memoria,
                    # habria que sumarle 1, pero como el estado incial lo tenenmos en memoria y no debe contarse para el coste, nos ahorramos sumarle 1
                    return "\nSe ha encontrado el estado final: " + str(
                        list(estadoGenerado)) + " con coste del algoritmo: " + str(
                        len(memoria)) + " Se han usado "+ str(discrepancias)+" discrepancias\nEl tiempo de ejecución ha sido: " + str(tiempoFinal - tiempoInicio) + " segundos."

        """"Ordenamos por heuristica"""
        if (type(problema) is N_Crepes):
            estadosSucesores = sorted(estadosSucesores, key=comparatorGap(heuristicaGap))
        else:
            estadosSucesores = sorted(estadosSucesores,
                                      key=comparatorManhattan(heuristicaManhattan, problema.longitudFila))

        """"Dividimos todos los estados sucesores en B bloques en funcion de la anchura del haz"""
        estadosSucesoresEnBloques = [estadosSucesores[i:i + anchuraHaz] for i in
                                     range(0, len(estadosSucesores), anchuraHaz)]




        # FIXME: de alguna manera hay que finalizr esto cuando pruebe todas las combinaciones para un tamaño de memoria concreto

        """"Vemos que haya un bloque B con indice que nos toca buscar con el backtraking en los sucesores, si se han acabado hay que subir un nivel como cuando la memoria esta llena"""
        #ESTE CASO NO ESTA MUY CONTEMPLADO QUE DIGAMOS creo que no se da nunca puesto que siempre se coge el primer elemento de los sucesores a no ser que tenga discrepancia
        # if (len(estadosSucesoresEnBloques) <= bASeleccionarDict[len(memoria)][0]):
        #     if (len(memoria) <= 1):
        #         Estos petara cuando todos los niveles del diccionario tengan a visitar el nodo 0 y tengan usada la discrepancia
        #         raise Exception(
        #             'Mediante el backtraking hemos llegado al estado inicial sin encontrar solucion en ninguno de sus estados sucesores ')
        #     memoriaLlena = 0
        #     memoria = aplicaBacktrackingDiscrepancias(memoria, bASeleccionarDict, memoriaLlena)
        #     continue

        # else:






        """Si tiene marcada para usar discrepancia en dicho nivel y hay un posible cantidad de bloques generados suficientes """
        if (bASeleccionarDict[len(memoria)][1] and len(estadosSucesoresEnBloques) > bASeleccionarDict[len(memoria)][0] + 1):
            # discrepanciasUsadas += 1
            bAExplorar = estadosSucesoresEnBloques[bASeleccionarDict[len(memoria)][0] + 1]

            """ los de proximos sucesores de este nivel abajo tendra que coger los primeros para todos, contemplando siempre las discrepancias que quedan"""

            """buscamos las discrepancias usadas por arriba de este nivel obsrvado para asi saber cuantas quedan por asociar"""
            actualizaInforNivelesSucesores(nivelSiguienteAExplorar, bASeleccionarDict)


        else:
            """Si tiene marcada discrepancia para el proximo nivel pero no hay ya bloques a los que visitar tras esa discrepancia entonces seleccionamos el primero y recuperamos esa discrepancia"""
            if (bASeleccionarDict[len(memoria)][1]):
                """Pregunta para tutoria si no hay tal cantidad de bloques como indica la  discrepancia se guarda para el proximo que lo permita"""

                aux = bASeleccionarDict[len(memoria)]
                # marcamos que ya para ese nivel no usamos discrepancia,
                aux[1] = 0
                #  pero que ya se ha usado hasta visitar todos sus sucesores
                aux[2] = 1
                bASeleccionarDict[len(memoria)] = aux
                bAExplorar = estadosSucesoresEnBloques[0]

                """Actualizamos la informacion para la busqueda con los sucesores, basicamente todos empezaran a buscar en el nodo 0, pondremos que ninguno ha usado discrepancia  y pondremos para el proximo nodo que tendra que usar discrepancia"""

                actualizaInforNivelesSucesores(nivelSiguienteAExplorar, bASeleccionarDict)


            else:
                """No tiene discrepancias y hay disponible un B para el indice indicado en el nivel siguiente"""
                bAExplorar = estadosSucesoresEnBloques[bASeleccionarDict[len(memoria)][0]]

        # si no cumple el tamaño del haz no pasa nada se explora lo que haya dentro

        """El B que usamos es el indicado por el algoritmo siempre sera el primero hasta que haya backtracking y haya que coger otro"""
        memoria.append(bAExplorar)

        """Comprobamos si la memoria esta llena"""
        if (len(memoriaAplanada) >= tamMemoria):
            memoriaLlena = 1
            memoria = aplicaBacktrackingDiscrepancias(memoria, bASeleccionarDict, memoriaLlena)

            """Fin -> completada la memoria con el backtracking y discrepancias completas"""
            if(memoria == "-1"):
                tiempoFinal = time.clock()
                return "\nSe ha llenado la memoria usando: "+ str(discrepancias) +" discrepancias sin encontrar estado final con coste del algoritmo: " + str(
                    len(memoria)) + "\nEl tiempo de ejecución ha sido: " + str(
                    tiempoFinal - tiempoInicio) + " segundos."


            continue


        """Si es la primera vez que se llega a un nivel nuevo se indica que la b siguiente a buscar es la pimera"""
        if (len(memoria) not in bASeleccionarDict):
            bASeleccionarDict[len(memoria)] = [0, 0 , 0]


        """Esto hay que verlo crep que no vale actaulemten mejor verlo de otra manera
        if (discrepancias - discrepanciasUsadas > 0):
          #Si quedan discrepancias sin usar la marcamos para usar en el siguiente nivel
            aux = bASeleccionarDict[len(memoria)]
            # marcamos que para ese nivel usamos discrepancia
            aux[1] = 1
            bASeleccionarDict[len(memoria)] = aux
        """


""" Metodo para inicializar la busqueda iterativa """


def inicializaBusquedaHazBacktrackingDiscrepancias(anchuraHaz, tamMemoria, tipoProblema, estadoInicial):
    global bAExplorar
    """ El estado inicial lo ponemos en la memoria por si hay que volver atras para generar sucesores con el backtraking """
    memoria = []

    """" bAExplorar es la B actual que estamos visitando incialmente solo el estado inicial """
    bAExplorar = [estadoInicial]

    memoria.append(bAExplorar)

    """" Para saber que B debe seleccionar en cada nivel, usaremos un diccionario que tenga como clave el nivel y como valor el b para ese nivel que debe seleccionar,
     el segundo parametro indicara 0-> no usa discrepancias 1-> usa discrepancias para ese nivel """
    bASeleccionarDict = dict()
    # Es decir para el nivel 1 (el que surge de explorar el estado inicial) tenemos que se va explorar incialmente el primer bloque b sin uar discrepancia acutalmente y el tercer elemento 0 indica que en el no se ha usado discrepancia nunca
    bASeleccionarDict[1] = [0, 0, 0]



    """ Elegimos entre los dos tipos de problemas """
    if (tipoProblema == 'N-Crepes'):
        problema = N_Crepes(estadoInicial)

    elif (tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)

    """ Iniciamos el algortimo iterativo de busqueda """
    return busquedaHazBacktrackingDiscrepancias(anchuraHaz, tamMemoria, memoria, problema, bASeleccionarDict)


# Iniciamos el problema declarando los datos
""" Aqui inicializamos el problema que vamos a probar """
anchoDelHaz = 10
tamDeMemoria = 60
tipoProblema = 'N-Puzzle'  # dos tipos: N-Puzzle o N-Crepes
estadoInicial = (8, 7, 6, 5, 4, 3, 2, 1, 0)

print(inicializaBusquedaHazBacktrackingDiscrepancias(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))
