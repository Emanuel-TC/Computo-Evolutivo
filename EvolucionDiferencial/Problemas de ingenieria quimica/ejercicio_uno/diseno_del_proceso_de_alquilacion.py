import numpy as np
from numpy import *
import random
import math
from matplotlib import pyplot
# definimos la función objetivo.
def funcion_objetivo(x):
    c1 = 1.715
    c2 = 0.035
    c3 = 4.05665
    c4 = 10.000
    c5 = 3000.0
    c6 = 0.063
    resultado = c1*x[0] + c2*x[0]*x[5] + c3*x[2] + c4*x[1] + c5 - c6*x[2]*x[4]
    return resultado
def restricciones(x):
    c7 = 0.59553571 * (math.e -2)
    c8 = 0.88392857
    #0.13035330
    c9 = 1.10880000                 #c10
    c10 = 0.13035330                #c11
    c11 = 0.00660330  #c12
    c12 = 0.66173269 * (math.e -3)   #c13
    c13 = 0.17239878 * (math.e -1)   #c14
    c14 = 0.56595559 * (math.e -2)   #c15
    c15 = 0.19120592 * (math.e -1)   #c16
    c16 = 0.56850750 * (math.e +2)                 #c17
    c17 = 1.08702000                 #c18
    c18 = 0.32175000                 #c19
    c19 = 0.3762000                 #c20
    c20 = 0.00619800   #c21
    c21 = 0.24623121 * (math.e +4)   #c22
    c22 = 0.25125634 * (math.e +2)                    #c23
    c23 = 5000.0    #c24
    #c24
    c24 = 0.48951000 * (math.e +6)   #c25
    c25 = 0.44333333 * (math.e +2)                 #c26
    c26 = 0.33000000                 #c27
    c27 = 0.02255600                 #c28
    c28 = 0.00759500                #c29
    c29 = 0.00061000                     #c30
    c30 = 0.0005                  #c31
    c31 = 0.81967200                 #c32
    c32 = 0.81967200                  #c33
    c33 = 245000.0                       #c34
    c34 = 250.0   #c35
    c35 = 0.10204082 * (math.e- 1)   #c36
    c36 = 0.12244898 * (math.e- 4)                 #c37
    c37 = 0.00006250                 #c38
    c38 = 0.00007625
    r1 = max(0,c7 * (x[5]**2) + c8 * (x[0]**-1) * (x[2]) - c9 * (x[5]) -1)
    r2 = max(0,c10 * x[0] * (x[2]**-1) + c11 * x[0] * (x[2]**-1) + c12 * x[0] * (x[2]**-1) * (x[5]**2) -1)
    r3 = max(0,c13 * (x[5]**2) + c14 * x[4] - c15 * x[3] - c16 * x[5] -1)
    r4 = max(0,c17 * (x[4]**-1) + c18 * (x[4]**-1) * x[5] + c19 * x[3] * (x[4]**-1) - c20 * (x[4]**-1) * (x[5]**2) -1)
    r5 = max(0,c21 * x[6] + c22 * x[1] * (x[2]**-1) * (x[3]**-1) - c23 * x[1] * (x[2]**-1) -1)
    r6 = max(0,c24 * (x[6]**-1) + c25 * x[1] * (x[2]**-1) * (x[6]**-1) - c26 * x[1] * (x[2]**-1) * (x[3]**-1) * (x[6]**-1) -1)
    r7 = max(0,c27 * (x[4]**-1) + c28 * (x[4]**-1) * x[6] -1)
    r8 = max(0,c29 * x[4] - c30 * x[6] -1)
    r9 = max(0,c31 * x[2] - c32 * x[0] -1)
    r10 = max(0,c33 * x[0] * (x[2]**-1) + c34 * (x[2]**-1) -1)
    r11 = max(0,c35 * x[1] * (x[2]**-1) * (x[3]**-1) - c36 * x[1] * (x[2]**-1)  -1)
    r12 = max(0,c37 * x[3] + c38 * (x[1]**-1) * x[2] * x[3] -1)

    return r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + r12
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

tamanio_de_poblacion = 20
numero_de_iteraciones = 5000
F = 0.6
cr = 0.7
limites = np.array([[1500.0, 2000.0], [1.0, 120.0], [3000.0, 3500.0], [85.0, 93.0], [90.0, 95.0], [3.0, 12.0], [145.0, 162.0]])
solucion = evolucion_diferencial(tamanio_de_poblacion,limites,numero_de_iteraciones,F, cr)
print(f"El vector solucion es {solucion[0:-2]} y su valor de aptitud es {solucion[-2]}")
