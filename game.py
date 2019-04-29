from board import Board
from players import *

class Game():
	def __init__(self, player1, player2):
		self.board = Board()
		self.player1 = None
		self.player2 = None
		self.GAME_OVER = False

		if(player1 == 1):
			self.player1 = User(" X ", 1)
		elif(player1 == 2):
			self.player1 = MonteCarlo(" X ", 1)
		elif(player1 == 3):
			self.player1 = Minimax(" X ", 1)
		elif(player1 == 4):
			self.player1 = Random(" X ", 1)

		if(player2 == 1):
			self.player2 = User(" O ", 2)
		elif(player2 == 2):
			self.player2 = MonteCarlo(" O ", 2)
		elif(player2 == 3):
			self.player2 = Minimax(" O ", 2)
		elif(player2 == 4):
			self.player2 = Random(" O ", 2)

		self.currentPlayer = self.player1

		#0 -> not claimed, 1 -> claimed by player 1, 2 -> claimed by player 2
		self.boardSpots = [[0 for i in range(9)] for j in range(9)]
		self.miniBoards = [[0 for i in range(3)] for j in range(3)]

		self.play()


	def play(self):
		row = -1
		col = -1
		while(not self.GAME_OVER):
			self.board.printBoard()
			row, col = self.currentPlayer.playTurn(self, row, col)
			self.updateGame(row, col, self.currentPlayer.playerNum, self.currentPlayer.symbol)

			print(self.currentPlayer.playerNum)

			if(self.currentPlayer.playerNum == 1):
				self.currentPlayer = self.player2
			else:
				self.currentPlayer = self.player1

			print(self.currentPlayer.playerNum)


	def updateGame(self, row, col, player, symbol):
		self.boardSpots[row][col] = player
		if self.board.checkMinibox(row, col, player, symbol, self) is True:
			print("omg i think a minibox has been won")
			mr, mc = self.board.getCurrentMiniBoard(row, col)
			self.miniBoards[mr][mc] = self.currentPlayer.playerNum
			if self.board.checkBoard(self.miniBoards, self) is True:
				#update the board to look like whoever won

				self.GAME_OVER = True
			else:
				print("yall good")
				self.board.wonMiniBoard(row, col, symbol)
				#update the box to show the player got it
		self.board.updateBoard(row, col, symbol)

