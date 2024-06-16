import copy
import random

class matrix_2048:
    #constructor
    def __init__ (self):
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
        random_number = random.randint(0,1) #se elige un número aleatorio entre 0 y 1
        self.matrix[random_cell[0]][random_cell[1]] = 2 if random_number == 0 else 4 #se añade un 2 o un 4 a la celda aleatoria

    #mover la matriz hacia arriba
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
            row = [x for x in row if x != 0]
            row = [0] * (4 - len(row)) + row
            self.matrix[i] = row
    
        return old_matrix != self.matrix
    
    #el agente de inteligencia artificial debe ser capaz de obtener el estado actual del juego
    def get_matrix(self):
        #retornar la matriz
        return self.matrix
    
    #el agente debe conocer el puntaje actual del juego
    #que se calcula como el mayor número en la matriz
    def get_score(self):
        return max([max(row) for row in self.matrix])
    
    #el agente debe ser capaz de saber si el juego ha terminado
    def game_over(self):
        if self.get_score() == 2048:
            return True
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    return False
                if i < 3 and self.matrix[i][j] == self.matrix[i+1][j]:
                    return False
                if j < 3 and self.matrix[i][j] == self.matrix[i][j+1]:
                    return False
        return True

    #checar si el movimiento es legal, se pasa
    #el movimiento y se retorna bool
    def is_legal(self, movement):
        old_matrix = copy.deepcopy(self.matrix)
        movement()
        legal = old_matrix != self.matrix
        self.matrix = old_matrix
        return legal
    
    def print_matrix(self):
        for row in self.matrix:
            print(row)
    
    #funcion de movimiento que llamara el agente con
    #la decision. Debe retornar recompensa, gameover y puntaje
    def play_step(self, direction):
        movement = None
        reward = 0
        gameover = False
        #direction = [0,0,0,0] con un 1 en la dirección
        if direction[0]:
            movement = self.up
        elif direction[1]:
            movement = self.down
        elif direction[2]:
            movement = self.left
        elif direction[3]:
            movement = self.right
        
        if movement:
            if self.is_legal(movement):
                reward = self.get_reward(movement)
                movement()
                self.add_number()
                gameover = self.game_over()
        return reward, gameover, self.get_score()


    def get_reward(self, movement):
        # Guardar el estado actual de la matriz antes del movimiento
        old_matrix = [row[:] for row in self.matrix]

        # Realizar el movimiento
        movement()

        # Calcular la recompensa basada en las diferencias entre las matrices
        reward = 0
        moved_but_not_merged = 0
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] != old_matrix[i][j]:
                    # Si la celda en la nueva matriz es mayor, se combinaron celdas
                    if self.matrix[i][j] > old_matrix[i][j]:
                        reward += self.matrix[i][j] - old_matrix[i][j]
                    # Si una celda se movió pero su valor no está en la matriz antigua, se movió pero no se fusionó
                    elif self.matrix[i][j] > 0 and not any(self.matrix[i][j] in row for row in old_matrix):
                        moved_but_not_merged += 1

        # Restar las celdas movidas pero no fusionadas del reward
        reward -= moved_but_not_merged

        # Penalizar si la matriz no cambió
        if old_matrix == self.matrix:
            reward = -100
        # Restaurar la matriz al estado original antes del movimiento
        self.matrix = old_matrix

        return reward

    def restart(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_number()
        self.add_number()