import time

from N_Crepes import *
from N_Puzzle import *
from Utilidades import *
import random
"""Metodo llamado desde el metodo busquedaHazBacktracking en el caso que se deba hacer backTracking"""
def aplicaBacktracking(memoria):
    global coste
    global bAExplorar
    global bASeleccionarDict
    memoria.pop()  # borramos el bloque superior para volver a explorar sus sucesores y coger el siguiente

    """"El bloque B de estados a analizar es en este caso el ultimo almacenado en la memoria tras haber borrado
        el que estabamos visitando, no hay que ordenarlos por heuristica ni nada porque en la memoria ya se introducen ordenados"""
    bAExplorar = memoria[len(memoria) - 1]

    """"Llamamos recursivamente Con el B anterior almacenado pero habra que indicar que de sus sucesores no coja el primer bloque B sino el que le toque debido al backtraking"""
    nivelSiguienteAExplorar = len(memoria)
    bASeleccionarDict[nivelSiguienteAExplorar] = bASeleccionarDict[nivelSiguienteAExplorar] + 1

    """Cada vez que subimos con backtraking un nivel debemos indicar que los niveles de abajo vuelva a buscar a partir del bloque 0"""
    for i in range(nivelSiguienteAExplorar + 1, len(bASeleccionarDict) + 1):
        bASeleccionarDict[i] = 0

    print("Hacemos backtraking debido a que se han explorado todos los sucesores del nivel: " + str(
        nivelSiguienteAExplorar) + str(bAExplorar))
    coste -= 1
    return memoria

def busquedaHazBacktracking(anchuraHaz, tamMemoria, memoria, problema ):
    global bAExplorar
    global coste
    global bASeleccionarDict
    tiempoInicio=time.clock()

    while (1):
        # Aplanamos todos los estados contenidos en cada bloque de la memoria para comprobar si esta contenido el estado observado actual en algun bloque
        memoriaAplanada = sum(memoria, [])
        """Limpiamos los sucesores de la anterior iteracion"""
        #Todos los estados que van a generarse apartir del bloque actual B que estamos visitando
        estadosSucesores = []
        print("Se va a exploarr "+ str(bAExplorar))

        """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
        for estado in bAExplorar:
            accionesAplicables = problema.acciones(estado)
            for accion in accionesAplicables:
                estadoGenerado = problema.aplica(estado, accion)

                if (not (estadoGenerado in memoriaAplanada) and not (estadoGenerado in estadosSucesores)):
                    estadosSucesores.append(estadoGenerado)

                """Comprobamos si alguno de los nuevos estados generados son final"""
                if (problema.es_estado_final(list(estadoGenerado))):
                    tiempoFinal = time.clock()

                    return "\nSe ha encontrado el estado final: " + str(
                        list(estadoGenerado)) + " con coste del algoritmo: " + str(coste)+"\nEl tiempo de ejecución ha sido: " + str(tiempoFinal-tiempoInicio) +  " segundos."

        """"Ordenamos por heuristica"""
        if (type(problema) is N_Crepes):
            estadosSucesores = sorted(estadosSucesores, key=comparatorGap(heuristicaGap))
        else:
            estadosSucesores = sorted(estadosSucesores,
                                      key=comparatorManhattan(heuristicaManhattan, problema.longitudFila))

        """"Dividimos todos los estados sucesores en B bloques en funcion de la anchura del haz"""
        estadosSucesoresEnBloques = [estadosSucesores[i:i + anchuraHaz] for i in
                                     range(0, len(estadosSucesores), anchuraHaz)]
        print("para el nivel "+ str(len(memoria))+ " Salen los siguientes sucesores"+ str(estadosSucesoresEnBloques))
        """"Vemos que haya un bloque B con indice que nos toca buscar con el backtraking en los sucesores, si se han acabado hay que subir un nivel como cuando la memoria esta llena"""
        if (len(estadosSucesoresEnBloques)== 0 or len(estadosSucesoresEnBloques) <= bASeleccionarDict[len(memoria)]):
            if (len(memoria) <= 1):
                tiempoFinal = time.clock()
                return "\nNo se ha podido encontrar un estado final, se ha llegado al estado inicial con backtracking habiendo explorado todos los niveles hasta completar la memoria: " + \
                       str(tamMemoria) + "\nEl tiempo de ejecución ha sido: " + str(
                    tiempoFinal - tiempoInicio) + " segundos."

            memoria=aplicaBacktracking(memoria)
            continue

        else:
            bAExplorar = estadosSucesoresEnBloques[bASeleccionarDict[len(memoria)]]

        # si no cumple el tamaño del haz no pasa nada se explora lo que haya dentro

        """El B que usamos es el indicado por el algoritmo siempre sera el primero hasta que haya backtracking y haya que coger otro"""
        memoria.append(bAExplorar)

        memoriaAplanada = sum(memoria, [])
        """Comprobamos si la memoria esta llena"""
        if (len(memoriaAplanada) >= tamMemoria):
            #en este caso quitamos el nodo que acabamos de insertar puesto que ya no cabe en la memoria
            memoria.pop()
            memoria=aplicaBacktracking(memoria)
            continue


        """Si es la primera vez que se llega a un nivel nuevo se indica que la b siguiente a buscar es la pimera"""
        if (len(memoria) not in bASeleccionarDict):
            bASeleccionarDict[len(memoria)] = 0

        coste += 1




""" Metodo para inicializar la busqueda iterativa """
def inicializaBusquedaHazBacktracking(anchuraHaz, tamMemoria, tipoProblema, estadoInicial):
    global bAExplorar
    global coste
    global bASeleccionarDict
    problema = None
    """ El estado inicial lo ponemos en la memoria por si hay que volver atras para generar sucesores con el backtraking """
    memoria = []
    aux = [estadoInicial]
    memoria.append(aux)

    """" El coste inicial del algoritmo es 0"""
    coste = 0

    """" Para saber que B debe seleccionar en cada nivel, usaremos un diccionario que tenga como clave el nivel y como valor el b para ese nivel que debe seleccionar """
    bASeleccionarDict = dict()
    # Es decir para el nivel 1 (el que surge de explorar el estado inicial) tenemos que se va explorar incialmente el primer bloque b
    bASeleccionarDict[1] = 0

    """" bAExplorar es la B actual que estamos visitando incialmente solo el estado inicial """
    bAExplorar = [estadoInicial]

    """ Elegimos entre los dos tipos de problemas """
    if (tipoProblema == 'N-Crepes'):
        problema = N_Crepes(estadoInicial)

    elif (tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)

    """ Iniciamos el algortimo iterativo de busqueda """
    return busquedaHazBacktracking(anchuraHaz, tamMemoria, memoria, problema)


# Iniciamos el problema declarando los datos
#ese ejemplo de ahi me ha tardado 65 segundos pero lo ha resuelto con backtraking el normal con esas caracteristicas no es capaz de resolverlo
""" Aqui inicializamos el problema que vamos a probar """
anchoDelHaz = 4
tamDeMemoria = 130
tipoProblema = 'N-Puzzle'  # dos tipos: N-Puzzle o N-Crepes
estadoInicial = (8, 7, 6, 5, 4, 3, 2, 1, 0)

print(inicializaBusquedaHazBacktracking(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))
"""Aqui inicializamos los datos del problema que vamos a probar"""
# anchoDelHaz=10
# tamDeMemoria=280 #siempre que la memoria sea <= al coste que nos retorna el algoritmo petara por llenar la memoria
# tipoProblema='N-Crepes' #dos tipos: N-Puzzle o N-Crepes
# #estadoInicial=(8, 7, 6, 5, 4, 3, 2, 1, 0)
#
# #estadoInicial=(4, 8, 5, 6, 1, 7, 2, 0, 3) #este estado en concreto hace que pete por memoria
#
# #tener en cuenta que este algoritmo no estamos metiendo en memoria el estado inicial puesto que es irrelevante porque no lo necesitaremos en el backtracking ya que no hjay en este algoritmo
# #en el de backtraking si metemos el incial puesto que podemos llegar a el con backtracking entonces o esto se le comenta al profesor o para que se pueda comparar la capacidad de las memoria deberiamos meterlo aqui tambien
# #print(inicializaBusquedaHaz(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))
#
# random.seed(20152016) #Establecemos semilla
#
# for x in range(0, 50): #Generamos los 100 problemas y los ejecutamos
#     estadoInicial = tuple(random.sample(range(1,31), 30)) #Devuelve una lista única de 9 elementos elegidos de entre la secuencia de población.
#
#     print("    ")
#     print("||------ Ejecución número " + str(x+1) + "------||")
#     print("||30-Crepes, estado inicial: " + str(estadoInicial) + "||")
#     print(inicializaBusquedaHazBacktracking(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))
#     print("||-------------------------------------------------||")
