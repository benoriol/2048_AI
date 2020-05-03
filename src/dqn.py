import torch
import numpy as np
from IPython import embed

def train(buffer, agent):
    state, action, next_state, reward, done = buffer.sample()

    embed()
    torch_state = torch.from_numpy(state)
    torch_action = torch.from_numpy(action)
    torch_next_state = torch.from_numpy(next_state)
    torch_reward = torch.from_numpy(reward)


    # q_values state
    all_q_values = agent.forward(torch_state)
    # pick q value of action
    q_values = all_q_values.gather(1, torch_action.unsqueeze(1))

    # next q values from next state
    next_q_values = agent.target_forward(torch_next_state)

    # compute target r + gamma* max q_values next state

    # comute loss

    # step optim stuff
