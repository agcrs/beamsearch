from N_Crepes import *
from N_Puzzle import *
from Utilidades import *

"""Metodo para inicializar la recursividad nos valdra para compartir variables y no tener que meterlas en la ram en cada recursion"""
def inicializaBusquedaHaz(anchHaz, tamMem, tipoProblema, estadoInicial):
    """"Preparamos los datos para la llamada la algoritmo de busqueda"""
    problema=None
    global estadosSucesores
    global bloqueEstadosActual
    anchuraHaz = anchHaz
    tamMemoria = tamMem
    memoria = []
    estadosSucesores = []
    costeInicial = 0
    """"bloqueEstadosActual es la B actual que estamos visitando incialmente solo el estado inicial"""
    bloqueEstadosActual = [estadoInicial]


    #elegimos entre los dos tipos de problemas
    if (tipoProblema == 'N-Crepes'):
        problema = N_Crepes(estadoInicial)

    elif (tipoProblema == 'N-Puzzle'):
        problema = N_Puzzle(estadoInicial)



    #Algoritmo recursivo que llamaremos desde estee propio metodo
    def busquedaHaz(problema, coste):
        """Todos los estados que van a generarse apartir del bloque actual que estamos visitando"""
        global estadosSucesores
        global bloqueEstadosActual

        """si es la primera vez que se llama tenemos un solo estado-> el inicial en los bloques acutales"""
        for estado in bloqueEstadosActual:
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

        """Si no ha encontrado estado final y hemos llenado la memoria lanzamos una excepcion"""
        if (len(memoria) == tamMemoria):
            raise Exception(
                'El tamaño de la memoria:+ ' + str(tamMemoria) + ' ha llegado a su limite no caben mas bloques B.')

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
        bSiguienteAExplorar = estadosSucesoresEnBloques[0]

        """Limpiamos los sucesores de la anterior iteracion"""
        estadosSucesores = []


        #He quitado el limite del haz porque sino es una mierda a veces solo tiene pocas acciones aplicable o la primera vez que inicia a lo sumo tiene 4
        """Pendiente de preguntar en tutoria
        if (len(bSiguienteAExplorar) < anchuraHaz):
            # En este caso debemos lanzar error en la aplicacion
            raise Exception('La generacion de sucesores no ha completado el tamaño del bloque B = ' + str(anchuraHaz))
        """

        """Lo ponemos en memoria en memoria"""
        memoria.append(bSiguienteAExplorar)

        print(bSiguienteAExplorar)

        bloqueEstadosActual = bSiguienteAExplorar
        """"Llamamos recursivamente"""
        return busquedaHaz(problema, coste + 1)

    """Iniciamos el algortimo recursivo de busqueda"""
    return busquedaHaz(problema, costeInicial)




"""Aqui inicializamos el problema que vamos a probar"""
anchoDelHaz=20
tamDeMemoria=100
TipoProblema='N-Puzzle' #dos tipos: N-Puzzle o N-Crepes
estadoInicial=(8, 7, 6, 5, 4, 3, 2, 1, 0)


#siempre que la memoria sea inferior al coste que nos retorna el algoritmo petara por llenar la memoria
print(inicializaBusquedaHaz(20, 33, 'N-Puzzle', (8, 7, 6, 5, 4, 3, 2, 1, 0)))


