from matrix import matrix_2048
import copy
import numpy as np
import random


snake_weight = np.array([[ 10,   8,    7,    6.5], # Se define la matriz de pesos
                         [ 0.5,  0.7,  1,    3],
                         [-0.5, -1.5, -1.8, -2],
                         [-3.8, -3.7, -3.5, -3]])

number_of_rollouts = 50 #number_of_rollouts define la cantidad de simulaciones realizadas para cada movimiento
avg_evaluations = 0 #avg_evaluations define si se promedia el valor de las simulaciones
eval_function = 1 #eval_function define la función de evaluación, 0 es el puntaje, 1 es la suma de la matriz, 2 es la heurística
allow_random = True #allow_random define si se permite realizar movimientos aleatorios
random_factor = 0.1 #random_factor define la probabilidad de realizar un movimiento aleatorio

class MCTS2048:
    def __init__(self, initial_state):
        self.initial_state = initial_state
    
    def heuristic(self, state): #Función heurística que evalúa el estado del juego
        state_np = np.array(state)
        heuristic_value = np.sum(state_np * snake_weight)
        return heuristic_value

    def heuristic_search(self, state):
        moves = ['up', 'down', 'left', 'right'] #Se definen las direcciones posibles
        heuristic_values = [] #Lista de valores heurísticos
        for move in moves: #Se recorren las direcciones
            new_state = state.try_step(move) #Se prueba el movimiento
            old_state = state.get_state() #Se obtiene el estado actual
            if new_state != old_state: #Si el movimiento es válido
                heuristic_values.append(self.heuristic(new_state)) #Se agrega el valor heurístico
            else: #Si el movimiento no es válido
                heuristic_values.append(float('-inf'))  #Se agrega un valor negativo
        
        best_value = max(heuristic_values) #Se obtiene el mejor valor heurístico
        best_index = heuristic_values.index(best_value) #Se obtiene el índice del mejor valor

        if random.random() <= random_factor and allow_random:
            best_index = random.randint(0, 3) #Se selecciona un movimiento aleatorio
        
        return best_index if best_value != float('-inf') else -1        
    
    def init_algorithm(self, game):
        while game.game_over() is None:
            ####
            #game.print_matrix()
            #print(" ")
            ### 
            directions = ['up', 'down', 'left', 'right'] #Se definen las direcciones posibles
            best_move = None #Indice del mejor movimiento
            best_rollout_eval = float('-inf') #Mejor evaluación de las simulaciones

            for move in directions: #Se recorren las direcciones
                game_copy = copy.deepcopy(game) #Copia del juego

                if getattr(game_copy, move)(): #Si el movimiento es válido
                    rollout_eval = 0 #Evaluación de las simulación específica

                    for i in range(number_of_rollouts): #Se realizan las simulaciones
                        rollout_game = copy.deepcopy(game_copy) #Otra copia del juego para simular
                        evaluation_value = 0 #Valor de la evaluación

                        while rollout_game.game_over() is None: #Mientras el juego no haya terminado
                            heuristic_move = directions[self.heuristic_search(rollout_game)] #Se obtiene el mejor movimiento
                            getattr(rollout_game, heuristic_move)() #Se realiza el movimiento
                            rollout_game.add_number() #Se agrega un número al juego

                        if eval_function == 0: #Se evalúa el juego según la función de evaluación
                            evaluation_value = rollout_game.get_score()
                        elif eval_function == 1: 
                            evaluation_value = rollout_game.sum_matrix()
                        elif eval_function == 2:
                            evaluation_value = self.heuristic(rollout_game.get_state())

                        rollout_eval += evaluation_value #Se suma la evaluación de la simulación
            
                    if avg_evaluations == 1: #Opcion de promediar las evaluaciones
                        rollout_eval /= number_of_rollouts

                    if rollout_eval > best_rollout_eval: #Si la evaluación es mejor que la mejor evaluación
                        best_rollout_eval = rollout_eval #Se actualiza la mejor evaluación
                        best_move = move #Se actualiza el índice del mejor movimiento
                
            if best_move: #Si se encontró un mejor movimiento
                if getattr(game, best_move)(): #Se realiza el movimiento
                    game.add_number() #Se agrega un número al juego

            else:
                break #Si no se encontró un mejor movimiento, se termina el juego

        return game.get_max_value() #Se retorna el valor máximo del juego
        
max_value = 0
i = 1
while max_value < 2048:
    game = matrix_2048()
    mcts = MCTS2048(game)
    max_value = mcts.init_algorithm(game)
    print(f"Max value in game {i}: ", max_value)
    game.print_matrix()
    print()
    i += 1

