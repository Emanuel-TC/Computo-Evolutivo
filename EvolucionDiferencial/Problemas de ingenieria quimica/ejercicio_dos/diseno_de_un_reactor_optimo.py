import numpy as np
from numpy import *
import random
import math
from matplotlib import pyplot
# definimos la función objetivo.
def funcion_objetivo(x):
    resultado = 0.4 * (x[0]**0.67) * (x[6]**-0.67) + 0.4 * (x[1]**0.67) * (x[7]**-0.67) + 10.0 - x[0] - x[1]
    return resultado
def restricciones(x):
    r1 = max(0, 0.0588 * x[4] * x[6] + 0.1 * x[0] -1)
    r2 = max(0, 0.0588 * x[5] * x[7] + 0.1 * x[0] + 0.1 * x[1] -1)
    r3 = max(0, 4 * x[2] * (x[4]**-1) + 2 * (x[2]**-0.71) * (x[4]**-1) + 0.0588 * (x[2]**-1.3) * x[6] -1)
    r4 = max(0, 4 * x[3] * (x[5]**-1) + 2 * (x[3]**-0.71) * (x[5]**-1) + 0.0588 * (x[3]**-1.3) * x[7]-1)

    return r1 + r2 + r3 + r4
def genera_poblacion(tamanio_de_poblacion, limites):
    poblacion = []  # creamos un arreglo vacio llamado poblacion
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
    # inicializar población
    poblacion = genera_poblacion(tamanio_de_poblacion, limites)
    grafica = []
    #Evaluamos cada individuo de la poblacion
    for index, vector in enumerate(poblacion):
        poblacion[index].append(funcion_objetivo(vector))
        poblacion[index].append(restricciones(vector))

    # ejecutar iteraciones del algoritmo
    i = 0
    while i in range(iteraciones):
        i += 1
        # iterar sobre todas las soluciones candidatas
        for j in range(tamanio_de_poblacion):
            # elegir tres candidatos, a, b y c, que no sean el actual
            vector_1, vector_2, vector_3 = random.choices(poblacion, k=3)

            # realizar mutación
            vector_mutado = mutacion(vector_1[0:-2],vector_2[0:-2],vector_3[0:-2],F)
            vector_mutado = ajusta_limites(vector_mutado, limites)

            # Procedemos a realizar la cruza
            vector_target = poblacion[j]
            vector_trial = cruza(vector_target[0:-2], vector_mutado, cr)

            #Evaluamos el nuevo vector, el vector trial
            vector_trial.append(funcion_objetivo(vector_trial))
            vector_trial.append(restricciones(vector_trial))

            # procedemos a realizar la seleccion
            if (vector_trial[-1] == 0) and (vector_target[-1] == 0): #si dos soluciones son factibles
                if vector_trial[-2] < vector_target[-2]: #se toma aquella con el valor aptitud deseado, en este caso, el menor
                    poblacion[j] = vector_trial
                    grafica.append(vector_trial[-2])
            elif (vector_trial[-1] != 0) and (vector_target[-1] != 0): #si dos soluciones no son factibles
                if vector_trial[-1] < vector_target[-1]: #se toma aquella con menor suma de violación de restricciones
                    poblacion[j] = vector_trial
                    grafica.append(vector_trial[-2])
            else:
                if (vector_trial[-1] == 0) and (vector_target[-1] != 0): #si una solucion es factible y la otra no
                    poblacion[j] = vector_trial #se toma la solución factible
                    grafica.append(vector_trial[-2])
    #se busca la mejor solución en la población mejorada
    mejor_vector = poblacion[0]
    for vector in poblacion:
        if vector[-2] < mejor_vector[-2]: #si el valor de aptitud del vector actual es menor al valor de aptitud del mejor vector
            mejor_vector = vector #mi mejor vector es el vector actual

    pyplot.plot(grafica, '.-')
    pyplot.xlabel('Evolución de solución')
    pyplot.ylabel('Evaluación de f(x)')
    pyplot.show()
    return mejor_vector

tamanio_de_poblacion = 30
numero_de_iteraciones = 5000
F = 0.7
cr = 0.6
                    #1            #2          #3           #4           #5          #6          #7          #8
limites = np.array([[0.1, 10.0], [0.1, 10.0],[0.1, 10.0], [0.1, 10.0], [0.1, 10.0], [0.1, 10.],[0.1, 10.0], [0.1, 10.0]])
solucion = evolucion_diferencial(tamanio_de_poblacion,limites,numero_de_iteraciones,F, cr)
print(f"El vector solucion es {solucion[0:-2]} y su valor de aptitud es {solucion[-2]}")