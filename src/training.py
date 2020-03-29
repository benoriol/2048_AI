
from __future__ import division, print_function

from keras.models import Sequential
from keras.layers.core import Activation, Dense, Flatten
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam

import numpy as np
import os
import collections
import Game
import time



def get_next_batch(experience, model, num_actions, gamma, batch_size):
    batch_indices = np.random.randint(low=0, high=len(experience), size=batch_size)
    batch = [experience[i] for i in batch_indices]
    X = np.zeros((batch_size, 4, 4))
    Y = np.zeros((batch_size, num_actions))
    for i in range(len(batch)):
        try:
            s_t, a_t, r_t, s_tp1, game_over, maxtile = batch[i]
        except:
            pass
        X[i] = s_t

        Y[i] = model.predict(np.reshape(s_t, (1, 4, 4)))[0]

        Q_sa = np.max(model.predict(np.reshape(s_tp1, (1, 4, 4)))[0])
        if game_over:
            Y[i, a_t] = r_t
        else:
            Y[i, a_t] = r_t + gamma + Q_sa
    return X, Y

model = Sequential()
model.add(Flatten(input_shape=(4, 4)))
model.add(Dense(64, kernel_initializer='normal', activation='relu'))
model.add(Dense(64, kernel_initializer='normal', activation='relu'))
model.add(Dense(64, kernel_initializer='normal', activation='relu'))
model.add(Dense(128, kernel_initializer='normal', activation='relu'))
model.add(Dense(128, kernel_initializer='normal', activation='relu'))
model.add(Dense(64, kernel_initializer='normal', activation='relu'))
model.add(Dense(4, kernel_initializer='normal', activation='relu'))

model.compile(optimizer=Adam(lr=1e-6), loss='mse')

DATA_DIR = 'data'
NUM_ACTIONS = 4
GAMMA = 0.99
INITIAL_EPSILON = 0.1
FINAL_EPSILON = 0.0001
MEMORY_SIZE = 50000
NUM_EPOCHS_OBSERVE = 100
NUM_EPOCHS_TRAIN = 200

BATCH_SIZE = 32
NUM_EPOCHS = NUM_EPOCHS_OBSERVE + NUM_EPOCHS_TRAIN

MAX_EQUAL_MOVES = 7

game = Game.Board()

experience = collections.deque(maxlen=MEMORY_SIZE)

fout = open(os.path.join(DATA_DIR, "rl-network-results.tsv"), 'w')
num_games, num_wins = 0, 0
epsilon = INITIAL_EPSILON

for e in range(NUM_EPOCHS):
    game = Game.Board()

    loss = 0.0

    #get first state
    a_0 = 0
    x_t, r_0, game_over, maxtile = game.step(a_0)
    s_t = x_t


    equal_moves = 0
    a_t_last = -99
    while not game_over:
        s_tm1 = s_t

        if e <= NUM_EPOCHS_OBSERVE:
            a_t = np.random.randint(low=0, high=NUM_ACTIONS, size=1)[0]

        else:
            if np.random.rand() <= epsilon:
                a_t = np.random.randint(low=0, high=NUM_ACTIONS, size=1)[0]
            else:

                q = model.predict(np.reshape(s_t, (1, 4, 4)))[0]
                a_t = np.argmax(q)
                if a_t == a_t_last:
                    equal_moves = equal_moves+1
                if equal_moves > MAX_EQUAL_MOVES:
                    a_t = (a_t+1)%NUM_ACTIONS
                    equal_moves = 0
                a_t_last = a_t

        x_t, r_t, game_over, maxtile = game.step(a_t)
        s_t = x_t

        experience.append((s_tm1, a_t, r_t, s_t, game_over, maxtile))

        if e > NUM_EPOCHS_OBSERVE:
            X, Y = get_next_batch(experience, model, NUM_ACTIONS, GAMMA, BATCH_SIZE)
            #print(X.shape)
            loss += model.train_on_batch(X, Y)

    if epsilon > FINAL_EPSILON:
        epsilon -= (INITIAL_EPSILON - FINAL_EPSILON)/NUM_EPOCHS

    print("Epoch {:04d}/{:d} | Loss {:.5f} | Maxtile {:f}"
          .format(e + 1, NUM_EPOCHS, loss, maxtile))
    fout.write("{:04d}t{:.5f}t{:d}n".format(e + 1, loss, num_wins))

    if e % 100 == 0:
        # model.save(os.path.join(DATA_DIR, "rl-network.h5"), overwrite=True)
        pass

fout.close()

model.save(os.path.join(DATA_DIR, "rl-network.h5"), overwrite=True)






