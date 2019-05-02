import random
import copy
import game
import math
from math import inf

class Player():
    def __init__(self, symbol, num):
        self.symbol = symbol
        self.playerNum = num

class Dummy(Player):
	def __init__(self, symbol, num):
			super(Dummy, self).__init__(symbol, num)

	def playTurn(self, game, lrow, lcol):
		mrow, mcol = game.board.getNextMiniBoard(lrow, lcol, game)
		valid = False
		row = -1
		col = -1
		random.seed()

		if(mrow == -1 and mcol == -1):
			while(not valid):
				row = random.randint(0,8)
				col = random.randint(0,8)

				miniRow, miniCol = game.board.getCurrentMiniBoard(row, col)

				if(game.boardSpots[row][col] == 0 and game.miniBoards[miniRow][miniCol] == 0):
					valid = True
		else:
			while(not valid):
				trow = random.randint(0,2)
				tcol = random.randint(0,2)
				row = 3*(mrow) + trow
				col = 3*(mcol) + tcol

				if(game.boardSpots[row][col] == 0):
					valid = True

		return row, col

class MonteCarlo(Player):
	def __init__(self, symbol, num):
		super(MonteCarlo, self).__init__(symbol, num)
		testGame = game.Game(0,0)
		self.mcTree = self.MCTree(0, 0, [], None, testGame)


	def playTurn(self, game, lrow, lcol):
		#tunable parameter
		C = math.sqrt(2)
		print()
		print("Player " + str(game.currentPlayer.playerNum) + " (Monte Carlo):")
		#set root node to current game state
		nextChild = self.findChild(game.boardSpots)
		if(nextChild == None):
			dummyGame = copy.deepcopy(game)
			dummyGame.player1 = Dummy(' X ', 1)
			dummyGame.player2 = Dummy(' O ', 2)

			if(game.currentPlayer.playerNum == 1):
				dummyGame.currentPlayer = dummyGame.player1
				dummyGame.nextPlayer = dummyGame.player2
			else:
				dummyGame.currentPlayer = dummyGame.player2
				dummyGame.nextPlayer = dummyGame.player1

			child = self.MCTree(0, 0, [], self.mcTree, dummyGame)
			self.mcTree.children.append(child)
			self.mcTree = child
		else:
			self.mcTree = nextChild

		for i in range(100):	
			#selection step
			leaf = self.mcTree
			random.seed()
			while(len(leaf.children) > 0):
				# leaf = leaf.children[random.randint(0, len(leaf.children) - 1)]
				ubc_lst = []
				for idx, ch in enumerate(leaf.children):
					if ch.gamesPlayed == 0:
						ubc = 0
					else:
						ubc =(ch.wins / ch.gamesPlayed) + C*(math.sqrt(math.log(leaf.gamesPlayed)/ch.gamesPlayed))
					ubc_lst.append(ubc)
				max_idx = ubc_lst.index(max(ubc_lst))
				#print(ubc_lst)
				leaf = leaf.children[max_idx]
				#print(type(leaf))

				# leaf = leaf.children[random.randint(0, len(leaf.children) - 1)]
				# maxVal = 0
				# maxOpt= None
				# for c in leaf.children:
				# 	if(c.gamesPlayed != 0):
				# 		val = (c.wins / c.gamesPlayed) + C * math.sqrt(math.log(leaf.gamesPlayed) / c.gamesPlayed)
				# 	else:
				# 		val = 0
				# 	if val >= maxVal:
				# 		maxVal = val
				# 		maxOpt = c
				# leaf = maxOpt
			
			#expansion step
			playoutNode = None
			result = self.terminal(leaf.game)
			if(result == 0):
				nextMBRow, nextMBCol = leaf.game.board.getNextMiniBoard(leaf.game.lrow, leaf.game.lcol, leaf.game)

				if(nextMBRow == -1 and nextMBCol == -1):
					#play anywhere
					for row in range(9):
						for col in range(9):
							mrow, mcol = leaf.game.board.getCurrentMiniBoard(row, col)

							if(leaf.game.boardSpots[row][col] == 0 and leaf.game.miniBoards[mrow][mcol] == 0):
								newGame = copy.deepcopy(leaf.game)
								newGame.updateGame(row, col, newGame.currentPlayer.playerNum, newGame.currentPlayer.symbol)

								temp = newGame.currentPlayer
								newGame.currentPlayer = newGame.nextPlayer
								newGame.nextPlayer = temp


								newChild = self.MCTree(0, 0, [], leaf, newGame)
								leaf.children.append(newChild)
				else:
					for trow in range(3):
						for tcol in range(3):
							row = 3 * nextMBRow + trow
							col = 3 * nextMBCol + tcol
							mrow, mcol = leaf.game.board.getCurrentMiniBoard(row, col)

							if(leaf.game.boardSpots[row][col] == 0 and leaf.game.miniBoards[mrow][mcol] == 0):
								newGame = copy.deepcopy(leaf.game)
								newGame.updateGame(row, col, newGame.currentPlayer.playerNum, newGame.currentPlayer.symbol)

								temp = newGame.currentPlayer
								newGame.currentPlayer = newGame.nextPlayer
								newGame.nextPlayer = temp

								newChild = self.MCTree(0, 0, [], leaf, newGame)
								leaf.children.append(newChild)
			
				#simulation
				random.seed()
				playoutNode = leaf.children[random.randint(0, len(leaf.children) - 1)]
				resultGame = copy.deepcopy(playoutNode.game)
				result = resultGame.dummyPlay()

			#backprop
			if(playoutNode == None):
				searchNode = leaf
			else:
				searchNode = playoutNode

			while(searchNode.parent != None):
				searchNode.gamesPlayed += 1
				if(result == self.playerNum):
					searchNode.wins += 1
				searchNode = searchNode.parent

		maxRatio = 0.0
		maxChild = None
		for child in self.mcTree.children:
			if(child.gamesPlayed != 0):
				ratio = child.wins / child.gamesPlayed
				if ratio >= maxRatio:
					maxRatio = ratio
					maxChild = child

		self.mcTree = maxChild

		return maxChild.game.lrow, maxChild.game.lcol

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
	def findChild(self, board):
		for child in self.mcTree.children:
			if(child.game.boardSpots == board):
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

	def evaluate_small_box(self, miniBoard, player):
		opponent = self.opponent(player)

		score = 0

		goal_states=[]
		col0 = [miniBoard[0][0],miniBoard[1][0],miniBoard[2][0]]
		goal_states.append(col0)
		col1 = [miniBoard[0][1],miniBoard[1][1],miniBoard[2][1]]
		goal_states.append(col1)
		col2 = [miniBoard[0][2],miniBoard[1][2],miniBoard[2][2]]
		goal_states.append(col2)
		diag1 = [miniBoard[0][0],miniBoard[1][1],miniBoard[2][2]]
		goal_states.append(diag1)
		diag2 = [miniBoard[0][2],miniBoard[1][1],miniBoard[2][0]]
		goal_states.append(diag2)
		row0 = miniBoard[0]
		goal_states.append(row0)
		row1 = miniBoard[1]
		goal_states.append(row1)
		row2 = miniBoard[2]
		goal_states.append(row2)

		for state in goal_states:
			
			if state.count(player) == 3:
				score += 100
			elif state.count(player) == 2 and state.count(0) == 1:
				score += 10
			elif state.count(player) == 1 and state.count(0) == 2:
				score += 1
			elif state.count(opponent) == 3:
				score -= 100
				return score
			elif state.count(opponent) == 2 and state.count(0) == 1:
				score -= 10
			elif state.count(opponent) == 1 and state.count(0) == 2:
				score -= 1

		return score

	def opponent(self, player):
		if player == 1:
			return 2
		else:
			return 1

	def evaluate(self, game, board, player):
		score = 0
		for row in range(3):
			for col in range(3):
				x,y = game.board.getCurrentMiniBoard(row, col)
				coords = game.board.miniCoordToGlobal(x, y)
				temp = []
				for x,y in coords:
					temp.append(board[x][y])
				miniBoard = []
				miniBoard.append(temp[:3])
				miniBoard.append(temp[3:6])
				miniBoard.append(temp[6:9])
				score += self.evaluate_small_box(miniBoard, player)
		return score

	def playTurn(self, game, lrow, lcol, depth=20):
		print()
		print("Player " + str(game.currentPlayer.playerNum) + " (MiniMax):")

		dummyGame = copy.deepcopy(game)
		dummyGame.player1 = Dummy(' X ', 1)
		dummyGame.player2 = Dummy(' O ', 2)
		if game.currentPlayer.playerNum == 1:
			dummyGame.currentPlayer = dummyGame.player1
			dummyGame.nextPlayer = dummyGame.player2
		else:
			dummyGame.currentPlayer = dummyGame.player2
			dummyGame.nextPlayer = dummyGame.player1

		player = dummyGame.currentPlayer.playerNum

		val, move = self.miniMax(dummyGame, lrow, lcol, depth, dummyGame.currentPlayer.playerNum)
		return move[0], move[1]
		# succ = self.successors(dummyGame.boardSpots, dummyGame, lrow, lcol, player)

		# best_move = (-inf, None)

		# for coord, board in succ.items():
		# 	dummyGame.updateGame(coord[0], coord[1], player, dummyGame.currentPlayer.symbol)
		# 	val = self.min_turn(dummyGame, board, coord, self.opponent(player), depth-1, -inf, inf)
		# 	if val > best_move[0]:
		# 		best_move = (val, coord)
		# nope = 0
		# if best_move[1] is None:
		# 	nope += 1
		# 	x = list(succ.keys())[0][0]
		# 	y = list(succ.keys())[0][1]
		# 	coord = (x,y)
		# 	best_move = (-inf, coord)
		# print(nope)
		# return best_move[1][0], best_move[1][1]

	def miniMax(self, game, lrow, lcol, depth, maxPlayer):
		#print('top minimax')
		#print(self.evaluate(game, game.boardSpots, game.nextPlayer.playerNum))
		
		player = game.currentPlayer.playerNum
		succ = self.successors(game.boardSpots, game, lrow, lcol, player)
		#stopping conditions, evaluate the state
		if depth <= 0 or len(succ) == 0 or game.board.checkBoard(game.miniBoards, self.opponent(player)) or game.board.checkBoard(game.miniBoards, player):
			return self.evaluate(game, game.boardSpots, game.nextPlayer.playerNum)
		
		depth -1

		if maxPlayer == game.currentPlayer.playerNum:
			val = -inf
			move = None
			for coord in succ:
				#update game
				game.updateGame(coord[0], coord[1], player, game.currentPlayer.symbol)
				#update next player
				hold = game.currentPlayer
				game.currentPlayer = game.nextPlayer
				game.nextPlayer = hold
				#maximize
				temp, move = self.miniMax(game, coord[0], coord[1], depth, maxPlayer)
				if temp > val:
					val = temp
					move = coord
			return val, move
		else:
			val = inf
			move = None
			for coord in succ:
				#update game
				game.updateGame(coord[0], coord[1], player, game.currentPlayer.symbol)
				#update next player
				hold = game.currentPlayer
				game.currentPlayer = game.nextPlayer
				game.nextPlayer = hold
				#minimize
				temp, move = self.miniMax(game, coord[0], coord[1], depth, maxPlayer)
				if temp < val:
					val = temp
					move = coord
			return val, move

	def successors(self, board, game, lrow, lcol, player):
		succ = []
		mr, mc = game.board.getNextMiniBoard(lrow, lcol, game)
		if mr == -1 or game.board.checkBoardFull(mr, mc, board) is True:
			for x, row in enumerate(board):
				for y, val in enumerate(row):
					temp = copy.deepcopy(game.boardSpots)
					if val == 0:
						temp[x][y] = player
						succ.append((x,y))
						# succ[(x,y)] = temp
		else:
			coords = game.board.miniCoordToGlobal(mr, mc)
			for (x,y) in coords:
				temp = copy.deepcopy(game.boardSpots)
				if temp[x][y] == 0:
					temp[x][y] = player
					succ.append((x,y))
					# succ[(x,y)] = temp
		return succ

	def min_turn(self, game, board, last_move, player, depth, alpha, beta):
		if depth <= 0 or game.board.checkBoard(game.miniBoards, self.opponent(player)) or game.board.checkBoard(game.miniBoards, player):
		# if depth <= 0:
			return self.evaluate(game, board, last_move, player)

		succ = self.successors(board, game, last_move[0], last_move[1], player)
		temp = inf
		for coord, board in succ.items():
			game.updateGame(coord[0], coord[1], player, game.currentPlayer.symbol)
			val = self.max_turn(game, board, coord, self.opponent(player), depth-1, alpha, beta)
			# if val < beta:
			#     beta = val
			# if alpha >= beta:
			#     break
			if val < temp:
				temp = val
		return temp

	def max_turn(self, game, board, last_move, player, depth, alpha, beta):
		if depth <= 0 or game.board.checkBoard(game.miniBoards, self.opponent(player)) or game.board.checkBoard(game.miniBoards, player):
		# if depth <= 0:
			return self.evaluate(game, board, last_move, player)

		succ = self.successors(board, game, last_move[0], last_move[1], player)
		temp = -inf
		for coord, board in succ.items():
			game.updateGame(coord[0], coord[1], player, game.currentPlayer.symbol)
			val = self.min_turn(game, board, coord, self.opponent(player), depth-1, alpha, beta)
			# if alpha < val:
			#     alpha = val
			# if alpha >= beta:
			#     break
			if val > temp:
				temp = val
		return temp

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
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 0 and row <= 2 and col >= 3 and col <= 5):
						valid = True
					else:
						print("This is not a valid move")
				except:
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
		print()
		print("Player " + str(self.playerNum) + " (Random):")
		mrow, mcol = game.board.getNextMiniBoard(lrow, lcol, game)
		valid = False

		random.seed()
		while(not valid):
			if(mrow == -1 and mcol == -1):
				row = random.randint(0,8)
				col = random.randint(0,8)
			else:
				row = 3*mrow + random.randint(0,2)
				col = 3*mcol + random.randint(0,2)

			miniRow, miniCol = game.board.getCurrentMiniBoard(row, col)
			if(game.boardSpots[row][col] == 0 and game.miniBoards[miniRow][miniCol] == 0):
				valid = True
		
		return row, col

