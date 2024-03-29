import numpy as np
import torch
import torch.nn as nn
import gym
import gym_draughts
import numpy as np

dim=6

def delete_diagonals(vec):
    delete1 = [2*i+1 for i in range(dim//2)]
    delete2 = [dim+2*i for i in range(dim//2)]
    delete = delete1 + delete2
    deletes = [[2*k*dim + x for x in delete] for k in range(dim//2)]
    flatlist = []
    for item in deletes:
        for thing in item:
            flatlist.append(thing)
    vec = np.delete(vec, flatlist)
    return vec

def board_to_onehot(board):
    board = board.flatten()
    boards = []
    for k in [-4, -3, -2, -1, 1, 2, 3, 4]:
        where = np.argwhere(board == k)
        z = np.zeros(dim**2)
        z[where]=1
        z = delete_diagonals(z)
        boards.append(z)
    return np.array(boards).flatten()

def output_to_move(out, move):
    locs1 = [2*i for i in range(dim//2)]
    locs2 = [dim+2*i+1 for i in range(dim//2)]
    loc = locs1 + locs2
    locations = [[2*k*dim + x for x in loc] for k in range(dim//2)]
    flatlist = []
    for item in locations:
        for thing in item:
            flatlist.append(thing)
    arg = np.random.choice(int(dim**2/2), p=out)
    posflat = flatlist[arg]
    ypos = posflat//dim
    xpos = posflat-ypos*dim
    move = np.random.choice(4, p=move)
    return (xpos, ypos, move), arg

def move_to_onehot(move):
    loc = dim*move[0]+move[1]
    move = move[2]
    loc1h = np.zeros(dim**2)
    loc1h[loc]=1
    move1h = np.zeros(4)
    move1h[move]=1
    loc1hd = delete_diagonals(loc1h)
    return loc1h, move1h

class Memory:
    def __init__(self, maxframes):
        self.memory = []
        self.maxframes = maxframes

    def addstate(self, prev_state, loc, move, movemade, step_output):
        prev = board_to_onehot(prev_state)
        next = board_to_onehot(step_output[0])
        reward = step_output[1]
        done = step_output[2]
        illegal = step_output[3]
        self.memory.append([prev, loc, move, movemade, next, reward, done, illegal])

    def erase_old(self):
        self.memory = self.memory[-self.maxframes:-1]

    def reset(self):
        self.memory = []

class Actor(torch.nn.Module):
    def __init__(self, input_dim, l1, l2, locations, moves):
        super(Actor, self).__init__()
        self.indim = input_dim
        self.l1 = l1
        self.l2 = l2
        self.out = locations
        self.moves = moves

        self.fc1 = nn.Linear(self.indim*8, self.l1)
        self.fc2 = nn.Linear(self.l1, self.l2)
        self.fc_location = nn.Linear(self.l2, self.out)
        self.fc_moves = nn.Linear(self.l2, self.moves)
        self.relu = nn.ReLU()
        self.softmax_loc = nn.Softmax()
        self.softmax_move = nn.Softmax()

    def forward(self, input):
        o1 = self.relu(self.fc1(input))
        o2 = self.relu(self.fc2(o1))
        loc = self.softmax_loc(self.fc_location(o2))
        move = self.softmax_move(self.fc_moves(o2))
        return loc, move

    def forward_from_board(self, input):
        onehot = board_to_onehot(input)
        onehot = torch.from_numpy(onehot).float()
        loc, move = self.forward(onehot)
        loc1 = loc.detach().numpy()
        move1 = move.detach().numpy()
        m, i = output_to_move(loc1, move1)
        return loc, move, m, i

class Critic(torch.nn.Module):
    def __init__(self, input_dim, l1, l2, l3):
        super(Critic, self).__init__()
        self.indim = input_dim
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

        self.fc1 = nn.Linear(self.indim*8, self.l1)
        self.fc2 = nn.Linear(self.l1, self.l2)
        self.fc3 = nn.Linear(self.l2, self.l3)
        self.fc4 = nn.Linear(self.l3, 1)
        self.relu = nn.ReLU()

    def forward(self, input):
        o1 = self.relu(self.fc1(input))
        o2 = self.relu(self.fc2(o1))
        o3 = self.relu(self.fc3(o2))
        out = self.fc4(o3)
        return out

    def forward_from_board(self, onehot):
        onehot = torch.from_numpy(onehot).float()
        Q = self.forward(onehot)
        return Q

class AC(torch.nn.Module):
    def __init__(self, input_dim, actor_layers, critic_layers, locs, moves):
        super(AC, self).__init__()
        self.actor = Actor(input_dim, actor_layers[0], actor_layers[1], locs, moves)
        self.critic = Critic(input_dim, critic_layers[0], critic_layers[1], critic_layers[2])
