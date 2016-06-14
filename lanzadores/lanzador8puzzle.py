from N_Crepes import *
from N_Puzzle import *
from Utilidades import *
import random
from BusquedaHaz import *
#from BusquedaHazBackTracking import *
#from BusquedaHazBacktrackingDiscrepancias import *

"""Aqui inicializamos los datos del problema que vamos a probar"""
anchoDelHaz=10
tamDeMemoria=100 #siempre que la memoria sea <= al coste que nos retorna el algoritmo petara por llenar la memoria
tipoProblema='N-Puzzle' #dos tipos: N-Puzzle o N-Crepes
#estadoInicial=(8, 7, 6, 5, 4, 3, 2, 1, 0)

#estadoInicial=(4, 8, 5, 6, 1, 7, 2, 0, 3) #este estado en concreto hace que pete por memoria

#tener en cuenta que este algoritmo no estamos metiendo en memoria el estado inicial puesto que es irrelevante porque no lo necesitaremos en el backtracking ya que no hjay en este algoritmo
#en el de backtraking si metemos el incial puesto que podemos llegar a el con backtracking entonces o esto se le comenta al profesor o para que se pueda comparar la capacidad de las memoria deberiamos meterlo aqui tambien
#print(inicializaBusquedaHaz(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))

random.seed(20152016) #Establecemos semilla

for x in range(0, 100): #Generamos los 100 problemas y los ejecutamos
    estadoInicial = random.sample(range(0,9), 9) #Devuelve una lista única de 9 elementos elegidos de entre la secuencia de población.

    print("    ")
    print("||------ Ejecución número " + str(x+1) + "------||")
    print("||8-Puzzle, estado inicial: " + str(estadoInicial) + "||")
    print(inicializaBusquedaHaz(anchoDelHaz, tamDeMemoria, tipoProblema, estadoInicial))
    print("||-------------------------------------------------||")
