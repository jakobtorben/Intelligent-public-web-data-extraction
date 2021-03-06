import torch
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
import random
import collections

# replay buffer class stores transition information (s,a,r,s') dynamically
# not used in testing
class ReplayBuffer:
    
    def __init__(self):
        self.buffer_len = 4
        self.buffer = collections.deque(maxlen=500)
        
    def append_to_buffer(self,transition):
        self.buffer.append(transition)
        
    def sample_minibatch(self):
        return random.sample(self.buffer,self.buffer_len)

# basic network architecture
# 3 layers: input, hidden, output
# relu activation, 100 nodes in hidden layer
class sampleNetwork(nn.Module):
    
    def __init__(self, input_dimension, output_dimension):
        super(sampleNetwork, self).__init__()
        self.layer_1 = nn.Linear(input_dimension, 100)
        self.layer_2 = nn.Linear(100, 100)
        self.output_layer = nn.Linear(100, output_dimension)
        
    def forward(self, x):
        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        x = self.output_layer(x)
        return x

# driver class
class spiderNet:
    
    def __init__(self,input_dimension):
        self.network = sampleNetwork(input_dimension, output_dimension=1)
        self.q_network = sampleNetwork(input_dimension, output_dimension=1)
        self.target_network = sampleNetwork(input_dimension, output_dimension=1)
        self.optimiser = optim.Adam(self.network.parameters(), lr=0.01)
        self.gamma = 0.9
    
    # training on a minibatch
    # 'Q_true' is only there for testing, would be replaced with a 
    # Q estimate in real implementation
    def train(self, minibatch):
        self.optimiser.zero_grad()
        loss = self._calculate_loss(minibatch)
        print("LOSS", loss)
        loss.backward()
        self.optimiser.step()
        return loss.item()
    
    # calculate loss on a minibatch, again Q_true only there for testing
    def _calculate_loss(self, minibatch):
        
        # unpack states into tensor
        SA_minibatch_tensor = torch.tensor([minibatch[i][0] for i in range(len(minibatch))])
        # unpack successor state into tensor
        next_SA_minibatch_tensor = torch.tensor([minibatch[i][2] for i in range(len(minibatch))])
        
        # unpack rewards into tensor
        reward_tensor = torch.tensor([minibatch[i][1] for i in range(len(minibatch))])
        
        # Q values for current state
        current_q = self.q_network.forward(SA_minibatch_tensor)
        
        # get Q value of best action in next state
        next_q = self.target_network.forward(next_SA_minibatch_tensor)
        
        # Q target defined as reward + gamma*best Q in next state
        target_q = reward_tensor + (self.gamma * next_q)
        
        # calculate MSE loss
        loss = torch.nn.MSELoss()(current_q,target_q)
        
        return loss
