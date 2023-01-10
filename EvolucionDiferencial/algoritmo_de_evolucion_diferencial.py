#Autor: Emanuel Rodríguez
import numpy as np
from numpy import *
import random
# definimos la función objetivo.
def funcion_objetivo(x):
    resultado = 3 * x[0] + 0.000001 * x[0] ** 3 + 2 * x[1] + (0.000002 / 3) * x[1] ** 3
    return resultado
def restricciones(vector):
    g1 = max(0, -vector[3] + vector[2] - 0.55)
    g2 = max(0, -vector[2] + vector[3] - 0.55)
    h3 = max(0, 1000 * math.sin(-vector[2] - 0.25) + 1000 * math.sin(-vector[3] - 0.25) + 894.8 - vector[0])
    h4 = max(0, 1000 * math.sin(vector[2] - 0.25) + 1000 * math.sin(vector[2] - vector[3] - 0.25) + 894.8 - vector[1])
    h5 = max(0, 1000 * math.sin(vector[3] - 0.25) + 1000 * math.sin(vector[3] - vector[2] - 0.25) + 1294.8)
    return g1 + g2 + h3 + h4 +h5
def genera_poblacion(tamanio_de_poblacion, limites):
    poblacion = []  # creamos un arreglo vació llamado poblacion
    for i in range(0,tamanio_de_poblacion):  # definimos el número de vectores a crear, en este caso, siempre lo define el tamanio de la poblacion
        vector = []
        for j in range(len(limites)):  # definimos el número de columnas o bien, dimension del vector
            vector.append(random.uniform(limites[j][0], limites[j][1]))  # lo llenamos con un valor flotante entre el limite inferior y el limite superior, iterando en cada índice de los limites designados
        poblacion.append(vector)  # y lo añadimos al arreglo
    return poblacion
def ajusta_limites(vector_mutado,limites):
    for i in range(len(vector_mutado)):
        while vector_mutado[i] < limites[i][0] or vector_mutado[i] > limites[i][1]:
            # si la variable excede los límites inferiores
            if vector_mutado[i] < limites[i][0]:
                vector_mutado[i] = limites[i][0] * 2 - vector_mutado[i]

            # si la variable excede los limites superiores
            if vector_mutado[i] > limites[i][1]:
                vector_mutado[i] = limites[i][1] * 2 - vector_mutado[i]
    return vector_mutado
def mutacion(vector_uno, vector_dos, vector_tres,F):
    # El proceso de mutación lo realizamos por partes:
    # primero la resta de x2-x3
    resta_x = [vector_dos_i - vector_tres_i for vector_dos_i, vector_tres_i in zip(vector_dos, vector_tres)]
    # luego lo multiplicamos por el factor de mutacion F, y le sumamos el vector x1
    vector_mutado = [vector_uno_i + F * resta_x_i for vector_uno_i, resta_x_i in zip(vector_uno, resta_x)]
    return vector_mutado
def cruza(vector_target, vector_mutado,cr):
    vector_trial = []
    # se realizará por cada elemento del vector tarjet
    for k in range(len(vector_target)):
        cruza = random.random()
        # el proceso de cruza ocurre cuando el valor generado aleatoriamente es menor
        # o igual al valor de la tasa de cruza
        if cruza <= cr:
            vector_trial.append(vector_mutado[k])

        # si no es así, entonces no se hace la cruza
        else:
            vector_trial.append(vector_target[k])
    return vector_trial

def evolucion_diferencial(tamanio_de_poblacion, limites, iteraciones, F, cr):
    # lo primero que se debe hacer es crear una población con valores aleatorios:
    # lo podemos hacer con el siguiente código:
    poblacion = genera_poblacion(tamanio_de_poblacion, limites)

    #Evaluamos cada individuo de la poblacion
    for index, vector in enumerate(poblacion):
        poblacion[index].append(funcion_objetivo(vector))
        poblacion[index].append(restricciones(vector))
        #print(vector)
    # ejecutar iteraciones del algoritmo
    i = 0
    vectores_candidatos = []
    while i in range(iteraciones):
        i += 1
        # iterar sobre todas las soluciones candidatas
        for j in range(tamanio_de_poblacion):
            # elegir tres candidatos, a, b y c, que no sean el actual
            #vectores_candidatos = [vector for vector in range(tamanio_de_poblacion) if vector != j]

            vector_1, vector_2, vector_3 = random.choices(poblacion, k=3)
            #print(vector_1)
            # realizar mutación
            vector_mutado = mutacion(vector_1[0:4],vector_2[0:4],vector_3[0:4],F)
            #print(f"El vector mutado {j}: {vector_mutado}")
            #Corroboramos que los limites estén dentro de los rangos establecidos
            #de los contrario se le aplica una modificación para controlar los limites
            vector_mutado = ajusta_limites(vector_mutado, limites)
            #print(f"El vector mutado corregido {j} es {vector_mutado}")
            # Procedemos a realizar la cruza
            vector_target = poblacion[j]
            #print(f"El vector target es: {vector_target}")
            vector_trial = cruza(vector_target[0:4], vector_mutado, cr)
            #print(f"El vector trial al realizar la cruza es: {vector_trial}")
            vector_trial.append(funcion_objetivo(vector_trial))
            vector_trial.append(restricciones(vector_trial))
            #print(f"El resultado de evaluar el vector trial es: {vector_trial}")

            # procedemos a realizar la seleccion

            if (vector_trial[5] == 0) and (vector_target[5] == 0): #si las restricciones de trial son iguales a 0 y las restricciones del vector target son iguales a0
                if vector_trial[4] < vector_target[4]: #si el valor de aptitud de trial es menor al de target
                    poblacion[j] = vector_trial #añade a la poblacion el vector trial
            elif (vector_trial[5] != 0) and (vector_target[5] != 0): #si dos soluciones no son factibles
                if vector_trial[5] < vector_target[5]:
                    poblacion[j] = vector_trial
            else:
                if (vector_trial[5] == 0) and (vector_target[5] != 0):
                    poblacion[j] = vector_trial
    best = poblacion[0]
    for i in poblacion:
        if i[-2] < best[-2]:
            best = i

    return best



tamanio_de_poblacion = 30
numero_de_iteraciones = 1000
F = 0.8
cr = 0.7
limites = np.array([[0.0, 1200.0], [0.0, 1200.0], [-0.55, 0.55], [-0.55, 0.55]])
solucion = evolucion_diferencial(tamanio_de_poblacion,limites,numero_de_iteraciones,F, cr)
print(f"El vector solucion es {solucion[0:4]} y su valor de aptitud es {solucion[4]}")
