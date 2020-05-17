import torch as T
import torch.nn as nn
import torch.nn.functional as F

def board_to_input(board):
    p4 = np.argwhere(board==4)
    p3 = np.argwhere(board==3)
    p2 = np.argwhere(board==2)
    p1 = np.argwhere(board==1)
    m1 = np.argwhere(board==-1)
    m2 = np.argwhere(board==-2)
    m3 = np.argwhere(board==-3)
    m4 = np.argwhere(board==-4)
    input = np.concatenate((p4, p3, p2, p1, m1, m2, m3, m4))
    return input

class ActorCritic(nn.Module):
    def __init__(self, observation_space, action_space):
