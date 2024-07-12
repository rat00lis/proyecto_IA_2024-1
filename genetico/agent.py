from genetico.population import *

class agent:
    def __init__ (self, population_size, genome_size, mutation_rate, tree_height):
        self.score = 0
        self.count = 0
        self.population = population(population_size, genome_size, mutation_rate, tree_height)
    
    def restart_game(self):
        if self.score > 0:
            self.count += 1
            self.population.get_cur().score = self.score
            self.population.go_next()
    
    def get_allowed_moves(self, board):
        allowed = [False, False, False, False]

        for x in range(0, 4):
            for y in range(0, 4):
                if board[y][x] != None:
                    if y < 3 and board[y + 1][x] in (None, board[y][x]):
                        allowed[0] = True
                    if y > 0 and board[y - 1][x] in (None, board[y][x]):
                        allowed[1] = True
                    if x > 0 and board[y][x - 1] in (None, board[y][x]):
                        allowed[2] = True
                    if x < 3 and board[y][x + 1] in (None, board[y][x]):
                        allowed[3] = True
        
        return allowed
    
    def get_move(self, score, board):
        self.score = score
        features = extract_features(board)
        g = self.population.get_cur()
        return g.decide(features, self.get_allowed_moves(board))
    
    def save_agent(self):
        self.population.save_population(filename="agent.json")
        #agregar score y count
        with open("agent.json", "r") as file:
            data = json.load(file)
            data["score_agent"] = self.score
            data["count_agent"] = self.count
        with open("agent.json", "w") as file:
            json.dump(data, file)


    def load_agent(self):
        try:
            self.population.load_population(filename="./genetico/agent.json")
            #cargar score y count
            with open("./genetico/agent.json", "r") as file:
                data = json.load(file)
                self.score = data["score_agent"]
                self.count = data["count_agent"]
        except Exception as e:
            print("No existe un agente entrenado, para entrenar uno ejecute training.py")
            print(e)
            exit()
