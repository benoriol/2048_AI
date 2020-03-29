import Game

Ninit = 3
b = Game.Board()

print(b.board)
while not (b.Lost()):
    movDir = input('Next movement: ')
    b.move(movDir)
    print(b.board)
    print('Score: ' + str(b.score))

print(' ----- GAME OVER -----')
print( 'FINAL SCORE: ' + str(b.score))
