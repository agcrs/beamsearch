# Práctica 3: Algoritmos genéticos
# ===========================================================================

# En esta práctica veremos la implementación en Python de un algoritmo
# genético y su aplicación para resolver instancias concretas del problema de
# la mochila.

# La práctica se estructura en tres partes:
# * En la primera, veremos una implementación concreta de un algoritmo
#   genético.
# * En la segunda, veremos cómo implementar la representación del problema de
#   la mochila para ser resuelto mediante algoritmos genéticos.
# * En la tercera parte, probaremos los algoritmos genéticos sobre los
#   problemas definidos.

# Necesitaremos el módulo random:
import random


# ================================================
# Parte I: Implementación de un algoritmo genético
# ================================================

# -----------
# Ejercicio 1
# -----------

# Definir una clase Problema_Genetico que incluya los elementos necesarios
# para la representación de un problema de optimización pueda ser abordado
# mediante un algoritmo genetico.

# Estos elementos son:

# - genes: lista de genes usados en el genotipo de los estados.
# - longitud_individuos: longitud de los cromosomas
# - decodifica: función de obtiene el fenotipo a partir del genotipo.
# - fitness: función

# Todos estos datos y funciones se almacenarán en sendos atributos de datos de
# la clase.

# Además, la clase debe incluir dos métodos:
# - muta: mutación de un cromosoma
# - cruza: cruce de un par de cromosomas
# Implementar las mutaciones y cruces tal y como se han definido en clase.

# Nótese que en la definición de esta clase no se especifica si el problema es
# de maximización o de minimización, ya que esto se especificará como
# parámetro en el algoritmo genético que vamos a implementar.

# ================ Solución:

class Problema_Genetico:
    """ Clase para representar un problema para que sea abordado mediante un
    algoritmo genético general. Consta de los siguientes atributos:
    - genes: lista de posibles genes en un cromosoma
    - longitud_individuos: la longitud de los cromosomas
    - decodifica: método que recibe el fenotipo (cromosoma) y devuelve el
      fenotipo (elemento del problema original que el cromosoma representa)
    - fitness: método de valoración de los cromosomas (actúa sobre el
      genotipo)
    - muta: función que realiza una mutación de un cromosoma
    - cruza: función que realiza un cruce entre dos cromosomas"""

    def __init__(self, genes, longitud_individuos, decodifica, fitness):
        self.genes = genes
        self.longitud_individuos = longitud_individuos
        self.decodifica = decodifica
        self.fitness = fitness

    def muta(self, c, prob):
        cm = c[:]  # una copia
        for i in range(len(cm)):
            if random.random() < prob:
                cm[i] = random.choice(self.genes)
        return cm

    def cruza(self, c1, c2):
        pos = random.randrange(1, self.longitud_individuos - 1)
        cr1 = c1[:pos] + c2[pos:]
        cr2 = c2[:pos] + c1[pos:]
        return [cr1, cr2]


# -----------
# Ejercicio 2
# -----------

# Definir una variable cuad_gen, que referencia a una instancia de la clase
# anterior, correspondiente al problema de optimizar (maximizar o minimizar)
# la función cuadrado en el conjunto de los números naturales menores que
# 2^{10}.

# Será necesaria la siguiente función que interpreta una lista de 0's y 1's
# como un número natural:

def binario_a_decimal(x):
    return sum(b * (2 ** i) for (i, b) in enumerate(x))

# Más eficiente y, además, funciona con los dígitos en el orden natural.
# def binario_a_decimal (x):
#     num = 0
#     for i in x:
#         num <<= 1
#         num += i
#     return num

cuad_gen = Problema_Genetico([0, 1], 10, binario_a_decimal,
                             lambda x: binario_a_decimal(x) ** 2)

# Una vez definido cuad_gen, probar alguna de las funciones definidas en la
# clase anterior, para esta instancia concreta. Por ejemplo:

# >>> cuad_gen.decodifica([1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1])
# 1329
# >>> cuad_gen.fitness([1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1])
# 1766241
# >>> cuad_gen.muta([1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1], 0.1)
# [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
# >>> cuad_gen.muta([1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1], 0.1)
# [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
# >>> cuad_gen.cruza([1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 0, 0, 1, 1, 1])
# [[1, 0, 0, 0, 1, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1]]


# -----------
# Ejercicio 3
# -----------

# Definir una función poblacion_inicial(problema_genetico, tamaño), para
# definir una población inicial de un tamaño dado, para una instancia dada de
# la clase anterior Problema_Genetico

# INDICACIÓN: Usar random.choice

# ======== Solución:

def poblacion_inicial(problema_genetico, tamaño):
    def generar_cromosoma():
        return [random.choice(problema_genetico.genes)
                for _ in range(problema_genetico.longitud_individuos)]
    return [generar_cromosoma() for _ in range(tamaño)]

# =========================


# -----------
# Ejercicio 4
# -----------

# Definir una función cruza_padres(problema_genetico, padres), que recibiendo
# una instancia de Problema_Genetico y una población de padres (supondremos
# que hay un número par de padres), obtiene la población resultante de
# cruzarlos de dos en dos (en el orden en que aparecen)

# ======= Solución

def cruza_padres(problema_genetico, padres):
    padres = iter(padres)
    return sum([problema_genetico.cruza(padre1, padre2)
                for padre1, padre2 in zip(padres, padres)],
               [])

# ================


# -----------
# Ejercicio 5
# -----------

# Definir una función muta_individuos(problema_genetico, poblacion, prob), que
# recibiendo una instancia de Problema_Genetico, una población y una
# probabilidad de mutación, obtiene la población resultante de aplicar
# operaciones de mutación a cada individuo.

# =========== Solución:

def muta_individuos(problema_genetico, poblacion, prob):
    return [problema_genetico.muta(c, prob) for c in poblacion]

# =============================================


# -----------
# Ejercicio 6
# -----------

# Definir una función
# seleccion_por_torneo(problema_genetico, poblacion, n, k, opt)
# que implementa la selección mediante torneo de n individuos de una
# población.  Esta función recibe como entrada una instancia de
# Problema_Genetico, una población, un número natural n (número de individuos
# a seleccionar) un número natural k (número de participantes en el torneo) y
# un valor opt que puede ser o la función max o la función min (dependiendo de
# si el problema es de maximización o de minimización, resp.).

# INDICACIÓN: Usar random.sample

# ======= Solución:


def seleccion_por_torneo(problema_genetico, poblacion, n, k, opt):
    def selecciona_uno_por_torneo():
        participantes = random.sample(poblacion, k)
        return opt(participantes, key=problema_genetico.fitness)
    return [selecciona_uno_por_torneo() for _ in range(n)]

# ================


# La siguiente función algoritmo_genetico_t implementa un algoritmo genetico
# que selecciona individuos mediante el método del torneo.

def algoritmo_genetico_t(problema_genetico, k, opt, ngen, tamaño,
                         prop_cruces, prob_mutar):
    poblacion = poblacion_inicial(problema_genetico, tamaño)
    n_padres = round(tamaño * prop_cruces)
    n_padres = (n_padres if n_padres % 2 == 0 else n_padres - 1)
    n_directos = tamaño - n_padres
    for _ in range(ngen):
        poblacion = nueva_generacion_t(problema_genetico, k, opt, poblacion,
                                       n_padres, n_directos, prob_mutar)
    mejor_cr = opt(poblacion, key=problema_genetico.fitness)
    mejor = problema_genetico.decodifica(mejor_cr)
    return (mejor, problema_genetico.fitness(mejor_cr))


# Sus argumentos de entrada son:

# * problema_genetico: una instancia de la clase Problema_Genetico, con el
#   problema de optimización que se quiere resolver.
# * k: número de participantes en los torneos de selección.
# * opt: max ó min, dependiendo si el problema es de maximización o de
#   minimización.
# * ngen: número de generaciones (condición de terminación)
# * tamaño: número de individuos en cada generación
# * prop_cruces: proporción del total de la población que serán padres.
# * prob_mutar: probabilidad de realizar una mutación de un gen.


# -----------
# Ejercicio 7
# -----------

# Se pide definir la única función auxiliar que queda por definir en el
# algoritmo anterior; es decir, la función
# nueva_generacion_t(problema_genetico,poblacion,n_padres,n_directos,prob_mutar)
# que a partir de una población dada, calcula la siguiente generación.

# Una vez definida, ejecutar el algoritmo genético anterior, para resolver el
# problema cuad_gen (tanto en minimización como en maximización).

# Por ejemplo:

# >>> algoritmo_genetico_t(cuad_gen, 3, min, 20, 10, 0.7, 0.1)
# (0, 0)
# >>> algoritmo_genetico_t(cuad_gen, 3, max, 20, 10, 0.7, 0.1)
# (1023, 1046529)

# NOTA: téngase en cuenta que el algoritmo genético devuelve un par con el
# mejor fenotipo encontrado, y su valoración.


# =========== Solución:

def nueva_generacion_t(problema_genetico, k, opt, poblacion, n_padres,
                       n_directos, prob_mutar):
    padres = seleccion_por_torneo(problema_genetico, poblacion, n_padres,
                                  k, opt)
    directos = seleccion_por_torneo(problema_genetico, poblacion, n_directos,
                                    k, opt)
    hijos = cruza_padres(problema_genetico, padres)
    return muta_individuos(problema_genetico, hijos + directos, prob_mutar)

# =======================


# ===================================================
# Parte II: Representación del problema de la mochila
# ===================================================

# Problema de la mochila: dados n objetos de pesos p_i y valor v_i
# (i=1,...,n), seleccionar cuáles se meten en una mochila que soporta un
# peso P máximo, de manera que se máximice el valor de los objetos
# introducidos.


# -----------
# Ejercicio 8
# -----------

# Definir una función
# decodifica_mochila(cromosoma, n_objetos, pesos, capacidad)
# que recibe como entrada:

# - un cromosoma (en este caso, una lista de 0s y 1s, de longitud igual a
#   n_objetos)
# - n_objetos: número total de objetos de la mochila
# - pesos: una lista con los pesos de los objetos
# - capacidad: peso máximo de la mochila.

# Esta función debe devolver una lista de 0s y 1s que indique qué objetos están
# en la mochila y cuáles no (el objeto i está en la mochila si y sólo si en la
# posción i-ésima de la lista hay un 1). Esta lista se obtendrá a partir del
# cromosoma, pero teniendo en cuenta que a partir del primer objeto que no
# quepa, éste y los siguientes se consideran fuera de la mochila,
# independientemente del valor que haya en su correspondiente posición de
# cromosoma.


# ========== Solución:

def decodifica_mochila(cromosoma, n_objetos, pesos, capacidad):
    en_mochila = [0] * n_objetos
    peso_acumulado = 0
    for i, (objeto, peso) in enumerate(zip(cromosoma, pesos)):
        if objeto:
            peso_acumulado += peso
            if peso_acumulado > capacidad:
                break
            en_mochila[i] = 1
    return en_mochila

# ==============================================


# -----------
# Ejercicio 8
# -----------

# Definir una función

# fitness_mochila(cromosoma, n_objetos, pesos, capacidad, valores)

# que devuelva el valor total de los objetos que están dentro de la mochila
# que representa el cromosma, según la codificación explicada en el ejercicio
# anterior. Aquí valores es la lista de los valores de cada objeto y el resto
# de argumentos son los mismos que en el ejercicio anterior.

# ============== Solución:

def fitness_mochila(cromosoma, n_objetos, pesos, capacidad, valores):
    en_mochila = decodifica_mochila(cromosoma, n_objetos, pesos, capacidad)
    return sum(valor for objeto, valor in zip(en_mochila, valores) if objeto)

# ===============================================


# ============================================================
# Parte III: Resolviendo instancias del problema de la mochila
# ============================================================

# Damos aquí tres instancias concretas del problema de la mochila. Damos
# también sus soluciones optimas, para que se puedan comparar con los
# resultados obtenidos por el algoritmo genético:

# _______________________________________________________
# Problema de la mochila 1:
# 10 objetos, peso máximo 165
pesos1 = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
valores1 = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

# Solución óptima= [1, 1, 1, 1, 0, 1, 0, 0, 0, 0], con valor 309
# _______________________________________________________

# _______________________________________________________
# Problema de la mochila 2:
# 15 objetos, peso máximo 750

pesos2 = [70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120]
valores2 = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221,
            229, 240]

# Solución óptima= [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1] con valor 1458
# _______________________________________________________


# _______________________________________________________
# Problema de la mochila 3:
# 24 objetos, peso máximo 6404180

pesos3 = [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460,
          903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046,
          446298, 931161, 31385, 496951, 264724, 224916, 169684]
valores3 = [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457,
            1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277,
            2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257,
            369261]

# Solución óptima= [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
#                   0, 1, 1, 1]
# con valoración 13549094

# _______________________________________________________


# -----------
# Ejercicio 9
# -----------

# Definir variables m1g, m2g y m3g, referenciando a instancias de
# Problema_Genetico que correspondan, respectivamente, a los problemas de la
# mochila anteriores.

# Usar el algoritmo genético anterior para resolver estos problemas.

# Por ejemplo:

# >>> algoritmo_genetico_t(m1g,3,max,100,50,0.8,0.05)
# ([1, 1, 1, 1, 0, 1, 0, 0, 0, 0], 309)

# >>> algoritmo_genetico_t(m2g,3,max,100,50,0.8,0.05)
# ([1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0], 1444)
# >>> algoritmo_genetico_t(m2g,3,max,200,100,0.8,0.05)
# ([0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0], 1439)
# >>> algoritmo_genetico_t(m2g,3,max,200,100,0.8,0.05)
# ([1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1], 1458)

# >>> algoritmo_genetico_t(m3g,5,max,400,200,0.75,0.1)
# ([1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0], 13518963)
# >>> algoritmo_genetico_t(m3g,4,max,600,200,0.75,0.1)
# ([1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0], 13524340)
# >>> algoritmo_genetico_t(m3g,4,max,1000,200,0.75,0.1)
# ([1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], 13449995)
# >>> algoritmo_genetico_t(m3g,3,max,1000,100,0.75,0.1)
# ([1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], 13412953)
# >>> algoritmo_genetico_t(m3g,3,max,2000,100,0.75,0.1)
# ([0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 13366296)
# >>> algoritmo_genetico_t(m3g,6,max,2000,100,0.75,0.1)
# ([1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1], 13549094)


# =========== Solución:

m1g = Problema_Genetico([0, 1],
                        10,
                        lambda x: decodifica_mochila(x, 10, pesos1, 165),
                        lambda x: fitness_mochila(x, 10, pesos1, 165, valores1))

m2g = Problema_Genetico([0, 1],
                        15,
                        lambda x: decodifica_mochila(x, 15, pesos2, 750),
                        lambda x: fitness_mochila(x, 15, pesos2, 750, valores2))

m3g = Problema_Genetico([0, 1],
                        24,
                        lambda x: decodifica_mochila(x, 24, pesos3, 6404180),
                        lambda x: fitness_mochila(x, 24, pesos3, 6404180, valores3))

# ===================================
