from IPython import embed

from utils import *
from Game import Board
from tqdm import tqdm
from Agent import Agent
from Buffer import Buffer
from torch.utils.tensorboard import SummaryWriter



config = getConfig('config_0.0')

setSeed(config['seed'])

paths = config['paths']

if ['tensorboard']:
    writer = SummaryWriter(paths['tensorboard'])

game = Board(N=config['game']['N'], Ninit=config['game']['init_tiles'])
agent = Agent(config['agent'], paths['weights'])
buffer = Buffer(config['buffer'])

embed()
for it in tqdm(range(config['iterations'])):
    pass
