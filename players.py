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
	#opt 0 -> all random, opt 1 -> selection with ucb
	def __init__(self, symbol, num, opt=0):
		super(MonteCarlo, self).__init__(symbol, num)
		testGame = game.Game(0,0)
		self.mcTree = self.MCTree(0, 0, [], None, testGame)
		self.totalGames = 0
		self.option = opt


	def playTurn(self, game, lrow, lcol):
		#tunable parameter
		C = math.sqrt(2)
		print()
		if(self.option == 0):
			print("Player " + str(game.currentPlayer.playerNum) + " (Monte Carlo Tree Search):")
		elif(self.option == 1):
			print("Player " + str(game.currentPlayer.playerNum) + " (UCT):")
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
				if(self.option == 0):
					leaf = leaf.children[random.randint(0, len(leaf.children) - 1)]
				elif(self.option == 1):
					ucb_lst = []
					for idx, ch in enumerate(leaf.children):
						ucb =((ch.wins+1) / (ch.gamesPlayed+1)) + C*(math.sqrt(math.log(self.totalGames +1)/(ch.gamesPlayed +1)))
						ucb_lst.append(ucb)

					max_idx = ucb_lst.index(max(ucb_lst))
					leaf = leaf.children[max_idx]

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
				self.totalGames +=1

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

	def evaluate(self, game, board, player, lrow, lcol):
		#print(board)
		dummyGame = copy.deepcopy(game)
		board = dummyGame.boardSpots
		opponent = self.opponent(player)
		#print(player, opponent)
		score = 0
		if dummyGame.winner == player:
			return 100000
		elif dummyGame.winner == opponent:
			return -100000
		elif game.GAME_OVER is True:
		 	return 0

		def weight(x, y):
			temp = game.miniBoards[x][y]
			if x == 1 and y == 1 and temp == player:
				return 4
			if x == 0 and y == 0 and temp == player:
				return 3
			if x == 0 and y == 2 and temp == player:
				return 3
			if x == 2 and y == 0 and temp == player:
				return 3
			if x == 2 and y == 2 and temp == player:
				return 3
			if x == 1 and y == 0 and temp == player:
				return 2
			if x == 1 and y == 2 and temp == player:
				return 2
			if x == 0 and y == 1 and temp == player:
				return 2
			if x == 2 and y == 1 and temp == player:
				return 2
			else:
				return 0

		#print(score)
		for row in range(3):
			for col in range(3):
				mini_score = 0

				if dummyGame.miniBoards[row][col] == player:
					mini_score += 24
					# print(game.miniBoards[row][col])
					# print((row,col),player, "won")
				elif dummyGame.miniBoards[row][col] == opponent:
					mini_score -= 24
					# print(game.miniBoards[row][col])
					# print((row,col),opponent, "won")
				elif dummyGame.miniBoards[row][col] != -1 and dummyGame.miniBoards[row][col] == 0:
					x,y = dummyGame.board.getCurrentMiniBoard(row, col)
					coords = dummyGame.board.miniCoordToGlobal(x, y)

					temp = []

					for x,y in coords:
						temp.append(board[x][y])
					miniBoard = []
					miniBoard.append(temp[:3])
					miniBoard.append(temp[3:6])
					miniBoard.append(temp[6:9])
					#print(miniBoard)
					if miniBoard[1][1] == player:
						mini_score += 4 
					elif miniBoard[1][1] == opponent:
						mini_score -= 4 

					if miniBoard[0][0] == player:
						mini_score += 3
					elif miniBoard[0][0] == opponent:
						mini_score -= 3 

					if miniBoard[0][2] == player:
						mini_score += 3
					elif miniBoard[0][2] == opponent:
						mini_score -= 3 

					if miniBoard[2][0] == player:
						mini_score += 3
					elif miniBoard[2][0] == opponent:
						mini_score -= 3 

					if miniBoard[2][2] == player:
						mini_score += 3
					elif miniBoard[2][2] == opponent:
						mini_score -= 3 

					if miniBoard[1][0] == player:
						mini_score += 2
					elif miniBoard[1][0] == opponent:
						mini_score -= 2 

					if miniBoard[1][2] == player:
						mini_score += 2
					elif miniBoard[1][2] == opponent:
						mini_score -= 2 

					if miniBoard[0][1] == player:
						mini_score += 2 
					elif miniBoard[0][1] == opponent:
						mini_score -= 2 

					if miniBoard[2][1] == player:
						mini_score += 2 
					elif miniBoard[2][1] == opponent:
						mini_score -= 2 

				w = weight(row,col)
				score += mini_score*w
		return score

	def playTurn(self, game, lrow, lcol, depth=2):
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
		sym = dummyGame.currentPlayer.symbol

		succ = self.successors(dummyGame.boardSpots, dummyGame, lrow, lcol, player)
		#print(succ)
		val = -inf
		move = None

		for coord in succ:
			g = copy.deepcopy(dummyGame)
			
			#update game
			#print(dummyGame.boardSpots)
			g.updateGame(coord[0], coord[1], player, sym)
			#print(g.boardSpots)
			#update next player
			hold = g.currentPlayer
			g.currentPlayer = g.nextPlayer
			g.nextPlayer = hold
			#maximize
			temp, _ = self.miniMax(g, coord[0], coord[1], depth-1, False)
			#print(temp, coord, "max")
			if temp > val:
				val = temp
				move = coord
		return move[0], move[1]

	def miniMax(self, game, lrow, lcol, depth, maxPlayer):
		dummyGame = copy.deepcopy(game)
		player = dummyGame.currentPlayer.playerNum
		sym = dummyGame.currentPlayer.symbol
		
		succ = self.successors(dummyGame.boardSpots, dummyGame, lrow, lcol, player)
		#print(succ)
		#stopping conditions, evaluate the state
		if depth <= 0 or dummyGame.GAME_OVER is True:
			val = self.evaluate(dummyGame, dummyGame.boardSpots, player, lrow, lcol)
			#print(dummyGame.currentPlayer.playerNum)
			#print(val)
			return val, (lrow,lcol)

		if maxPlayer:
			val = -inf
			move = None
			for coord in succ:
				g = copy.deepcopy(dummyGame)
				#update game
				g.updateGame(coord[0], coord[1], player, sym)
				#update next player
				hold = g.currentPlayer
				g.currentPlayer = g.nextPlayer
				g.nextPlayer = hold
				#maximize
				temp, _ = self.miniMax(g, coord[0], coord[1], depth-1, False)
				#print(coord, temp, player, maxPlayer)
				#print(temp)
				if temp > val:
					val = temp
					move = coord
			#print(val, move)
			return val, move
		else:
			val = inf
			move = None
			for coord in succ:
				#print(coord)
				g = copy.deepcopy(dummyGame)
				#update game
				#print(g.currentPlayer.playerNum)
				g.updateGame(coord[0], coord[1], player, sym)
				#update next player
				hold = g.currentPlayer
				g.currentPlayer = g.nextPlayer
				g.nextPlayer = hold
				#print(g.currentPlayer.playerNum)
				#minimize
				temp, _ = self.miniMax(g, coord[0], coord[1], depth-1, True)
				#print(temp)
				#print(coord, temp, player, maxPlayer)
				if temp < val:
					val = temp
					move = coord
				#print(temp, coord, "min")
			return val, move

	def successors(self, board, game, lrow, lcol, player):
		dummyGame = copy.deepcopy(game)
		succ = []
		mr, mc = dummyGame.board.getNextMiniBoard(lrow, lcol, dummyGame)
		if mr == -1 or dummyGame.board.checkBoardFull(mr, mc, board) is True:
			for x, row in enumerate(board):
				for y, val in enumerate(row):
					mr, mc = dummyGame.board.getCurrentMiniBoard(x, y)
					if dummyGame.miniBoards[mr][mc] == 0:
						temp = copy.deepcopy(dummyGame.boardSpots)
						if val == 0:
							temp[x][y] = player
							succ.append((x,y))
		else:
			coords = dummyGame.board.miniCoordToGlobal(mr, mc)
			for (x,y) in coords:
				temp = copy.deepcopy(dummyGame.boardSpots)
				if temp[x][y] == 0:
					temp[x][y] = player
					succ.append((x,y))
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
				try:
					row = int(input("Enter row: "))
					col = int(input("Enter col: "))
					if(row >= 3 and row <= 5 and col >= 0 and col <= 2):
						valid = True
					else:
						print("This is not a valid move")
				except:
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
					print("This mini board is finished")
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


