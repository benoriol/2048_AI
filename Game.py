import numpy as np
import random


class Board:

    def __init__(self, initMatrix = [[-1]], N = 4, Ninit = 3):

        self.PTwoTiles = 0.2
        self.PTileIsFour = 0.3

        self.MOVE_DICT = {0: 'd', 1: 'r', 2: 'u', 3: 'l'}

        self.N = N
        if ((initMatrix[0][0]) != -1):
            self.board = initMatrix
        else:
            self.board = np.zeros((self.N, self.N))

        for i in range(Ninit):
            self.addTileRand(2)

        self.score = 0

    def addTile(self, x, y, size):
        self.board[x, y] = size

    def emptyTiles(self):
        NEmpty = 0
        empty = np.zeros((16, 2), dtype='i4')
        for x in range(4):
            for y in range(4):
                if self.board[x, y] == 0:
                    empty[NEmpty] = [x, y]
                    NEmpty += 1
        return (empty, NEmpty)

    #Adds tile of given value in a random position:
    #If no argument is passed, if might add o or two tiles of vslue 2 or 4, determined randomly
    def addTileRand(self, size = -1):

        (empty, NEmpty) = self.emptyTiles()
        pos = random.choice(empty[:NEmpty])
        if size == -1:

            N = (random.randint(0, 1) < self.PTwoTiles) + 1
            for n in range(N):
                size = 2 * ((random.randint(0, 1) < self.PTileIsFour) + 1)
                (empty, NEmpty) = self.emptyTiles()
                if NEmpty > 0:
                    pos = random.choice(empty[:NEmpty])
                    self.addTile(pos[0], pos[1], size)


        elif size != -1:
            (empty, NEmpty) = self.emptyTiles()
            if NEmpty > 0:
                pos = random.choice(empty[:NEmpty])
                self.addTile(pos[0], pos[1], size)

    # Puts all the tiles together in upwards direction
    def packTiles(self, col):
        NnonZeros = np.count_nonzero(col)
        col[0:NnonZeros] = [val for val in col if val != 0]
        col[NnonZeros:] *= 0
        return NnonZeros

    # Merges the tiles that are the same value AND directly next to each other
    def mergeTiles(self, col):

        NnonZeros = self.packTiles(col)

        if(NnonZeros > 1):
            for x in range(NnonZeros-1):
                if col[x] == col[x+1]:
                    self.score += int(col[x])
                    col[x] *= 2
                    col[:-1] = np.delete(col, x+1)
                    col[-1] = 0

    # Executes a movement in the upwards direction
    def moveUp(self):
        for y in range(self.N):
            self.mergeTiles(self.board[:, y])

    # Executes a movement in a given direction
    def move(self, direction):
        self.lastScore = self.score

        lastBoard = np.array(self.board)
        if direction == 'u':
            self.moveUp()
        elif direction == 'r':
            self.board = np.rot90(self.board, 1)
            self.moveUp()
            self.board = np.rot90(self.board, 3)
        elif direction == 'l':
            self.board = np.rot90(self.board, 3)
            self.moveUp()
            self.board = np.rot90(self.board, 1)
        elif direction == 'd':
            self.board = np.rot90(self.board, 2)
            self.moveUp()
            self.board = np.rot90(self.board, 2)
        if not(np.array_equal(lastBoard, self.board)):
            self.addTileRand()
        self.score_increment = self.score - self.lastScore

    def step(self, action):
        self.move(self.MOVE_DICT[action])
        return [self.board, self.reward(), self.Lost(), np.max(self.board)]

    def reward(self):
        n = np.count_nonzero(self.board)
        # return (8.0 - n)/16.0 * self.score_increment
        return self.score_increment

    # Returns True if the player can't do any movement
    def Lost (self):
        import numpy as np
        for n in range(2):
            for x in range(self.N):
                for y in range(self.N-1):
                    if (self.board[y, x] == self.board[y+1, x]) | (self.board[x, y] == 0):
                        self.board = np.rot90(self.board, 4-n)
                        return False
                if self.board[self.N-1, x] == 0:
                    self.board = np.rot90(self.board, 4 - n)
                    return False
            self.board = np.rot90(self.board, 1)
        self.board = np.rot90(self.board, 4 - n)
        return True
