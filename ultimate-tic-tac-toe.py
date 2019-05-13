from game import Game

def main():
	print("Welcome to Ultimate Tic-Tac-Toe!")
	startGame()

def startGame():
	numOfPlayers = 5
	player1 = -1
	player2 = -1
	repeat = -1

	while(player1 < 1 or player1 > numOfPlayers):
		print("Select Player 1 (X):")
		print("1 - User")
		print("2 - Monte Carlo Tree Search AI")
		print("3 - MiniMax AI")
		print("4 - Random AI")
		print("5 - UCT AI")
		try:
			player1 = int(input("Enter Choice: "))
			if(player1 < 1 or player1 > numOfPlayers):
				print("Not a valid option")
				print()
		except:
			print("Not a valid option")
			print()

	print()

	while(player2 < 1 or player2 > numOfPlayers):
		print("Select Player 2 (O):")
		print("1 - User")
		print("2 - Monte Carlo Tree Search AI")
		print("3 - MiniMax AI")
		print("4 - Random AI")
		print("5 - UCT AI")
		try:
			player2 = int(input("Enter Choice: "))
			if(player2 < 1 or player2 > numOfPlayers):
				print("Not a valid option")
				print()
		except:
			print("Not a valid option")
			print()

	print()

	while(repeat <= 0):
		try:
			repeat = int(input("How many games should be played?: "))
			if(repeat <= 0):
				print("Not a valid option")
				print()
		except:
			print("Not an integer")
			print()

	game = Game(player1, player2, repeat)

if __name__ == "__main__": main()