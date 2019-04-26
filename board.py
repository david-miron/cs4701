class Board():

	def __init__(self):
		self.spots = [[" - " for i in range(9)] for j in range(9)]

	def printBoard(self):
		for row in range(0, 9):
			#separaters between boards
			if(row % 3 == 0):
				#first row
				if(row == 0):
					print(" ", end = "")
					for col in range(1,30):
						#label columns
						if(col % 3 == 0 and col != 30):
							if((col - 3) % 9 == 0 and col != 3):
								print("-", end = "")
							print(int(col / 3) - 1, end = "")
						else:
							print("-", end = "")
				else:
					print(" ", end = "")
					for col in range(1,32):
						print("-", end = "")
				print()	

			print(row, end = "")

			#fill in spots
			for col in range(0, 9):

				#separaters between boards
				if(col % 3 == 0):
					print("|", end = "")

				print(self.spots[row][col], end = "")
			print("|")

		print(" ", end = "")
		for col in range(1,32):
			print("-", end = "")
		print()

	def updateBoard(self, row, col, symbol):
		self.spots[row][col] = symbol

	def getCurrentMiniBoard(self, row, col):
		miniBoardRow = int(row / 3)
		miniBoardCol = int(col / 3)

		return miniBoardRow, miniBoardCol

	def buildMiniBoard(self, board, trow, brow, lcol, rcol):
		miniBoard = []
		rows = board[trow:(brow+1)]
		for row in rows:
			miniBoard.append(row[lcol:(rcol+1)])

		return miniBoard

	def checkMiniboxHelper(self, miniBoard, num):
		col0 = 0
		col1 = 0
		col2 = 0
		diag1 = 0
		diag2 = 0
		for i, row in enumerate(miniBoard):
			col0 = col0 + 1 if row[0] == num else col0
			col1 = col1 + 1 if row[1] == num else col1
			col2 = col2 + 1 if row[2] == num else col2
			diag1 = diag1 + 1 if row[i] == num else diag1
			diag2 = diag2 + 1 if row[-(i+1)] == num else diag2
			if row.count(num) == 3:
				print("here")
				return True 

		if col0 == 3 or col1 == 3 or col2 == 3 or diag1 == 3 or diag2 == 3:
			print("not there")
			return True

		return False

	def checkMinibox(self, row, col, player, symbol, game):
		miniRow, miniCol = self.getCurrentMiniBoard(row, col)
		#print(miniRow, miniCol)
		if (miniRow == 0) and (miniCol == 0):
			miniBoard = self.buildMiniBoard(game.boardSpots, 0, 2, 0, 2)
			print(miniBoard)
			num = game.currentPlayer.playerNum
			print(num)
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 0) and (miniCol == 1):
			miniBoard = self.buildMiniBoard(game.boardSpots, 0, 2, 3, 5)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 0) and (miniCol == 2):
			miniBoard = self.buildMiniBoard(game.boardSpots, 0, 2, 6, 8)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 1) and (miniCol == 0):
			miniBoard = self.buildMiniBoard(game.boardSpots, 3, 5, 0, 2)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 1) and (miniCol == 1):
			miniBoard = self.buildMiniBoard(game.boardSpots, 3, 5, 3, 5)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 1) and (miniCol == 2):
			miniBoard = self.buildMiniBoard(game.boardSpots, 3, 5, 6, 8)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 2) and (miniCol == 0):
			miniBoard = self.buildMiniBoard(game.boardSpots, 6, 9, 0, 2)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 2) and (miniCol == 1):
			miniBoard = self.buildMiniBoard(game.boardSpots, 6,  9, 3, 5)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		elif (miniRow == 2) and (miniCol == 2):
			miniBoard = self.buildMiniBoard(game.boardSpots, 6,  9, 6, 8)
			num = game.currentPlayer.playerNum
			if self.checkMiniboxHelper(miniBoard, num) is True:
				return True

		return False

	def checkBoard(self, row, col, player, symbol, game):
		num = game.currentPlayer.playerNum
		if self.checkMiniboxHelper(miniBoard, num) is True:
			return True
		else:
			return False

	def getCurrentMiniBoard(self, lrow, lcol, game):
		if(lrow == -1 and lcol == -1):
			miniBoardRow = -1
			miniBoardCol = -1
		else:
			miniBoardRow = int(lrow / 3)
			miniBoardCol = int(lcol / 3)

			if(game.miniBoards[miniBoardRow][miniBoardCol] != 0):
				miniBoardRow = -1
				miniBoardCol = -1

		return miniBoardRow, miniBoardCol