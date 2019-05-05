from board import Board
from players import *

class Game():
	def __init__(self, player1, player2, repeat = 1):
		self.board = Board()
		self.player1 = None
		self.player2 = None
		self.winner = 0
		self.lrow = -1
		self.lcol = -1
		self.GAME_OVER = False

		if(player1 == 1):
			self.player1 = User(" X ", 1)
		elif(player1 == 2):
			self.player1 = MonteCarlo(" X ", 1)
		elif(player1 == 3):
			self.player1 = Minimax(" X ", 1)
		elif(player1 == 4):
			self.player1 = Random(" X ", 1)
		elif(player1 == 0):
			self.player1 = Dummy(' X ', 1)

		if(player2 == 1):
			self.player2 = User(" O ", 2)
		elif(player2 == 2):
			self.player2 = MonteCarlo(" O ", 2)
		elif(player2 == 3):
			self.player2 = Minimax(" O ", 2)
		elif(player2 == 4):
			self.player2 = Random(" O ", 2)
		elif(player2 == 0):
			self.player2 = Dummy(' O ', 2)


		self.currentPlayer = self.player1
		self.nextPlayer = self.player2

		#-1 -> tied and full mini-board, 0 -> not claimed, 1 -> claimed by player 1, 2 -> claimed by player 2
		self.boardSpots = [[0 for i in range(9)] for j in range(9)]
		self.miniBoards = [[0 for i in range(3)] for j in range(3)]

		player1Wins = 0
		player2Wins = 0
		ties = 0
		if(player1 != 0):
			for i in range(0, repeat):
				self.play()
				if(self.board.checkBoard(self.miniBoards, 1)):
					player1Wins += 1
				elif(self.board.checkBoard(self.miniBoards, 2)):
					player2Wins += 1
				else:
					ties += 1

				print("player 1 wins: " + str(player1Wins))
				print("player 2 wins: " + str(player2Wins))
				print("ties: " + str(ties))


				self.board = Board()
				self.player1 = None
				self.player2 = None
				self.lrow = -1
				self.lcol = -1
				self.GAME_OVER = False

				if(player1 == 1):
					self.player1 = User(" X ", 1)
				elif(player1 == 2):
					self.player1 = MonteCarlo(" X ", 1)
				elif(player1 == 3):
					self.player1 = Minimax(" X ", 1)
				elif(player1 == 4):
					self.player1 = Random(" X ", 1)
				elif(player1 == 0):
					self.player1 = Dummy(' X ', 1)

				if(player2 == 1):
					self.player2 = User(" O ", 2)
				elif(player2 == 2):
					self.player2 = MonteCarlo(" O ", 2)
				elif(player2 == 3):
					self.player2 = Minimax(" O ", 2)
				elif(player2 == 4):
					self.player2 = Random(" O ", 2)
				elif(player2 == 0):
					self.player2 = Dummy(' O ', 2)


				self.currentPlayer = self.player1
				self.nextPlayer = self.player2

				#-1 -> tied and full mini-board, 0 -> not claimed, 1 -> claimed by player 1, 2 -> claimed by player 2
				self.boardSpots = [[0 for i in range(9)] for j in range(9)]
				self.miniBoards = [[0 for i in range(3)] for j in range(3)]
				


	def play(self):
		row = -1
		col = -1
		while(not self.GAME_OVER):
			self.board.printBoard()
			row, col = self.currentPlayer.playTurn(self, row, col)
			self.lrow, self.lcol = row, col
			self.updateGame(row, col, self.currentPlayer.playerNum, self.currentPlayer.symbol)

			if(self.currentPlayer.playerNum == 1):
				self.currentPlayer = self.player2
				self.nextPlayer = self.player1
			else:
				self.currentPlayer = self.player1
				self.nextPlayer = self.player2

	#play out a test game for Monte Carlo
	def dummyPlay(self):
		while(not self.GAME_OVER):
			row, col = self.currentPlayer.playTurn(self, self.lrow, self.lcol)
			self.updateGame(row, col, self.currentPlayer.playerNum, self.currentPlayer.symbol)

			if(self.currentPlayer.playerNum == 1):
				self.currentPlayer = self.player2
				self.nextPlayer = self.player1
			else:
				self.currentPlayer = self.player1
				self.nextPlayer = self.player2

		if(self.board.checkBoard(self.miniBoards, 1)):
			return 1
		elif(self.board.checkBoard(self.miniBoards, 2)):
			return 2
		elif(self.board.checkTie(self.miniBoards)):
			return -1


	def updateGame(self, row, col, player, symbol):
		self.lrow, self.lcol = row, col
		self.boardSpots[row][col] = player
		if self.board.checkMinibox(row, col, player, self.boardSpots) is True:
			mr, mc = self.board.getCurrentMiniBoard(row, col)
			self.miniBoards[mr][mc] = player

			if self.board.checkBoard(self.miniBoards, self.currentPlayer.playerNum) is True:
				self.board.finishBoard(symbol)
				self.board.winner = player
				
				if(not isinstance(self.currentPlayer, Dummy)):
					self.board.printBoard()
					print()
					print("PLAYER " + str(player) + " WON!")

				self.GAME_OVER = True
			else:
				self.board.finishMiniBoard(row, col, symbol)

				if self.board.checkTie(self.miniBoards):
					if(not isinstance(self.currentPlayer, Dummy)):
						self.board.finishBoard(' + ')
						self.board.printBoard()
						print()
						print("YOU TIED!")

					self.GAME_OVER = True

		elif self.board.checkBoardFull(row, col, self.boardSpots):
			mr, mc = self.board.getCurrentMiniBoard(row, col)
			self.miniBoards[mr][mc] = -1
			self.board.finishMiniBoard(row, col, ' + ')

			if self.board.checkTie(self.miniBoards):
				if(not isinstance(self.currentPlayer, Dummy)):
					self.board.finishBoard(' + ')
					self.board.printBoard()
					print()
					print("YOU TIED!")

				self.GAME_OVER = True

		else:
			self.board.updateBoard(row, col, symbol)

