import copy
import random

class matrix_2048:
    #constructor
    def __init__ (self):
        self.WINCONDITION = 2048
        self.score = 0
        self.exponential_score = 0
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_number()
        self.add_number()
    
    #añadir un número aleatorio en una celda vacía
    def add_number(self):
        empty = []
        for i in range(4): #recorrer la matriz
            for j in range(4):
                if self.matrix[i][j] == 0: #si la celda está vacía
                    empty.append((i, j)) #añadir la celda a la lista de celdas vacías

        if not empty: #si no queda espacio, se acabo el juego
            return
        
        random_cell = random.choice(empty) #se elige una celda aleatoria de la lista de celdas vacías
        random_number = random.randint(0,9) #se elige un número aleatorio entre 0 y 1
        self.matrix[random_cell[0]][random_cell[1]] = 2 if random_number <= 8 else 4 #se añade un 2 o un 4 a la celda aleatoria

    # mover la matriz hacia arriba
    def up(self):
        old_matrix = copy.deepcopy(self.matrix)
        for j in range(4):
            column = [self.matrix[i][j] for i in range(4)]
            column = [x for x in column if x != 0]
            column += [0] * (4 - len(column))
            for i in range(3):
                if column[i] == column[i+1]:
                    column[i] *= 2
                    column[i+1] = 0
                    self.score += column[i]
                    self.exponential_score += 2 ** column[i]
            column = [x for x in column if x != 0]
            column += [0] * (4 - len(column))
            for i in range(4):
                self.matrix[i][j] = column[i]
        return old_matrix != self.matrix
    
    #mover la matriz hacia abajo
    def down(self):
        old_matrix = copy.deepcopy(self.matrix)
        for j in range(4):
            column = [self.matrix[i][j] for i in range(4)]
            column = [x for x in column if x != 0]
            column = [0] * (4 - len(column)) + column
            for i in range(3, 0, -1):
                if column[i] == column[i-1]:
                    column[i] *= 2
                    column[i-1] = 0
                    self.score += column[i]
                    self.exponential_score += 2 ** column[i]
            column = [x for x in column if x != 0]
            column = [0] * (4 - len(column)) + column
            for i in range(4):
                self.matrix[i][j] = column[i]
    
        return old_matrix != self.matrix
    
    #mover la matriz hacia la izquierda
    def left(self):
        old_matrix = copy.deepcopy(self.matrix)
        for i in range(4):
            row = self.matrix[i]
            row = [x for x in row if x != 0]
            row += [0] * (4 - len(row))
            for j in range(3):
                if row[j] == row[j+1]:
                    row[j] *= 2
                    row[j+1] = 0
                    self.score += row[j]
                    self.exponential_score += 2 ** row[j]
            row = [x for x in row if x != 0]
            row += [0] * (4 - len(row))
            self.matrix[i] = row
    
        return old_matrix != self.matrix
    
    #mover la matriz hacia la derecha
    def right(self):
        old_matrix = copy.deepcopy(self.matrix)
        for i in range(4):
            row = self.matrix[i]
            row = [x for x in row if x != 0]
            row = [0] * (4 - len(row)) + row
            for j in range(3, 0, -1):
                if row[j] == row[j-1]:
                    row[j] *= 2
                    row[j-1] = 0
                    self.score += row[j]
                    self.exponential_score += 2 ** row[j]
            row = [x for x in row if x != 0]
            row = [0] * (4 - len(row)) + row
            self.matrix[i] = row
        
        return old_matrix != self.matrix
    
    #el agente de inteligencia artificial debe ser capaz de obtener el estado actual del juego
    def get_state(self):
        #retornar la matriz
        return self.matrix
    
    #el agente debe conocer el puntaje actual del juego
    #que se calcula como el mayor número en la matriz
    def get_max_value(self):
        return max([max(row) for row in self.matrix])
    
    def get_score(self):
        return self.score
    
    def get_exponential_score(self):
        return self.exponential_score
    
    #suma de toda la matriz
    def sum_matrix(self):
        return sum([sum(row) for row in self.matrix])
    
    # el agente debe ser capaz de saber si el juego ha terminado
    # True si ha ganado, False si ha perdido, None si no ha terminado
    def game_over(self):
        if self.get_max_value() >= self.WINCONDITION:
            return True
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    return None
                if i < 3 and self.matrix[i][j] == self.matrix[i+1][j]:
                    return None
                if j < 3 and self.matrix[i][j] == self.matrix[i][j+1]:
                    return None
        return False
    
    def print_matrix(self):
        for row in self.matrix:
            print(row)
    
    #se puede probar un movimiento sin cambiar la matriz
    #y se retorna la matriz resultante
    def try_step(self, move):
        new_matrix = copy.deepcopy(self)
        if move == 'up': new_matrix.up()
        elif move == 'down': new_matrix.down()
        elif move == 'left': new_matrix.left()
        elif move == 'right': new_matrix.right()
        else: return None
        
        return new_matrix.get_state()
    
    #resetear
    def restart(self):
        self.score = 0
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_number()
        self.add_number()
    