import random
import os
import json
from genetico.utils import *

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
    
    def to_dict(self):
        if self.test is not None:
            return {
                "feature": self.test.feature,
                "cmp_with": self.test.cmp_with,
                "test": self.test.test,
                "left": self.left.to_dict(),
                "right": self.right.to_dict(),
                "height": self.height
            }
        else:
            return {
                "value": self.value,
                "height": self.height
            }

    def save_tree(self, filename):
        tree_dict = self.to_dict()
        with open(filename, 'w') as file:
            json.dump(tree_dict, file, indent=4)

    @staticmethod
    def load_tree(filename):
        with open(filename, 'r') as file:
            tree_dict = json.load(file)
        
        def dict_to_tree(d):
            if "value" in d:
                node = decision_tree(0, [])
                node.value = d["value"]
                node.height = d["height"]
                return node
            else:
                node = decision_tree(d["height"], [])
                node.test = decider([])
                node.test.feature = d["feature"]
                node.test.cmp_with = d["cmp_with"]
                node.test.test = d["test"]
                node.left = dict_to_tree(d["left"])
                node.right = dict_to_tree(d["right"])
                return node
        
        return dict_to_tree(tree_dict)

    @staticmethod
    def from_dict(tree_dict, limits):
        if "value" in tree_dict:
            # It's a leaf node
            node = decision_tree(0, limits)
            node.value = tree_dict["value"]
        else:
            # It's an internal node
            height = tree_dict["height"]
            node = decision_tree(height, limits)
            node.test = decider(limits)
            node.test.feature = tree_dict["feature"]
            node.test.cmp_with = tree_dict["cmp_with"]
            node.test.test = tree_dict["test"]
            node.left = decision_tree.from_dict(tree_dict["left"], limits)
            node.right = decision_tree.from_dict(tree_dict["right"], limits)
        node.height = tree_dict.get("height", 0)  # Ensure height is set for both leaf and internal nodes
        return node

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
    
    def to_dict(self):
        return {
            'size': self.size,
            'score': self.score,
            'limits': self.limits,
            'mutation_rate': self.mutation_rate,
            'tree_heights': self.tree_heights,
            'genes': [tree.to_dict() for tree in self.genes]
        }
    
    @staticmethod
    def from_dict(genome_dict):
        g = genome(genome_dict['size'], genome_dict['tree_heights'], genome_dict['mutation_rate'])
        g.score = genome_dict['score']
        g.limits = genome_dict['limits']
        # Inside genome.from_dict method
        g.genes = [decision_tree.from_dict(tree_dict, g.limits) for tree_dict in genome_dict['genes']]
        return g

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
    

    def save_population(self, filename):
        population_dict = {
            'size': self.size,
            'cur': self.cur,
            'gen': self.gen,
            'genome_size': self.genome_size,
            'individuals': [ind.to_dict() for ind in self.individuals]
        }
        with open(filename, 'w') as file:
            json.dump(population_dict, file, indent=4)


    def load_population(self, filename):
        print ("Cargando la población...")
        with open(filename, 'r') as file:
            population_dict = json.load(file)
        
        self.size = population_dict['size']
        self.cur = population_dict['cur']
        self.gen = population_dict['gen']
        self.genome_size = population_dict['genome_size']
        total = len(population_dict['individuals'])
        for i, ind in enumerate(population_dict['individuals'], start=1):
            self.individuals.append(genome.from_dict(ind))
            print(f"{i}/{total}")        # print(self.individuals)

