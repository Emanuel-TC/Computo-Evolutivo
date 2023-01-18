# Evolución Diferencial en Python
 
La Evolución Diferencial (ED) es un método de optimización 
perteneciente a la categoría de computación evolutiva, 
aplicado en la resolución de problemas complejos. 
Al igual que otros algoritmos de esta categoría, la ED 
mantiene una población de soluciones candidatas, las 
cuales se recombinan y mutan para producir nuevos 
individuos los cuales serán elegidos de acuerdo al 
valor de su función de desempeño. 
Lo que caracteriza a la ED es el uso de vectores de 
prueba, los cuales compiten con los individuos de la 
población actual a fin de sobrevivir.

En el siguiente archivo desarrollo en python una
solución de minimzación con restricciones a un 
problema matemático mediante el algoritmo de 
evolución diferencial. 
Cabe mencionar que se espera desarrollar una base 
para implementar el algoritmo en sus diversas formas 
y que trabaje de forma general para resolver 
cualquier problema. 
A continuación explico cómo se han implementado 
sus funciones.

## Autor

- [@Emanuel-TC](https://github.com/Emanuel-TC)



## Documentación

El problema a resolver es el siguiente:
![problema_g05](https://github.com/Emanuel-TC/Computo-Evolutivo/blob/main/EvolucionDiferencial/Ejercicio5.jpeg?raw=true)
## Descripción del desarrollo en python
El algoritmo comienza iniciando aleatoriamente una población de vectores de 
decisión de valor real, también conocidos como genomas o cromosomas. 
Estos representan las soluciones candidatas al problema de optimización 
multidimensional.

Crearemos una función general llamada *evolucion_diferencial*, la cual la definimos así:
```python
def evolucion_diferencial(tamanio_de_poblacion, limites, iteraciones, F, cr):
```
La  función requiere que se le ingrese un valor entero de acuerdo al tamaño de la población;
los límites del problema, estos en forma de un arreglo de las dimensiones que el usuario prefiera;
el número de iteraciones que quiere que el algoritmo ejecute; el factor de escala de mutación *F*, dentro
de un valor de 0.0 a 1.0 y finalmente, la tasa de cruza, dentro del mismo rango que el elemento anterior.
/

Comenzando con el desarrollo de este trabajo, se crea una función para generar una población inicial de soluciones candidatas.

```python
  def genera_poblacion(tamanio_de_poblacion, limites):
    poblacion = []  # creamos un arreglo vació llamado poblacion
    for i in range(0,tamanio_de_poblacion):  # definimos el número de vectores a crear, en este caso, siempre lo define el tamanio de la poblacion
        vector = []
        for j in range(len(limites)):  # definimos el número de columnas o bien, dimension del vector
            vector.append(random.uniform(limites[j][0], limites[j][1]))  # lo llenamos con un valor flotante entre el limite inferior y el limite superior, iterando en cada índice de los limites designados
        poblacion.append(vector)  # y lo añadimos al arreglo
    return poblacion
```
Creamos un arreglo donde mandamos llamar la función anterior de la siguiente forma:
```python
    poblacion = genera_poblacion(tamanio_de_poblacion, limites)
```
\
Y posteriormente evaluamos la a cada individuo generado 
con la función objetivo y las restricciones que se declaran por el usuario:
```python
#Evaluamos cada individuo de la poblacion
    for index, vector in enumerate(poblacion):
        poblacion[index].append(funcion_objetivo(vector))
        poblacion[index].append(restricciones(vector))
```

Ahora el algoritmo comenzará a trabajar en un ciclo dentro el 
rango de las iteraciones que sean designadas por el usuario:
```python
    i = 0
    while i in range(iteraciones):
        i+=1
```
Dentro de cada iteración, habrá un ciclo del tamaño de la población:
```python
        # iterar sobre todas las soluciones candidatas
        for j in range(tamanio_de_poblacion):
```
Y aquí comienzan a operar los elementos de ED.

Se eligen tres vectores aleatorios que no sean el que se está iterando actualmente:
```python
            # elegir tres candidatos, a, b y c, que no sean el actual
            vector_1, vector_2, vector_3 = random.choices(poblacion, k=3)
```
El proceso de mutación entra en acción haciendo uso de los vectores seleccionados previamente.
Para ello se ha creado una función llamada *mutación* y la definimos de la siguiente forma:
```python
def mutacion(vector_uno, vector_dos, vector_tres,F):
    # El proceso de mutación lo realizamos por partes:
    # primero la resta de x2-x3
    resta_x = [vector_dos_i - vector_tres_i for vector_dos_i, vector_tres_i in zip(vector_dos, vector_tres)]
    # luego lo multiplicamos por el factor de mutacion F, y le sumamos el vector x1
    vector_mutado = [vector_uno_i + F * resta_x_i for vector_uno_i, resta_x_i in zip(vector_uno, resta_x)]
    return vector_mutado
```
Y dentro de la función de ED la usamos de la siguiente forma:
```python
            vector_mutado = mutacion(vector_1[0:4],vector_2[0:4],vector_3[0:4],F)
```
Podemos observar que creamos un nuevo vector pero que definimos como *vector_mutado*, posteriormente usaremos 
este vector para la siguiente etapa del algoritmo.

Pero antes es necesario verificar que el nuevo vector esté dentro de los límites establecidos, ya que debido al 
factor de mutación si fue mutado parcial o totalmente, entonces es probable que su valores hayan cambiado y 
por lo tanto, posiblemente se salga de los límites que se establecieron, por lo que usaremos una función auxiliar 
que nos permite ajustar los valores del vector siempre y cuando estén fuera de los límites.

```python
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
```
La función establece que se revisará cada valor del vector, y mientras el valor que se está revisando actualmente está 
por fuera de los límites ya sean los superiores o los inferiores, se realizará una operación de ajuste hasta que ya no cumpla 
con la sentencia anterior, para que finalmente se devuelva el vector ajustado.

Dentro de nuestra función de ED la usamos así:
```python
            vector_mutado = ajusta_limites(vector_mutado, limites)
```
Luego declaramos que el vector padre, o *target*, es el vector actual:
```python
            vector_target = poblacion[j]
```

Continuando con el algoritmo, pasamos a la etapa de cruza, y de la misma manera, se ha creado una función que realice este proceso.
 ```python
def cruza(vector_target, vector_mutado,cr):
    vector_trial = []
    # se realizará por cada elemento del vector target
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
```
Para esta función vamos a usar los elementos que hemos generado previamente, el más reciente, el vector target, el vector mutado,
y un elemento nuevo, pero que es definido por el usuario en la función de ED, la tasa de cruza, o bien, *cr*
Cabe mencionar que, para la cruza se crea un nuevo vector, llamado, vector hijo, o bien, vector *trial*,
el cual será prodructo, como se puede inferir de generar una cruza entre dos vectores, el vector mutado y el vector padre.

Este función básicamente define que, la cruza ocurre cuando el valor generado aleatoriamente es menor
igual al valor de la tasa de cruza. En ese caso, para ese valor del vector hijo se le asigna el valor que tiene en esa misma
posición el vector mutado, de lo contrario, se asigna el valor de la misma posición, pero dle vector padre.

Ya pasando nuevamente a la función de ED, lo usaremos de la siguiente forma:

 ```python
            vector_trial = cruza(vector_target[0:4], vector_mutado, cr)
            vector_trial.append(funcion_objetivo(vector_trial))
            vector_trial.append(restricciones(vector_trial))
```
En donde creamos la variable que almacenará a nuestro vector hijo, y le asignamos los valores que pide
la función de cruza. Es menester mencionar que se define el vector tarjet en un rango de sus parámetros, ya que,
la variable ha sido evaluada con la funcón objetivo y sus restricciones.

Finalmente, evaluamos el vector hijo igualmente con la función objetivo y las restricciones, para dar pie a la última fase del algoritmo.

Para la selección se consideran las reglas de Deb, las cuales indican que:
1. Entre dos soluciones factibles, se elige como mejor solución a la que tenga el valor más bajoen su función objetivo (cuando el problema es de minimización).

2. Entre una solución factible y otra infactible, la mejor solución es la factible.

3. Entre dos soluciones infactibles la mejor será aquella con la menor suma de violaciones de las restricciones.

Entonces, en nuestro programa lo declaramos de la siguiente forma:

```python
            if (vector_trial[5] == 0) and (vector_target[5] == 0): #si las restricciones de trial son iguales a 0 y las restricciones del vector target son iguales a0
                if vector_trial[4] < vector_target[4]: #si el valor de aptitud de trial es menor al de target
                    poblacion[j] = vector_trial #añade a la poblacion el vector trial
            elif (vector_trial[5] != 0) and (vector_target[5] != 0): #si dos soluciones no son factibles
                if vector_trial[5] < vector_target[5]:
                    poblacion[j] = vector_trial
            else:
                if (vector_trial[5] == 0) and (vector_target[5] != 0):
                    poblacion[j] = vector_trial
```
Después, obtenemos el mejor vector que se ha generado con el algoritmo de la siguiente forma:

```python
    mejor_vector = poblacion[0]
    for i in poblacion:
        if i[-2] < mejor_vector[-2]:
            mejor_vector = i

    return mejor_vector
```
 Finalmente tenemos el desarrollo de todo el algoritmo en el siguiente apartado:


```python
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
```
