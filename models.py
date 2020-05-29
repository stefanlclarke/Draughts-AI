import numpy as np
import torch as T
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
    arg = np.argmax(out)
    posflat = flatlist[arg]
    ypos = posflat//dim
    xpos = posflat-ypos*dim
    move = np.argmax(move)
    return (xpos, ypos, move)

class Memory:
    def __init__(self, maxframes):
        self.memory = []
        self.maxframes = maxframes

    def addstate(self, prev_state, loc, move, step_output):
        prev = board_to_onehot(prev_state)
        next = board_to_onehot(step_output[0])
        reward = step_output[1]
        done = step_output[2]
        self.memory.append([prev, loc, move, next, reward, done])

    def erase_old(self):
        self.memory = self.memory[-self.maxframes:-1]

class Actor:
    def __init__(self, input_dim, l1, l2, locations, moves):
        #super(Network, self).__init__()
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
        onehot = T.from_numpy(onehot).float()
        loc, move = self.forward(onehot)
        loc = loc.detach().numpy()
        move = move.detach().numpy()
        m = output_to_move(loc, move)
        return loc, move, m
