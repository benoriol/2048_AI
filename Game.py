class Board:

    N = 4

    def __init__(self, initMatrix = [-1]):
        import numpy as np
        if (initMatrix[0,0] != -1):
            self.board = initMatrix
        else:
            self.board = np.zeros((self.N, self.N))

    def addTile(self, x, y, size):
        self.board[x, y] = size

    def addTileRand(self, size):
        import numpy as np
        NEmpty = 0
        emptyTiles = np.zeros((16, 2), dtype='i4')
        for x in range(4):
            for y in range(4):
                if self.board[x, y] == 0:
                    emptyTiles[NEmpty] = [x, y]
                    NEmpty += 1

        import random
        pos = random.choice(emptyTiles[:NEmpty])

        self.addTile(pos[0], pos[1], size)

    def moveUp(self):
        for y in range(self.N):
            for x in range(self.N):
                i = 0
                while (self.board[x, y] == 0) & (i < 3):
                    self.board[x:-1, y] = self.board[x+1:, y]
                    self.board[-1, y] = 0
                    i += 1

            for x in range(self.N-1):
                if (self.board[x,y] == self.board[x+1, y]) & (self.board[x,y] != 0):
                    self.board[x,y] *= 2
                    self.board[-1] = 0
                    if x < self.N - 2:
                        self.board[x+1:-1] = self.board[x+2:, y]

    def move(self, dir):
        import numpy as np
        if dir == 'u':
            self.moveUp()
        elif dir == 'r':
            self.board = np.rot90(self.board, 1)
            self.moveUp()
            self.board = np.rot90(self.board, 3)
        elif dir == 'l':
            self.board = np.rot90(self.board, 3)
            self.moveUp()
            self.board = np.rot90(self.board, 1)
        elif dir == 'd':
            self.board = np.rot90(self.board, 2)
            self.moveUp()
            self.board = np.rot90(self.board, 2)




