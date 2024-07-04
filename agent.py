#agente para que aprenda a jugar 2048

# acciones: arriba, abajo, izquierda, derecha
# estado: matriz 4x4 con los valores actuales,
#       la puntuación actual y la puntuación máxima
#       
#recompensa: puntaje total de las celdas que se unieron
#           en la última acción
#
#restricciones: no se permiten movimientos que no cambien
#               la matriz
#               no se permiten movimientos inválidos
#
#objetivo: obtener el mayor puntaje posible
#
# output: 4 acciones y elegir la mejor

import torch
import numpy
import random
from matrix import matrix_2048
from collections import deque
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 #random
        self.gamma = 0.9 #tasa de descuento
        self.memory = deque(maxlen=MAX_MEMORY)
        #inputs son 16 valores de la matriz y la puntuación
        #outputs son 4 valores para las 4 acciones
        self.model = Linear_QNet(17, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    
    def get_state(self, game):
        #retornar el estado actual del juego
        #la matriz 4x4 con los valores actuales
        #la puntuación actual
        
        matrix = game.get_matrix()
        score = game.get_score()
        #make the matrix an array
        state = numpy.array(matrix).flatten()
        state = numpy.append(state, score)
        return state


    def remember(self, state, action, reward, next_state, gameover):
        self.memory.append((state, action, reward, next_state, gameover))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, gameovers = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, gameovers)


    def train_short_memory(self, state, action, reward, next_state, gameover):
        self.trainer.train_step(state, action, reward, next_state, gameover)

    def get_action(self, state):
        #random moves: tradeoff entre la exploracion y la explotación
        self.epsilon = 80 - self.number_of_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
        

