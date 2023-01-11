
# Evolución Diferencial en Python
 

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

[Documentacion](https://link)


El problema a resolver es el siguiente:
![problema_g05](https://github.com/Emanuel-TC/Computo-Evolutivo/blob/main/EvolucionDiferencial/Ejercicio5.jpeg?raw=true)


## Descripción de funciones

Función para generar una población, ya que el algoritmo de 
evolución diferencial comienza generando una población inicial de soluciones candidatas.

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
\
Y posteriormente evaluamos la a cada individuo generado 
con la función objetivo que se declara por el usuario:
```python
#Evaluamos cada individuo de la poblacion
    for index, vector in enumerate(poblacion):
        poblacion[index].append(funcion_objetivo(vector))
        poblacion[index].append(restricciones(vector))
```


