import gym
import gym_draughts
from models import Actor, delete_diagonals, board_to_onehot, output_to_move, Memory, move_to_onehot, Critic, AC
import torch as T
import numpy as np
import random

actor_layers = [10, 10]
critic_layers = [10, 10, 10]
memory = Memory(2000)
ac = AC(18, actor_layers, critic_layers, 18, 4)
gamma = 0.9
learning_rate = 3e-3
optimizer = T.optim.Adam(ac.parameters(), lr = learning_rate)

env = gym.make('draughts-v0')

def play_against_random():
    maxmoves = 10000
    num_moves = 0
    env.reset()
    playing = True
    firstmove = True
    while playing:
        currentmove = env.board.player
        if currentmove == -1:
            nowstate = env.get_state()
            if not firstmove:
                memory.addstate(oldstate, loc, move, (m,i), (nowstate, reward, done, illegal))
            else:
                firstmove = False
            oldstate = env.get_state()
            loc, move, m, i = ac.actor.forward_from_board(env.board.board)
            newstate, reward, done, illegal = env.step(m)
            #print(reward)
            #env.render()
            num_moves += 1
            if num_moves > maxmoves:
                playing = False
            if done:
                nowstate = env.get_state()
                memory.addstate(oldstate, loc, move, (m,i), (nowstate, reward, done, illegal))
                #print(reward)
                playing = False
        if currentmove == 1 and playing == True:
            mr = env.random_move()
            newstate, rewardy, done, illegal_random = env.step(mr)
            reward -= rewardy
            #env.render()
            if done:
                nowstate = env.get_state()
                memory.addstate(oldstate, loc, move, (m,i), (nowstate, reward, done, illegal))
                #print(reward)
                playing = False

def play_random_game():

    env.reset()
    playing=True
    firstmove = True
    while playing:
        currentmove = env.board.player
        if currentmove == -1:
            nowstate = env.get_state()
            if not firstmove:
                memory.addstate(oldstate, loc, move, (mr,), (nowstate, reward, done))
            else:
                firstmove = False
            oldstate = env.get_state()
            mr = env.random_move()
            loc, move = move_to_onehot(mr)
            newstate, reward, done = env.step(mr)
            env.render()
            if done:
                nowstate = env.get_state()
                memory.addstate(oldstate, loc, move, (mr,), (nowstate, reward, done))
        if currentmove == 1:
            mrr = env.random_move()
            newstate, rewardy, done = env.step(mrr)
            reward -= rewardy
            env.render()
            if done:
                nowstate = env.get_state()
                memory.addstate(oldstate, loc, move, (mr,), (nowstate, reward, done))
        if done:
            playing = False

def play_random_games(number):
    for i in range(number):
        play_random_game()

def train_against_random(steps_per_loop, epochs_per_loop=10, states_per_epoch=100, recurrent=False, loops=0):
    loops_elapsed = 0
    training = True
    while training:
        env.reset()
        memory.reset()
        wins = 0
        for step in range(steps_per_loop):
            play_against_random()
            if memory.memory[-1][-3]>0:
                wins += 1

        for i in range(epochs_per_loop):
            sample = random.sample(memory.memory, states_per_epoch)
            num_steps = len(sample)
            Qerrors = []
            nextQs = []
            logprobs = []
            for state in sample:
                prevq = ac.critic.forward_from_board(state[0])
                newq = ac.critic.forward_from_board(state[4])
                reward = state[5]
                Qerror = (prevq - reward - gamma*newq)**2
                Qerrors.append(Qerror)
                nextQs.append(newq)
                move_chosen = state[3][0][2]
                loc_chosen = state[3][1]
                loc_prob = state[1][loc_chosen]
                #print(move_chosen)
                move_prob = state[2][move_chosen]
                log_prob = T.log(loc_prob) + T.log(move_prob)
                logprobs.append(log_prob)

            Qerrors = T.stack(Qerrors)
            logprobs = T.stack(logprobs)
            nextQs = T.stack(nextQs)
            actor_loss = (-logprobs*nextQs).mean()
            critic_loss = Qerrors.mean()
            loss = actor_loss + critic_loss

            optimizer.zero_grad()
            loss.backward(retain_graph=True)
            optimizer.step()

        win_prop = wins/steps_per_loop
        move_legalities = [memory.memory[x][-1] for x in range(len(memory.memory))]
        legal_count = move_legalities.count(True)
        legal_prop = legal_count/len(move_legalities)

        print(f"ILLEGAL PROPORTION: {legal_prop}")
        print(f"WIN PROPORTION: {win_prop}")

        loops_elapsed += 1
        if not recurrent:
            if loops_elapsed > loops:
                training = False

train_against_random(1, loops=1)
[memory.memory[i][-3] for i in range(len(memory.memory))]
env.render()
