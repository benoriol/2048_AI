import math
import os
import random
import torch
import numpy as np
from NN import QNet
from IPython import embed
from random import choice
from collections import defaultdict

class Agent:
	def __init__(self, cfg, weights_path, iterations):

		# General params
		self.movements = 0
		self.maxTile = 0
		self.eps_scheduled = lambda index: cfg['eps_fin'] + (cfg['eps_ini'] - cfg['eps_fin']) * math.exp(-1. * index / int(iterations / 7))

		# NN parameters
		self.gamma = cfg['gamma']
		self.alpha_nn = cfg['alpha']
		self.weight_decay = cfg['weight_decay']
		self.start_learning = cfg['start_learning']
		self.target_update_freq = cfg['target_update_freq']
		self.loss = 0

		# NN INITIALIZATION
		self.nn = None
		self.target_nn = None
		self.dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
		self.optim = None
		self.loss_fn = None
		self.initNN()

		# Weights params
		self.path_out = weights_path
		self.save_weights = cfg['save_weights']
		self.save_weights_freq = cfg['save_weights_freq']

	def initNN(self):
		self.nn = QNet()
		self.target_nn = QNet()
		self.nn.type(self.dtype)
		self.target_nn.type(self.dtype)
		self.optim = torch.optim.Adam(self.nn.parameters(), lr=self.alpha_nn)
		self.loss_fn = torch.nn.MSELoss()

	def reset(self, initState):
		self.movements = 0
		self.maxTile = 0
		self.done = False
		self.loss = 0

	def selectAction(self, state, it):
		if random.random() > self.eps_scheduled(it):
			q_values = self.forward(state)
			return int(q_values.argmax())
		else:
			return random.randint(0,3)

	def forward(self, state):
		state = torch.from_numpy(state).type(self.dtype)
		return self.nn.forward(state)

	def target_forward(self, state):
		state = torch.from_numpy(state).type(self.dtype)
		return self.target_nn.forward(state)


	def loadWeights(self, weights):
		self.nn.load_state_dict(weights)

	def updateTargetNN(self):
		self.target_nn.load_state_dict(self.nn.state_dict())

	# Save model and weights
	def saveModel(self, version, n, epoch):
		pass
		# TODO: modify paths and so on..

		# base_path = os.path.join(self.path_out, self.alg)
		# version_path = os.path.join(base_path, version)
		# agent_path = os.path.join(version_path, str(n))
		#
		# epoch_path = os.path.join(agent_path, '{}.pt'.format(epoch))
		# if not os.path.isdir(self.path_out):
		# 	os.mkdir(self.path_out)
		# if not os.path.isdir(base_path):
		# 	os.mkdir(base_path)
		# if not os.path.isdir(version_path):
		# 	os.mkdir(version_path)
		# if not os.path.isdir(agent_path):
		# 	os.mkdir(agent_path)
		#
		# torch.save({
		# 	'agent': n,
		# 	'state_dict': self.nn.state_dict(),
		# 	'optimizer': self.optim},
		# 	epoch_path)
