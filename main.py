import Game
import numpy as np


Ninit = 3
init = np.zeros((1,1))-1
b = Game.Board(init)

for i in range(Ninit):
    b.addTileRand(2)
print b.board
while True:
    movDir = raw_input('Movement: ')
    b.move(movDir)
    b.addTileRand(2)
    print b.board

"""
init = np.zeros((4,4))
init[1:, 3] = [4, 4, 16]
b = Game.Board(init)
print b.board
b.move('d')
print b.board
"""