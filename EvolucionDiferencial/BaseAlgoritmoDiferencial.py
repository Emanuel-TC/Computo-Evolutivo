from numpy.random import rand
from numpy.random import choice
from numpy import asarray
from numpy import clip
from numpy import argmin
from numpy import min
from numpy import around


# definimos la función objetivo
def funcionObjetivo(x):
  #return 0
  return x[0]**2.0 + x[1]**2.0


# definimos la operación de mutación
def mutacion(x, F):
    return x[0] + F * (x[1] - x[2]) 
#el operador de mutacion consiste en una diferencia
		#aritmetica entre pares de vectores seleccionados aleatoriamente
        #normalnte F es 0<F>2


#################CON LIMITES#########################################################################                                                                                                  
def revisarLimites(vectores_mutados, limites):                                                               
    limiteMutado = [clip(vectores_mutados[i], limites[i, 0], limites[i, 1]) for i in range(len(limites))]    
    return limiteMutado                                                                             
                                                                                                   
##################CON LIMITES########################################################################

# definimos la operación de cruza
def cruza(vectoresMutados, target, cr, nVariablesDeEntrada): #cr es 0<= cr <= 1
    # generamos un valor aleatorio uniforme para variable de entrada
    p = rand(nVariablesDeEntrada)
    # generamos vector de target por cruza binomial
    trial = [vectoresMutados[i] if p[i] < cr else target[i] for i in range(nVariablesDeEntrada)]
    return trial
  
  
def evolucion_diferencial(tamanio_de_poblacion, limites, iter, F, cr):
    # inicializar la población aleatoria de soluciones candidatas dentro de los límites especificados
    poblacion = limites[:, 0] + (rand(tamanio_de_poblacion, len(limites)) * (limites[:, 1] - limites[:, 0]))
    
    # evaluar nuestra población inicial de soluciones candidatas
    solucionesCandidatas = [funcionObjetivo(poblacionInicial) for poblacionInicial in poblacion]
    
    #Encuentre el mejor vector de rendimiento de la población inicial.
    mejor_vector = poblacion[argmin(solucionesCandidatas)]
    mejor_obj = min(solucionesCandidatas)
    anterior_obj = mejor_obj
    
    
    #  ejecutar iteraciones del algoritmo
    for i in range(iter):
        # iterar sobre todas las soluciones candidatas
        for j in range(tamanio_de_poblacion): 
            # elegir tres candidatos, a, b y c, que no sean el actual
            candidatos = [candidato for candidato in range(tamanio_de_poblacion) if candidato != j]
            a, b, c = poblacion[choice(candidatos, 3, replace=False)]
            
            # realizar mutación
            vectores_mutados = mutacion([a, b, c], F)
            
            # comprobamos que los límites inferior y superior se conservan después de la mutación
            vectores_mutados = revisarLimites(vectores_mutados,limites)
            
            #Realizar cruza
            trial = cruza(vectores_mutados, poblacion[j], len(limites), cr)
              
            # calcular el valor de la función objetivo para el vector objetivo
            vectorObjetivo = funcionObjetivo(poblacion[j])
            # calcular el valor de la función objetivo para el vector de prueba
            vectorPrueba = funcionObjetivo(trial)
            # realizar selección
            if vectorPrueba < vectorObjetivo:
                # reemplace el vector objetivo con el vector de prueba
                poblacion[j] = trial
                # almacenar el nuevo valor de la función objetivo
                solucionesCandidatas[j] = vectorPrueba
                
        #encontrar el vector de mejor rendimiento en cada iteración
        mejor_obj = min(solucionesCandidatas)
        # store the lowest objective function value
        if mejor_obj < anterior_obj:
            mejor_vector = poblacion[argmin(solucionesCandidatas)]
            anterior_obj = mejor_obj
            # report progress at each iteration
            print('Iteracion: %d f([%s]) = %.5f' % (i, around(mejor_vector, decimals=5), mejor_obj))
    return [mejor_vector, mejor_obj]

###########################################Evolucion Diferencial##############################################

# define population size
tamanio_de_poblacion = 10
# define lower and upper bounds for every dimension
limites = asarray([(-5.0, 5.0), (-5.0, 5.0)])
# define number of iterations
iter = 100
# define scale factor for mutation
F = 0.5
# define crossover rate for recombination
cr = 0.7

# perform differential evolution
solucion = evolucion_diferencial(tamanio_de_poblacion, limites, iter, F, cr)
print('\nLa solucion de optimizar funcion es: f([%s]) = %.5f' % (around(solucion[0], decimals=5), solucion[1]))