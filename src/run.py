import os
from IPython import embed
from time import sleep
from utils import *
from Game import Board
from tqdm import tqdm
from Agent import Agent
from Buffer import Buffer
from dqn import train
# from torch.utils.tensorboard import SummaryWriter



config = getConfig('config_0.0')

setSeed(config['seed'])

paths = config['paths']

# if ['tensorboard']:
#     writer = SummaryWriter(paths['tensorboard'])

game = Board(N=config['game']['N'], Ninit=config['game']['init_tiles'])
agent = Agent(config['agent'], paths['weights'], config['iterations'])
buffer = Buffer(config['buffer'])

counter = 0
episodes = 0
super_max_tile = 0
iteration_max_tile = -1
iteration_sum_maxtile = 0
for it in range(config['iterations']):
    game.reset()
    state = game.getLogBoard()


    while not game.Lost():

        action = agent.selectAction(state, counter)
        next_state, reward, done, max_tile = game.step(action)
        buffer.store([state, action, next_state, reward, done])
        state = next_state
        # sleep(0.1)
        # os.system('clear')
        # print(next_state)
        counter += 1

        # NN training
        if counter > 50:
            train(buffer, agent)
        iteration_max_tile = max(iteration_max_tile, max_tile)


        if max_tile > super_max_tile:
            super_max_tile = max_tile
    # update target NN
    iteration_sum_maxtile += iteration_max_tile
    if episodes % agent.target_update_freq == 0:
        agent.target_nn.load_state_dict(agent.nn.state_dict())
        print("Episode {}.\t iterations avg max tile {}.\t Max tile so far {}\t Epislon {}".format(
            episodes, iteration_sum_maxtile/agent.target_update_freq, super_max_tile, agent.eps_scheduled(it)))
        iteration_max_tile = -1
        iteration_sum_maxtile = 0



    episodes += 1
