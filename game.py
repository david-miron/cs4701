from board import Board
from players import *

class Game():
	def __init__(self, player1, player2):
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
			self.player1 = Dummy()

		if(player2 == 1):
			self.player2 = User(" O ", 2)
		elif(player2 == 2):
			self.player2 = MonteCarlo(" O ", 2)
		elif(player2 == 3):
			self.player2 = Minimax(" O ", 2)
		elif(player2 == 4):
			self.player2 = Random(" O ", 2)
		elif(player2 == 0):
			self.player2 = Dummy()


		self.currentPlayer = self.player1
		self.nextPlayer = self.player2

		#-1 -> tied and full mini-board, 0 -> not claimed, 1 -> claimed by player 1, 2 -> claimed by player 2
		self.boardSpots = [[0 for i in range(9)] for j in range(9)]
		self.miniBoards = [[0 for i in range(3)] for j in range(3)]

		if(player1 != 0):
			self.play()


	def play(self):
		row = -1
		col = -1
		while(not self.GAME_OVER):
			self.board.printBoard()
			row, col = self.currentPlayer.playTurn(self, row, col)
			lrow, lcol = row, col
			self.updateGame(row, col, self.currentPlayer.playerNum, self.currentPlayer.symbol)

			if(self.currentPlayer.playerNum == 1):
				self.currentPlayer = self.player2
				self.nextPlayer = self.player1
			else:
				self.currentPlayer = self.player1
				self.nextPlayer = self.player2


	def updateGame(self, row, col, player, symbol):
		self.boardSpots[row][col] = player
		if self.board.checkMinibox(row, col, player, symbol, self) is True:
			mr, mc = self.board.getCurrentMiniBoard(row, col)
			self.miniBoards[mr][mc] = player

			if self.board.checkBoard(self.miniBoards, self.currentPlayer.playerNum) is True:
				self.board.finishBoard(symbol)
				
				self.board.printBoard()
				print()
				print("PLAYER " + str(player) + " WON!")

				self.GAME_OVER = True
			else:
				self.board.finishMiniBoard(row, col, symbol)

				if self.board.checkTie(self.miniBoards):
					self.board.finishBoard(' + ')
					self.board.printBoard()
					print()
					print("YOU TIED!")

					self.GAME_OVER = True

		elif self.board.checkBoardFull(row, col, self):
			mr, mc = self.board.getCurrentMiniBoard(row, col)
			self.miniBoards[mr][mc] = -1
			self.board.finishMiniBoard(row, col, ' + ')

			if self.board.checkTie(self.miniBoards):
					self.board.finishBoard(' + ')
					self.board.printBoard()
					print()
					print("YOU TIED!")

					self.GAME_OVER = True

		else:
			self.board.updateBoard(row, col, symbol)

