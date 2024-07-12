import sys
from matrix import matrix_2048
from agent import agent
import os

if len(sys.argv) < 2:
    print("Error: No se ha proporcionado el nombre del archivo del agente.")
    sys.exit(1)

print("Ejecutando experimento con el agente", sys.argv[1])
agent_filename = sys.argv[1]
a = agent(0, 0, 0, 0)
a.load_agent(agent_filename)

game = matrix_2048()
game.restart()

max_score = {
    "score": 0,
    "max_cell": 0,
}

for i in range(100):
    game.restart()
    game.add_number()
    game.add_number()
    while True:
        score = game.get_score()
        board = game.get_matrix()
        move = a.get_move(score, board)
        if game.game_over() != None:
            if game.get_max_value() > max_score["max_cell"]:
                max_score["max_cell"] = game.get_max_value()
            if score > max_score["score"]:
                max_score["score"] = score
            break
        if move == 0:
            game.down()
        elif move == 1:
            game.up()
        elif move == 2:
            game.left()
        elif move == 3:
            game.right()
        game.add_number()

# Asegúrate de que el directorio existe antes de intentar escribir en el archivo
results_dir = "./agents/results"
os.makedirs(results_dir, exist_ok=True)

with open(f"{results_dir}/results.csv", "a") as file:
    file.write(agent_filename + "," + str(max_score["score"]) + "," + str(max_score["max_cell"]) + "\n")
    
print("Experimento finalizado")