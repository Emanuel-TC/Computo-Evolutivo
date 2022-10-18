from numpy.random import rand
from numpy.random import choice
from numpy import asarray
from numpy import clip
from numpy import argmin
from numpy import min
from numpy import around


# definimos la función objetivo
def funcionObjetivo(x):
  return 0
  #return x[0]**2.0 + x[1]**2.0


# definimos la operación de mutación
def mutacion(x, F):
    return x[0] + F * (x[1] - x[2]) 
#el operador de mutacion consiste en una diferencia
		#aritmetica entre pares de vectores seleccionados aleatoriamente
        #normalnte F es 0<F>2


#################CON LIMITES#########################################################################
#                                                                                                   #
# definimos la operación de verificación de límites                                                 #
def revisarLimites(mutados, limites):                                                               #
    limiteMutado = [clip(mutados[i], limites[i, 0], limites[i, 1]) for i in range(len(limites))]    #
    return limiteMutado                                                                             #
#                                                                                                   #
##################CON LIMITES########################################################################

# definimos la operación de cruza
def cruza(vectoresMutados, target, cr, nVariablesDeEntrada): #cr es 0<= cr <= 1
    # generamos un valor aleatorio uniforme para variable de entrada
    p = rand(nVariablesDeEntrada)
    # generamos vector de target por cruza binomial
    trial = [vectoresMutados[i] if p[i] < cr else target[i] for i in range(nVariablesDeEntrada)]
    return trial
  
  
 
 def evolucion_diferencial(tamanio_de_poblacion, limites, iter, F, cr):
    # initialise population of candidate solutions randomly within the specified bounds
    poblacion = limites[:, 0] + (rand(tamanio_de_poblacion, len(limites)) * (limites[:, 1] - limites[:, 0]))
    
    # evaluar nuestra población inicial de soluciones candidatas
    solucionesCandidatas = [funcionObjetivo(poblacionInicial) for poblacionInicial in poblacion]
    
    #Encuentre el mejor vector de rendimiento de la población inicial.
    mejor_vector = poblacion[argmin(solucionesCandidatas)]
    mejor_obj = min(solucionesCandidatas)
    anterior_obj = mejor_obj
    # run iterations of the algorithm
    for i in range(iter):
        # iterate over all candidate solutions
        for j in range(tamanio_de_poblacion):
            
            # elegir tres candidatos, a, b y c, que no sean el actual
          candidatos = [candidato for candidato in range(tamanio_de_poblacion) if candidato != j]
          a, b, c = poblacion[choice(candidatos, 3, replace=False)]
            
            # realizar mutación
            mutados = mutacion([a, b, c], F)
            
            # check that lower and upper bounds are retained after mutation
            
            mutados = revisarLimites(mutados,limites)
            
            #Realizar cruza
            trial = cruza(mutados, poblacion[j], len(limites), cr)
            
              
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
                
                
                
        # find the best performing vector at each iteration
        #encontrar el vector de mejor rendimiento en cada iteración
        mejor_obj = min(solucionesCandidatas)
        # store the lowest objective function value
        if mejor_obj < anterior_obj:
            mejor_vector = poblacion[argmin(solucionesCandidatas)]
            prev_obj = mejor_obj
            # report progress at each iteration
            print('Iteration: %d f([%s]) = %.5f' % (i, around(mejor_vector, decimals=5), mejor_obj))
    return [mejor_vector, mejor_obj]

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
print('\nLa solucion de optimizar funcion es: f([%s]) = %.5f' % (around(solution[0], decimals=5), solucion[1]))