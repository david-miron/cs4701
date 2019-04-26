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

	def getCurrentMiniBoard(self, lrow, lcol, game):
		if(lrow == -1 and lcol == -1):
			miniBoardRow = -1
			miniBoardCol = -1
		else:
			miniBoardRow = lrow / 3
			miniBoardCol = lcol / 3

			if(game.miniBoards[miniBoardRow][miniBoardCol] != 0):
				miniBoardRow = -1
				miniBoardCol = -1

		return miniBoardRow, miniBoardCol

	def checkMinibox():
		return 0

	def checkBoard():
		return 0
