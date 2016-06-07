
from SolucionesIA.algoritmos_de_búsqueda import *
from N_Puzzle import *
from N_Crepes import *
# -----------
# Ejercicio 2
# -----------

# Usar búsqueda en anchura y en profundidad para encontrar soluciones tanto al
# problema de las jarras como al problema del ocho puzzle con distintos
# estados iniciales.
#
# Ejemplos de uso:
nCrepes = N_Crepes((6, 11, 12, 13, 1, 7, 14, 8, 9, 10, 2, 3, 4, 5, 15))
nPuzzles = N_Puzzle(( 7, 8, 0, 1, 2, 3, 4, 5, 6))

BúsquedaEnAnchura(nCrepes).solucion()
