import torch
import torch.nn as nn
import torch.nn.functional as F
from IPython import embed


class QNet(nn.Module):
	def __init__(self):
		super(QNet, self).__init__()
		self.fc1 = nn.Linear(16, 32)
		self.fc2 = nn.Linear(32, 64)
		self.fc3 = nn.Linear(64, 32)
		self.fc4 = nn.Linear(32, 4)
	def forward(self, x):
		(_, H, W) = x.data.size()
		x = x.view(-1, H * W)
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = F.relu(self.fc3(x))
		return self.fc4(x)
