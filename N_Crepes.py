import math
from ProblemaEspacioEstados import Problema


class N_Crepes(Problema):

    def __init__(self, pilaInicial):
        longPila=len(pilaInicial)
        super().__init__(estado_inicial=pilaInicial, n=longPila, estado_final=list(range(1,longPila+1)))

    def acciones(self, estado):
        acciones_aplicables = list(range(2 ,self.n+1))
        return acciones_aplicables

    def aplica(self, estado, accion):
        """"restamos uno a la accion ya que el indice de la lista empieza en 0 o en 1"""
        accion-=1
        """Obtenemos una tupla con los k primeros elementos invertidos"""
        estadoKInvertido = estado[accion::-1]

        """"Añadimos a la tupla con los k elementos invertidos con el resto"""
        return estadoKInvertido+estado[accion+1::]

"""
#Ejemplos que se pueden ejecutar una vez se ha definido la clase:
p8p_1 = N_Crepes((1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15))
print(p8p_1.estado_inicial)
# (2, 8, 3, 1, 6, 4, 7, 0, 5)
print(p8p_1.estado_final)
# (1, 2, 3, 8, 0, 4, 7, 6, 5)
accionesAplicables=p8p_1.acciones(p8p_1.estado_inicial)
print(accionesAplicables)
# ['Mover hueco arriba', 'Mover hueco izquierda', 'Mover hueco derecha']
print("Accion que se va a aplicar " + str(accionesAplicables[7]))
print(p8p_1.aplica(p8p_1.estado_inicial,accionesAplicables[7]))
# (2, 8, 3, 1, 0, 4, 7, 6, 5)
print(p8p_1.coste_de_aplicar_accion(p8p_1.estado_inicial,"Mover hueco arriba"))
# 1
"""