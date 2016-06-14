import random
import time
from N_Crepes import *
from N_Puzzle import *
from Utilidades import *

"""Metodo para inicializar la busqueda nos valdra para compartir variables y no tener que meterlas en la ram en cada recursion"""
def inicializaBusquedaHaz(anchHaz, tamMem, tipoProblema, estadoInicial):
    """"Preparamos los datos para la llamada la algoritmo de busqueda"""
    problema = None
    global estadosSucesores
    global bAExplorar
    anchuraHaz = anchHaz
    tamMemoria = tamMem
    memoria = []
    estadosSucesores = []
    costeInicial = 0
    """"bAExplorar es la B actual que estamos visitando incialmente solo el estado inicial"""
    bAExplorar = [estadoInicial]

    """Metemos el estado inicial en memoria, es irrelevante puesto que aqui no hay backtraking,
      pero para igualar el tamaño de la memoria  y las iteraciones del algoritmo de backtracking debemos hacerlo,
      ya que en el de backtracking si debemos meterlo en la memoria"""
    memoria.append(estadoInicial)


    #elegimos entre los dos tipos de problemas
    if (tipoProblema == 'N-Crepes'):
        problema = N_Crepes(estadoInicial)

    elif (tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)



    #Algoritmo iterativo
    def busquedaHaz(problema, coste):
        """Todos los estados que van a generarse apartir del bloque actual que estamos visitando"""
        global estadosSucesores
        global bAExplorar
        tiempoInicio = time.clock()

        while(1):
            """Limpiamos los sucesores de la anterior iteracion"""
            estadosSucesores = []

            """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
            for estado in bAExplorar:
                accionesAplicables = problema.acciones(estado)
                for accion in accionesAplicables:
                    estadoGenerado = problema.aplica(estado, accion)

                    """"Preguntar en  tutoria si eso es asi, es decir si el estado esta en memoria no se añade a sucesores"""
                    if (not (estadoGenerado in memoria) and not (estadoGenerado in estadosSucesores)):
                        estadosSucesores.append(estadoGenerado)

                    """Comprobamos si los nuevos estados generados son estado final"""
                    if (problema.es_estado_final(list(estadoGenerado))):
                        tiempoFinal = time.clock()

                        return "\nSe ha encontrado el estado final: " + str(list(estadoGenerado)) + " con coste del algoritmo: " + \
                               str(coste) + "\nEl tiempo de ejecución ha sido: " + str(tiempoFinal - tiempoInicio) + " segundos."



            """Si no ha encontrado estado final y hemos llenado la memoria lanzamos una excepcion"""
            if (len(memoria) >= tamMemoria):
                #raise Exception(
                #    'El tamaño de la memoria: ' + str(tamMemoria) + ' ha llegado a su limite no caben mas bloques B.')
                tiempoFinal = time.clock()

                return "\nNo se ha podido encontrar un estado final, se ha alcanzado el límite de la memoria: " + \
                    str(tamMemoria) + "\nEl tiempo de ejecución ha sido: " + str(tiempoFinal - tiempoInicio) + " segundos."

            """"Ordenamos por heuristica"""
            if (type(problema) is N_Crepes):
                estadosSucesores = sorted(estadosSucesores, key=comparatorGap(heuristicaGap))
            else:
                estadosSucesores = sorted(estadosSucesores,
                                          key=comparatorManhattan(heuristicaManhattan, problema.longitudFila))

            """"Dividimos todos los estados sucesores en B bloques en funcion de la anchura del haz"""
            estadosSucesoresEnBloques = [estadosSucesores[i:i + anchuraHaz] for i in
                                         range(0, len(estadosSucesores), anchuraHaz)]

            """"Cogemos el primer bloque ya que en este algoritmo sin backtracking siempre se explorará el primero"""
            bAExplorar = estadosSucesoresEnBloques[0]


            """Lo ponemos en memoria en memoria"""
            for estado in bAExplorar:
                memoria.append(estado)

            #print(bAExplorar)

            coste+=1

    """Iniciamos el algortimo iterativo de busqueda"""
    return busquedaHaz(problema, costeInicial)




# """Aqui inicializamos los datos del problema que vamos a probar"""
# anchoDelHaz=100
# tamDeMemoria=3000 #siempre que la memoria sea <= al coste que nos retorna el algoritmo petara por llenar la memoria
# tipoProblema='N-Puzzle' #dos tipos: N-Puzzle o N-Crepes
# estadoInicial=(8, 7, 6, 5, 4, 3, 2, 1, 0)
#
# # tener en cuenta que este algoritmo no estamos metiendo en memoria el estado inicial puesto que es irrelevante porque no lo necesitaremos en el backtracking ya que no hjay en este algoritmo
# # en el de backtraking si metemos el incial puesto que podemos llegar a el con backtracking entonces o esto se le comenta al profesor o para que se pueda comparar la capacidad de las memoria deberiamos meterlo aqui tambien
# print(inicializaBusquedaHaz(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))


