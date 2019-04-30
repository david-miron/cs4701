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

	#returns the mini board to play on next if the last move was (lrow, lcol)
	def getNextMiniBoard(self, lrow, lcol, game):
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

	#returns the coordinates of the minboard at row and col
	def getCurrentMiniBoard(self, row, col):
		miniBoardRow = int(row / 3)
		miniBoardCol = int(col / 3)

		return miniBoardRow, miniBoardCol

	#Returns a 3x3 miniboard for a given section of the board
	def buildMiniBoard(self, board, trow, brow, lcol, rcol):
		miniBoard = []
		rows = board[trow:(brow+1)]
		for row in rows:
			miniBoard.append(row[lcol:(rcol+1)])

		return miniBoard

	#Returns True if the 3x3 miniboard has been won, false otherwise
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
				return True 

		if col0 == 3 or col1 == 3 or col2 == 3 or diag1 == 3 or diag2 == 3:
			return True

		return False

	#Returns true if the current player has won a minibox, false otherwise
	def checkMinibox(self, row, col, player, symbol, game):
		miniRow, miniCol = self.getCurrentMiniBoard(row, col)
		if (miniRow == 0) and (miniCol == 0):
			miniBoard = self.buildMiniBoard(game.boardSpots, 0, 2, 0, 2)
			num = game.currentPlayer.playerNum
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

	#Returns True if the current player has won the game, False otherwise
	def checkBoard(self, miniBoards, num):
		if self.checkMiniboxHelper(miniBoards, num) is True:
			return True
		else:
			return False

	#return True if the board is full (meaning it is tied), and False otherwise
	def checkTie(self, miniBoards):
		for row in range(3):
			for col in range(3):
				if miniBoards[row][col] == 0:
					return False

		return True

	
	#Given col and row in the minibox of question, returns True if that minibox is full, False otherwise
	def checkBoardFull(self, row, col, game):
		def checkBoardFullHelper(miniboard):
			for row in miniboard:
				if 0 in row:
					return False

			return True

		miniRow, miniCol = self.getCurrentMiniBoard(row, col)
		if (miniRow == 0) and (miniCol == 0):
			miniBoard = self.buildMiniBoard(game.boardSpots, 0, 2, 0, 2)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 0) and (miniCol == 1):
			miniBoard = self.buildMiniBoard(game.boardSpots, 0, 2, 3, 5)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 0) and (miniCol == 2):
			miniBoard = self.buildMiniBoard(game.boardSpots, 0, 2, 6, 8)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 1) and (miniCol == 0):
			miniBoard = self.buildMiniBoard(game.boardSpots, 3, 5, 0, 2)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 1) and (miniCol == 1):
			miniBoard = self.buildMiniBoard(game.boardSpots, 3, 5, 3, 5)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 1) and (miniCol == 2):
			miniBoard = self.buildMiniBoard(game.boardSpots, 3, 5, 6, 8)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 2) and (miniCol == 0):
			miniBoard = self.buildMiniBoard(game.boardSpots, 6, 9, 0, 2)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 2) and (miniCol == 1):
			miniBoard = self.buildMiniBoard(game.boardSpots, 6,  9, 3, 5)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		elif (miniRow == 2) and (miniCol == 2):
			miniBoard = self.buildMiniBoard(game.boardSpots, 6,  9, 6, 8)
			if checkBoardFullHelper(miniBoard) is True:
				return True

		return False

	#fill in mini board with appropriate symbols when it has been won or tied
	def finishMiniBoard(self, row, col, symbol):
		miniRow, miniCol = self.getCurrentMiniBoard(row, col)
		if (miniRow == 0) and (miniCol == 0):
			for row in range(3):
				for col in range(3):
					self.updateBoard(row, col, symbol)
		elif (miniRow == 0) and (miniCol == 1):
			for row in range(3):
				for col in range(3,6):
					self.updateBoard(row, col, symbol)

		elif (miniRow == 0) and (miniCol == 2):
			for row in range(3):
				for col in range(6,9):
					self.updateBoard(row, col, symbol)

		elif (miniRow == 1) and (miniCol == 0):
			for row in range(3,6):
				for col in range(3):
					self.updateBoard(row, col, symbol)

		elif (miniRow == 1) and (miniCol == 1):
			for row in range(3,6):
				for col in range(3,6):
					self.updateBoard(row, col, symbol)

		elif (miniRow == 1) and (miniCol == 2):
			for row in range(3,6):
				for col in range(6,9):
					self.updateBoard(row, col, symbol)

		elif (miniRow == 2) and (miniCol == 0):
			for row in range(6,9):
				for col in range(3):
					self.updateBoard(row, col, symbol)

		elif (miniRow == 2) and (miniCol == 1):
			for row in range(6,9):
				for col in range(3,6):
					self.updateBoard(row, col, symbol)

		elif (miniRow == 2) and (miniCol == 2):
			for row in range(6,9):
				for col in range(6,9):
					self.updateBoard(row, col, symbol)

	#fill full board with appropriate symbol when it has been won or tied
	def finishBoard(self, symbol):
		for row in range(9):
			for col in range(9):
				self.updateBoard(row, col, symbol)


