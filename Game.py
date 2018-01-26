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


    def packTiles(self, col):
        import numpy as np
        NnonZeros = np.count_nonzero(col)
        col[0:NnonZeros] = [val for val in col if val != 0]
        col[NnonZeros:] *= 0
        return NnonZeros

    def mergeTiles(self, col):
        import numpy as np

        NnonZeros = self.packTiles(col)

        if(NnonZeros > 1):
            for x in range(NnonZeros-1):
                if col[x] == col[x+1]:
                    col[x] *= 2
                    col[:-1] = np.delete(col, x+1)
                    col[-1] = 0

    def moveUp(self):
        for y in range(self.N):
            self.mergeTiles(self.board[:,y])

    def move(self, direction):
        import numpy as np
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





