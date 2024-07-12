import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
import math
from collections import deque, namedtuple
from matrix import matrix_2048
import matplotlib.pyplot as plt
from itertools import count

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(DEVICE)

# He init
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
    
def encode_state(game):
  game = np.array(game)
  game_flatten = [0 if e == 0 else int(math.log(e, 2)) for e in game.flatten()]
  game_flatten = torch.LongTensor(game_flatten)
  game_flatten = F.one_hot(game_flatten, num_classes=16).float().flatten()
  game_flatten = game_flatten.reshape(1, 4, 4, 16).permute(0, 3, 1, 2)
  return game_flatten

# Replay buffer
Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

# Hiperparámetros
BATCH_SIZE = 64
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 0.9999
TARGET_UPDATE = 20
n_actions = 4

policy_net = DQN().to(DEVICE)
target_net = DQN().to(DEVICE)
target_net.load_state_dict(policy_net.state_dict())
# Descomentar para cargar pesos 
#policy_net.load_state_dict(torch.load('./training_DQN/policy_w.pth'))
#target_net.load_state_dict(torch.load('./training_DQN/target_w.pth'))
target_net.eval()
policy_net.train()

optimizer = optim.Adam(policy_net.parameters(), lr=5e-5)
memory = ReplayMemory(50000)

steps_done = 0

def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = max(EPS_END, EPS_START * (EPS_DECAY ** steps_done))
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.randrange(n_actions)]], device=DEVICE, dtype=torch.long)
    
def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=DEVICE, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=DEVICE)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    criterion = nn.MSELoss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def same_move(state, next_state, last_memory):
  return torch.eq(state, last_memory.state).all() and torch.eq(next_state, last_memory.next_state).all()

game =  matrix_2048()
total_scores, best_tile_list = [], []
historical_max_value = 0

num_episodes = 10000
for episode in range(num_episodes):
    #print(f"Episode {episode}")
    game.restart()
    state = encode_state(game.get_state()).float()
    duplicate = False
    for t in count():
        # Seleccionar y realizar acción
        valid_move = True
        action = select_action(state)
        old_score = game.get_score()
        if action.item() == 0:
            valid_move = game.up()
        elif action.item() == 1:
            valid_move = game.down()
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
                print(f'Nuevo máximo alcanzado: {historical_max_value}, episodio: {episode}')
        done = game.game_over() is not None
        reward = (game.get_score() - old_score)
        reward = torch.tensor([reward], device=DEVICE)

        # Observar nuevo estado
        if not done:
            next_state = encode_state(game.get_state()).float()
        else:
            next_state = None
        
        if next_state != None and torch.eq(state, next_state).all():
            reward -= 10
        
        if game.game_over() == True:
            reward += 50
        elif game.game_over() == False:
            reward -= 30

        if next_state == None or len(memory) == 0 or not same_move(state, next_state, memory.memory[-1]):
            memory.push(state, action, next_state, reward)
        
        state = next_state
        
        if done:
            # Optimizar el modelo
            for _ in range(100):
                optimize_model()

            total_scores.append(game.get_score())
            best_tile_list.append(game.get_max_value())
            break

    # Actualizar red target
    if episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
        policy_net.train()
    
    # Guardar pesos 
    if episode % 10 == 0:
        torch.save(policy_net.state_dict(), './policy_w.pth')
        torch.save(target_net.state_dict(), './target_w.pth')

torch.save(policy_net.state_dict(), './policy_w.pth')
torch.save(target_net.state_dict(), './target_w.pth')

# Realizar gráficos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica de las puntuaciones
ax1.plot(total_scores)
ax1.set_xlabel('Episodios')
ax1.set_ylabel('Reward total')
ax1.set_title('Reward total en entrenamiento')

# Gráfica de Max_value
ax2.plot(best_tile_list)
ax2.set_xlabel('Episodios')
ax2.set_ylabel('Valor más alto en entrenamiento')
ax2.set_title('Valor más alto')

# Guardar la figura completa con ambos subplots
plt.savefig('training.png')

print('Complete')
