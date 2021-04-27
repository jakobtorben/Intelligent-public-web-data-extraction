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
        self.optimiser = optim.Adam(self.network.parameters(), lr=0.01)
    
    # training on a minibatch
    # 'Q_true' is only there for testing, would be replaced with a 
    # Q estimate in real implementation
    def train(self, minibatch, Q_true):
        self.optimiser.zero_grad()
        loss = self._calculate_loss(minibatch)
        loss.backward()
        self.optimiser.step()
        return loss.item()
    
    # calculate loss on a minibatch, again Q_true only there for testing
    def _calculate_loss(self, minibatch):
        
        Q_pred = self.network.forward(minibatch)
        
        Q_target = self.network.forward(next_state)
        
        # calculate MSE loss
        loss = torch.nn.MSELoss()(Q_pred,Q_true)
        
        return loss