import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math
from itertools import count
from collections import Counter
import matplotlib.pyplot as plt
from matrix import matrix_2048

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(DEVICE)

def init_weights(m):
        if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
            nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
            if m.bias is not None:
                nn.init.zeros_(m.bias)

class ConvBlock(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ConvBlock, self).__init__()
        d = output_dim // 4
        self.conv1 = nn.Conv2d(input_dim, d, 1, padding='same')
        self.conv2 = nn.Conv2d(input_dim, d, 2, padding='same')
        self.conv3 = nn.Conv2d(input_dim, d, 3, padding='same')
        self.conv4 = nn.Conv2d(input_dim, d, 4, padding='same')

    def forward(self, x):
        x = x.to(DEVICE)
        output1 = self.conv1(x)
        output2 = self.conv2(x)
        output3 = self.conv3(x)
        output4 = self.conv4(x)
        return torch.cat((output1, output2, output3, output4), dim=1)

class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.conv1 = ConvBlock(16, 2048)
        self.conv2 = ConvBlock(2048, 2048)
        self.conv3 = ConvBlock(2048, 2048)
        self.dense1 = nn.Linear(2048 * 16, 1024)
        self.dense6 = nn.Linear(1024, 4)
        self.apply(init_weights)
 
    def forward(self, x):
        x = x.to(DEVICE)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = nn.Flatten()(x)
        x = F.dropout(self.dense1(x))
        return self.dense6(x)
    
def encode_state(board):
  board = np.array(board)
  board_flat = [0 if e == 0 else int(math.log(e, 2)) for e in board.flatten()]
  board_flat = torch.LongTensor(board_flat)
  board_flat = F.one_hot(board_flat, num_classes=16).float().flatten()
  board_flat = board_flat.reshape(1, 4, 4, 16).permute(0, 3, 1, 2)
  return board_flat

policy_net = DQN().to(DEVICE)
policy_net.load_state_dict(torch.load('./training_DQN/policy_w.pth'))
policy_net.eval()

def select_action(state):
    with torch.no_grad():
        q_values = policy_net(state)
        sorted_actions = torch.argsort(q_values, dim=1, descending=True)

        action_mapping = ['up', 'down', 'left', 'right']  
        for action in sorted_actions[0]:
            action_str = action_mapping[action.item()] 
            new_state = game.try_step(action_str)
            new_state = encode_state(new_state).float()
            if not torch.eq(state, new_state).all():  
                return action.view(1, 1)
        return sorted_actions[0, 0].view(1, 1)
    

# Inicialización del juego
game = matrix_2048()
total_scores, best_tile_list = [], []
historical_max_value = 0

# Número de episodios 
num_test_episodes = 5
print("Start")
for i_episode in range(num_test_episodes):
    game.restart()
    state = encode_state(game.get_state()).float()
    for t in count():
        action = select_action(state)
        valid_move = True
        if action.item() == 0:
            valid_move = game.up()
        elif action.item() == 1:
            valid_move =  game.down()
        elif action.item() == 2:
            valid_move = game.left()
        elif action.item() == 3:
            valid_move = game.right()
        else:
            raise ValueError("Acción no válida")

        if valid_move:
            game.add_number()
        

        if game.get_max_value() > historical_max_value:
            historical_max_value = game.get_max_value()
            
        done = game.game_over() is not None
        if not done:
            next_state = encode_state(game.get_state()).float()
        else:
            next_state = None

        state = next_state
        
        if done:
            total_scores.append(game.get_score())
            best_tile_list.append(game.get_max_value())
            #print(f'Episodio {i_episode} finalizado - Puntuación: {game.get_score()}, Mejor ficha: {game.get_max_value()}')
            break

print("Complete")

# Contar la frecuencia de cada mejor ficha
best_tile_counter = Counter(best_tile_list)

# Extraer los datos para el gráfico de barras
best_tiles = list(best_tile_counter.keys())
tile_counts = list(best_tile_counter.values())
best_tiles_str = [str(i) for i in best_tiles]

# Crear la figura y los subgráficos
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Primer subgráfico: gráfico de barra con la cantidad de veces que se repite cada mejor ficha
axs[0].bar(best_tiles_str, tile_counts, color='blue')
axs[0].set_title('Frecuencia de las Mejores Fichas')
axs[0].set_xlabel('Mejor Ficha')
axs[0].set_ylabel('Cantidad de Veces')
for i in range(len(best_tiles_str)):
    axs[0].text(i, tile_counts[i], str(tile_counts[i]), ha='center', va='bottom')

# Segundo subgráfico: gráfico de línea con total_scores
axs[1].plot(range(len(total_scores)), total_scores, marker='o', linestyle='-', color='red')
axs[1].set_title('Puntuación Total por Episodio')
axs[1].set_xlabel('Episodio')
axs[1].set_ylabel('Puntuación Total')

# Mostrar los gráficos
plt.tight_layout()
plt.savefig('evalDQN.png')