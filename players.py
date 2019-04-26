class Player():
    def __init__(self, symbol, num):
        self.symbol = symbol
        self.playerNum = num

    def playTurn(self, game):
    	return 0

    def getMiniBoard(self, lrow, lcol, game):
    	if(lrow == -1 and lcol == -1):
    		miniBoardRow = -1
    		miniBoardCol = -1
    	else:
    		miniBoardRow = lrow % 3
    		miniBoardCol = lcol % 3

    		if(game.miniBoards[miniBoardRow][miniBoardCol] != 0):
    			miniBoardRow = -1
    			miniBoardCol = -1

    	return miniBoardRow, miniBoardCol

class MonteCarlo(Player):
	def __init__(self, symbol, num):
		super(MonteCarlo, self).__init__(symbol, num)

class Minimax(Player):
	def __init__(self, symbol, num):
		super(Minimax, self).__init__(symbol, num)

class User(Player):
	def __init__(self, symbol, num):
		super(User, self).__init__(symbol, num)

	#(lrow, lcol) was the last move
	def playTurn(self, game, lrow, lcol):
		valid = False
		row = -1
		col = -1

		while(not valid):
			miniBoardRow, miniBoardCol = self.getMiniBoard(lrow, lcol, game)

			if(miniBoardRow < 0 and miniBoardCol < 0):
				print("You can play on any mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 0 and row <= 8 and col >= 0 and col <= 8):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 0 and miniBoardCol == 0):
				print("You can play on the top left mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 0 and row <= 2 and col >= 0 and col <= 2):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 0 and miniBoardCol == 1):
				print("You can play on the top middle mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 0 and row <= 2 and col >= 3 and col <= 5):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 0 and miniBoardCol == 2):
				print("You can play on the top right mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 0 and row <= 2 and col >= 6 and col <= 8):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 1 and miniBoardCol == 0):
				print("You can play on the middle left mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 3 and row <= 5 and col >= 0 and col <= 2):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 1 and miniBoardCol == 1):
				print("You can play on the middle mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 3 and row <= 5 and col >= 3 and col <= 5):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 1 and miniBoardCol == 2):
				print("You can play on the middle right mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 3 and row <= 5 and col >= 6 and col <= 8):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 2 and miniBoardCol == 0):
				print("You can play on the bottm left mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 6 and row <= 8 and col >= 0 and col <= 2):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 2 and miniBoardCol == 1):
				print("You can play on the bottom middle mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 6 and row <= 8 and col >= 3 and col <= 5):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 2 and miniBoardCol == 2):
				print("You can play on the bottom right mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 6 and row <= 8 and col >= 6 and col <= 8):
					valid = True
				else:
					print("This is not a valid move")

				print()

			if(game.boardSpots[row][col] != 0):
				print("This spot is already taken")
				valid = False

		return row,col


class Random(Player):
	def __init__(self, symbol, num):
		super(Random, self).__init__(symbol, num)
