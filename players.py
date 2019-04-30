import random
import copy
import game

class Player():
    def __init__(self, symbol, num):
        self.symbol = symbol
        self.playerNum = num

class Dummy(Player):
	def __init__(self):
			name = "big dumb"

	def playTurn(self, game, lrow, lcol):
		print("hey dummy")

class MonteCarlo(Player):
	def __init__(self, symbol, num):
		super(MonteCarlo, self).__init__(symbol, num)
		testGame = game.Game(0,0)
		self.mcTree = self.MCTree(0, 0, [], None, testGame)


	def playTurn(self, game, lrow, lcol):
		#set root node to current game state
		nextChild = self.findChild(game, game.boardSpots)
		if(nextChild == None):
			child = self.MCTree(0, 0, [], self.mcTree, game)
			self.mcTree.children.append(child)
			self.mcTree = child
		else:
			self.mcTree = nextChild

		#selection step
		leaf = self.mcTree
		random.seed()
		while(len(leaf.children) > 0):
			leaf = leaf.children[random.randint(0, len(leaf.children) - 1)]

		#expansion step
		if(self.terminal(leaf.game) == 0):
			nextMBRow, nextMBCol = leaf.game.board.getNextMiniBoard(leaf.game.lrow, leaf.game.lcol, leaf.game)

			if(nextMBRow == -1 and nextMBCol == -1):
				print("play anywhere")
			else:
				for trow in range(3):
					for tcol in range(3):
						row = 3 * nextMBRow + trow
						col = 3 * nextMBCol + tcol
						mrow, mcol = leaf.game.board.getCurrentMiniBoard(row, col)

						if(leaf.game.boardSpots[row][col] == 0 and leaf.game.miniBoards()[mrow][mcol] == 0):
							newGame = copy.deepcopy(leaf.game)
							newGame.updateGame(row, col, newGame.currentPlayer.playerNum, newGame.currentPlayer.symbol)
							newChild = self.MCTree(0, 0, [], leaf, newGame)
							leaf.children.append(newChild)
		
		#simulation

		#backprop
		return -10, -10

	#return number of player that has won if there is a winner, 0 if on going, -1 if tie
	def terminal(self, game):
		if(game.board.checkBoard(game.miniBoards, 1)):
			return 1
		elif(game.board.checkBoard(game.miniBoards, 2)):
			return 2
		elif(game.board.checkTie(game.miniBoards)):
			return -1
		
		return 0



	#find child of current tree with matching board and return, None if it doesn't exist
	def findChild(self, game, board):
		for child in self.mcTree.children:
			if(child.game.boardState == board):
				return child
		return None

	class MCTree():
		def __init__(self, w, gp, ch, par, g):
			self.wins = w
			self.gamesPlayed = gp
			self.children = ch
			self.parent = par
			self.game = g


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
			miniBoardRow, miniBoardCol = game.board.getNextMiniBoard(lrow, lcol, game)

			if(miniBoardRow < 0 and miniBoardCol < 0):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on any mini board")
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 0 and row <= 8 and col >= 0 and col <= 8):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 0 and miniBoardCol == 0):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the top left mini board")
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 0 and row <= 2 and col >= 0 and col <= 2):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 0 and miniBoardCol == 1):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the top middle mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 0 and row <= 2 and col >= 3 and col <= 5):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 0 and miniBoardCol == 2):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the top right mini board")
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 0 and row <= 2 and col >= 6 and col <= 8):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 1 and miniBoardCol == 0):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the middle left mini board")
				row = int(input("Enter row: "))
				col = int(input("Enter col: "))
				if(row >= 3 and row <= 5 and col >= 0 and col <= 2):
					valid = True
				else:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 1 and miniBoardCol == 1):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the middle mini board")
				try:	
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 3 and row <= 5 and col >= 3 and col <= 5):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 1 and miniBoardCol == 2):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the middle right mini board")
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 3 and row <= 5 and col >= 6 and col <= 8):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 2 and miniBoardCol == 0):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the bottm left mini board")
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 6 and row <= 8 and col >= 0 and col <= 2):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 2 and miniBoardCol == 1):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the bottom middle mini board")
				try:	
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 6 and row <= 8 and col >= 3 and col <= 5):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			elif(miniBoardRow == 2 and miniBoardCol == 2):
				print("Player " + str(game.currentPlayer.playerNum) + " can play on the bottom right mini board")
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 6 and row <= 8 and col >= 6 and col <= 8):
						valid = True
					else:
						print("This is not a valid move")
				except:
					print("This is not a valid move")

				print()
			
			if(valid):
				if(game.boardSpots[row][col] != 0):
					print("This spot is already taken")
					valid = False

				mrow, mcol = game.board.getCurrentMiniBoard(row, col)
				if(game.miniBoards[mrow][mcol] != 0):
					print("This mini board is out of cOmIsSiOn ya big ol' dummy")
					valid = False

		return row,col


class Random(Player):
	def __init__(self, symbol, num):
		super(Random, self).__init__(symbol, num)

	def playTurn(self, game, lrow, lcol):
		(mbr, mbc) = self.getNextMiniBoard(lrow, lcol, game)
		(playr, playc) = ((3*mbr)+random.randint(0,2), (3*mbc)+random.randint(0,2))
		while game.boardSpots[playr][playc] == 1:
			(row, col) = ((3*mbr)+random.randint(0,2), (3*mbc)+random.randint(0,2))
		return (row, col)

