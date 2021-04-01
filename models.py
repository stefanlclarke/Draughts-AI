import torch
import torch.nn as nn

class FeedForwardNet(torch.nn.Module):
    """
    Generic feedforward neural net
    """
    def __init__(self, board_dim, layers, role='actor'):
        super(FeedForwardNet, self).__init__()

        self.input_dim = board_dim * board_dim * 4

        if role == 'actor':
            self.actor = True
            self.output_dim = board_dim * board_dim * 2
        else:
            self.actor = False
            self.output_dim = 1

        self.layer_sizes = layers 
        in_layer_out = [self.input_dim] + layers + [self.output_dim]
        feedforward_dimensions = [(in_layer_out[i],in_layer_out[i+1]) for i in range(len(in_layer_out)-1)]

        self.hidden_layers = [nn.Linear(*dims) for dims in feedforward_dimensions]
        self.relu = nn.ReLU()

        if self.actor:
            self.softmax = nn.Softmax(dim=0)

        self.n_layers = len(self.hidden_layers)

    def forward(self, x):
        curr_val = x
        for i in range(self.n_layers - 1):
            curr_val = self.relu(self.hidden_layers[i](curr_val))

        if self.actor:
            curr_val = self.softmax(self.hidden_layers[-1](curr_val))
        else:
            curr_val = self.hidden_layers[-1](curr_val)
        return curr_val


class A2C(torch.nn.Module):
    def __init__(self, board_dim, hidden_actor, hidden_critic):
        """
        A2C nets
        """
        super(A2C, self).__init__()
        self.actor = FeedForwardNet(board_dim, hidden_actor, role='actor')
        self.critic = FeedForwardNet(board_dim, hidden_critic, role='critic')

    def forward(self, x):
        return self.actor(x), self.critic(x)
