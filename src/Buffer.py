import numpy as np
from collections import defaultdict
from random import randint
from IPython import embed

class Buffer:
	def __init__(self, cfg):
		self.buffer_size = cfg['memory_size']
		self.batch_size = cfg['batch_size']
		self.buffer_data = defaultdict(list)

	def store(self, step):
		for i, s in enumerate(self.buffer_data.keys()):
			if len(self.buffer_data[s]) > self.buffer_size:
				self.buffer_data[s].pop(0)
		self.buffer_data['state'].append(step[0])
		self.buffer_data['action'].append(step[1])
		self.buffer_data['next_state'].append(step[2])
		self.buffer_data['reward'].append(step[3])
		self.buffer_data['done'].append(step[4])

	def sample(self):
		sample_data = defaultdict(list)
		seen = []
		for s in range(min(self.batch_size, len(self.buffer_data['state']))):
			sample_num = randint(0, len(self.buffer_data['state']) - 1)
			while sample_num in seen:
				sample_num = randint(0, len(self.buffer_data['state']) - 1)
			seen.append(sample_num)
			for key in self.buffer_data.keys():
				sample_data[key].append(self.buffer_data[key][sample_num])
		return sample_data
