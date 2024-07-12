import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math

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
    
def encode_state(state):
  state = np.array(state)
  state_flatten = [0 if e == 0 else int(math.log(e, 2)) for e in state.flatten()]
  state_flatten = torch.LongTensor(state_flatten)
  state_flatten = F.one_hot(state_flatten, num_classes=16).float().flatten()
  state_flatten = state_flatten.reshape(1, 4, 4, 16).permute(0, 3, 1, 2)
  return state_flatten

class DQN_Agent():
    def __init__(self):
        self.policy_net = DQN().to(DEVICE)
        self.policy_net.load_state_dict(torch.load('./training_DQN/policy_w.pth'))
        self.policy_net.eval()

    def select_action(self, game):
        state = encode_state(game.get_state()).float()
        with torch.no_grad():
            q_values = self.policy_net(state)
            sorted_actions = torch.argsort(q_values, dim=1, descending=True)

            action_mapping = ['up', 'down', 'left', 'right']  
            for action in sorted_actions[0]:
                action_str = action_mapping[action.item()] 
                new_state = game.try_step(action_str)
                new_state = encode_state(new_state).float()
                if not torch.eq(state, new_state).all():  
                    return action.view(1, 1)
            return sorted_actions[0, 0].view(1, 1)
    



    