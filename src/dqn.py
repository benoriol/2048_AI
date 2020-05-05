import torch
import numpy as np
from IPython import embed

def train(buffer, agent):
    data = buffer.sample()

    torch_state = torch.from_numpy(np.array([m.tolist() for m in data['state']]))
    torch_action = torch.from_numpy(np.array(data['action']))
    torch_next_state = torch.from_numpy(np.array([m.tolist() for m in data['next_state']]))
    torch_reward = torch.from_numpy(np.array(data['reward']))
    torch_done = torch.from_numpy(np.array(data['done']))


    # q_values state
    all_q_values = agent.forward(torch_state.float())
    # pick q value of action
    q_values = all_q_values.gather(1, torch_action.unsqueeze(dim=1))
    # next q values from next state
    next_q_values = agent.target_forward(torch_next_state.float())

    # compute target r + gamma* max q_values next state
    tgt = torch_reward.unsqueeze(dim=1) + agent.gamma * torch.max(next_q_values, dim=1)[0].unsqueeze(dim=1)
    # comute loss
    loss = agent.loss_fn(q_values, tgt)

    # step optim stuff
    agent.optim.zero_grad()
    loss.backward()
    agent.optim.step()
