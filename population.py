import random
from utils import *

'''

    Decision tree.
    Crear una estructura arbol de decision, que
    sera utilizada para tomar decisiones en el
    juego.


'''
class decider:
    def __init__(self, limits):
        self.feature = random.randint(0, len(limits) - 1)
        feat_min = limits[self.feature][0]
        feat_max = limits[self.feature][1]
        self.cmp_with = random.randint(feat_min, feat_max)
        self.test = random.randint(0, 1)
    
    def decide(self, X):
        if self.test == 1:
            return X[self.feature] >= self.cmp_with
        else:
            return X[self.feature] <= self.cmp_with

class decision_tree:
    def __init__(self, height, limits):
        #nodo hoja
        if height == 0:
            self.value = random.randint(0, 10)
            self.left = None
            self.right = None
            self.test = None
            self.height = height
        else:
            #nodo interno
            self.left = decision_tree(height - 1, limits)
            self.right = decision_tree(height - 1, limits)
            self.value = None
            self.test = decider(limits)
            self.height = height
    
    def decide(self, X):
        if self.test != None:
            if self.test.decide(X):
                return self.left.decide(X)
            else:
                return self.right.decide(X)
        else:
            return self.value

"""

    Genome.
    Crear un genoma con un tamaño dado, el cual
    contendra un conjunto de arboles de decision.

"""

class genome:
    def __init__(self, size, tree_heights, mutation_rate):
        self.genes = []
        self.size = size
        self.score = 0
        self.limits = get_features_limits()
        self.mutation_rate = mutation_rate
        self.tree_heights = tree_heights
    
    #inicializar el genoma con arboles de decision aleatorios
    def randomize(self):
        for i in range(0, self.size):
            self.genes.append(decision_tree(self.tree_heights, self.limits))


    #cruzar dos genomas
    def crossover(self, p1, p2):
        for _ in range(self.size):
            if random.randint(0, 1) == 0:
                self.genes.append(p1.genes[random.randint(0, self.size - 1)])
            else:
                self.genes.append(p2.genes[random.randint(0, self.size - 1)])

    def mutate(self):
        num_genes = len(self.genes)  # Obtener el número total de genes
        for i in range(num_genes):
            if random.random() < self.mutation_rate:  # Verificar si cada gen debe mutar
                mutation_type = random.choice(['increment', 'decrement', 'random', 'modify_tree'])  # Include 'modify_tree' as a mutation type
                if isinstance(self.genes[i], decision_tree):
                    if mutation_type == 'modify_tree':
                        self.genes[i] = decision_tree(self.tree_heights, self.limits) 
                else:
                    if mutation_type in ['increment', 'decrement', 'random']:
                        value = self.genes[i]
                        if i < len(self.limits):  # Check if index is within bounds for self.limits
                            if mutation_type == 'increment':
                                self.genes[i] = min(value + random.uniform(0.01, 0.1), self.limits[i][1])
                            elif mutation_type == 'decrement':
                                self.genes[i] = max(value - random.uniform(0.01, 0.1), self.limits[i][0])
                            elif mutation_type == 'random':
                                self.genes[i] = random.uniform(self.limits[i][0], self.limits[i][1])
    
    
    #la funcion de decidir
    def decide(self, X, allowed):
        choices = [0, 0, 0, 0]
        for i in range(0, self.size):
            decision = self.genes[i].decide(X)
            if decision < len(choices):
                choices[decision] += 1
        for i in range(0, 4):
            if not allowed[i]:
                choices[i] = -1
        #retornando el indice de la decision con mayor votacion
        return choices.index(max(choices))

"""
    Population
    poblacion de genomas, la cual se encarga de
    evolucionar a los genomas.

"""

class population:
    def __init__(self, size, genome_size, mutation_rate, tree_heights):
        self.size = size # tamaño de la poblacion
        self.cur = 0 # indice del genoma actual
        self.gen = 0 # generacion actual
        self.individuals = [] # individuos de la poblacion
        self.genome_size = genome_size # tamaño del genoma
        #crear individuos
        for _ in range(self.size):
            g = genome(genome_size, tree_heights, mutation_rate)
            g.randomize() #empieza con arboles de decision aleatorios
            self.individuals.append(g)#agregar individuo a la poblacion
    
    #avanzar al siguiente genoma
    def go_next(self):
        self.cur += 1 #indice aumenta
        #si se llega al final de la poblacion
        if self.cur >= self.size:
            self.cur = 0 #reiniciar el indice
            self.crossover() #cruzar los genomas
            self.mutate() #mutar los genomas
            self.gen += 1 #aumentar la generacion
        
    #seleccionar un genoma
    #elegir el de mejor puntaje con ruleta uniforme
    def select(self):
        # Calcular el puntaje total de todos los individuos en la población
        total_score = sum(ind.score for ind in self.individuals)
        # Si el puntaje total es 0 (todos tienen puntaje 0), elegir un individuo al azar
        if total_score == 0:
            return random.choice(self.individuals)
        
        # Elegir un número al azar entre 0 y el puntaje total
        pick = random.uniform(0, total_score)
        current = 0
        # Recorrer los individuos acumulando sus puntajes
        for ind in self.individuals:
            current += ind.score
            # Si el acumulado supera el número elegido, retornar ese individuo
            if current > pick:
                return ind
        
    #cruzar los genomas
    def crossover(self):
        new = [] #nueva poblacion

        #ordenar los individuos por puntaje
        self.individuals = sorted(self.individuals,
                key = lambda ind: ind.score,
                reverse = True)
        
        #cruzar los genomas
        for _ in range(self.size):
            p1 = self.select() 
            #asegurarse de que no se cruce consigo mismo
            while True:
                p2 = self.select()
                if p1 != p2:
                    break
            g = genome(self.genome_size, p1.tree_heights, p1.mutation_rate)
            g.crossover(p1, p2)
            new.append(g)
        self.individuals = new

    #mutar los genomas
    def mutate(self):
        for individual in self.individuals:
            individual.mutate()
    
    #obtener el genoma actual
    def get_cur(self):
        return self.individuals[self.cur]
    

