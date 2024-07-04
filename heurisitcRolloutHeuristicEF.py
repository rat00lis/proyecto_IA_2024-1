from matrix import matrix_2048
import copy

class MCTS2048:
    def __init__(self, initial_state):
        self.initial_state = initial_state
    
    def heuristic(self, state):
        snake_weight = [[ 10,   8,    7,    6.5],
                        [ 0.5,  0.7,  1,    3],
                        [-0.5, -1.5, -1.8, -2],
                        [-3.8, -3.7, -3.5, -3]]
        heuristic_value = 0
        for i in range(4):
            for j in range(4):
                heuristic_value += state[i][j] * snake_weight[i][j]
        return heuristic_value

    def heuristicSearch(self, state):
        moves = ['up', 'down', 'left', 'right']
        heuristic_values = []
        for move in moves:
            new_state = state.try_step(move)
            old_state = state.get_state()
            if new_state != old_state:
                heuristic_values.append(self.heuristic(new_state))
            else:
                heuristic_values.append(-100000000000)
        
        best_move = -100000000000
        best_index = -1

        for i in range(len(heuristic_values)):
            if heuristic_values[i] > best_move:
                best_move = heuristic_values[i]
                best_index = i
        return best_index
    
    def init_algorithm(self, game):
        while game.game_over() is None:
            game.print_matrix()
            print(" ")
            direction = ['up', 'down', 'left', 'right']
            best_move_index = 0  # Use index to store the best move
            best_value = 0
            for move_index, move in enumerate(direction):  # Use enumerate to get both index and value
                moveSumValue = 0
                # copy of game
                gameCopy = copy.deepcopy(game)
                movement = getattr(gameCopy, move, None)
                movement()
                if gameCopy.get_state() == game.get_state():
                    continue
                rollouts = 100
                for i in range(rollouts):
                    gameCopyCopy = copy.deepcopy(gameCopy)
                    while gameCopyCopy.game_over() is None:
                        a_star_move = self.heuristicSearch(gameCopyCopy)  # Use a different variable for the move index
                        movement = getattr(gameCopyCopy, direction[a_star_move], None)
                        movement()
                        gameCopyCopy.add_number()
                    print(move, i, self.heuristic(gameCopyCopy.get_state()))  
                    moveSumValue += self.heuristic(gameCopyCopy.get_state())
                if moveSumValue > best_value:
                    best_value = moveSumValue
                    best_move_index = move_index  # Update the best move index based on the outer loop
            movement = getattr(game, direction[best_move_index], None)  # Use the best move index to select the direction
            movement()
            game.add_number()
        return game.get_max_value()
        
# Inicialización de A*
max_value = 0
#while max_value < 1024:
game = matrix_2048()
print()
astar_solver = MCTS2048(game)
max_value = astar_solver.init_algorithm(game)
print(f"Max value: {max_value}")
game.print_matrix()
print()

