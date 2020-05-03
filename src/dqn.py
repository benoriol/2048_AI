import torch
import numpy as np
from IPython import embed

def train(buffer, agent):
    data = buffer.sample()

    torch_state = torch.from_numpy(np.array([m.tolist() for m in data['state']]))
    torch_action = torch.from_numpy(data['action'])
    torch_next_state = torch.from_numpy(data['next_state'])
    torch_reward = torch.from_numpy(data['reward'])
    torch_done = torch.from_numpy(data['done'])


    # q_values state
    all_q_values = agent.forward(torch_state)
    # pick q value of action
    q_values = all_q_values.gather(1, torch_action.unsqueeze(1))

    # next q values from next state
    next_q_values = agent.target_forward(torch_next_state)

    # compute target r + gamma* max q_values next state

    # comute loss

    # step optim stuff
