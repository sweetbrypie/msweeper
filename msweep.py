import sys, os
from gameplay import Board, GameState
import re
import time
import random

""" 
	Command Line / Terminal Version of Minesweeper
	- Created by Angelica Quach
"""

class Game:

	def __init__(self):
		self.board = Board(rows=10, cols=10)

	def play(self):
		self.welcome()
		while self.board.game_state in [GameState.ongoing, GameState.start]:
			self.board.print_board_wrapper(self.board.print_board_hook)
			try:
				inp = input("> ")
				line = "".join(inp.split())
				point = tuple(map(int, line.split(",")))
				self.board.click_square(point[0], point[1])
			except (IndexError, ValueError):
				self.help()
			except KeyboardInterrupt:
				try:
					sys.exit(0)
				except SystemExit:
					os._exit(0)
		if self.board.game_state == GameState.lose:
			print("\n\nOh no! Better luck next time! You hit a mine.\n")
			print("Here's the solution!\n")
		else:
			print("\n\nYou didn't hit any of the mines! You win!\n")            
		self.board.print_board_wrapper(self.board.print_board_end_hook)

	def welcome(self):
		print("\nLet's play Minesweeper in Terminal!")
		self.help()
	
	def help(self):
		print("\nUse the following format to enter coordinates!")
		print("> <row>, <column>")
		print("> eg. 1, 1")

	def play_again(self):
		ask = input('Would you like to go again? (y/n): ')
		return ask.lower() == 'y'


class Solver:
	def __init__(self):
		self.game_count = 0
		self.win_count = 0
		self.possible_coords = []
		self.make_choices()

	def make_choices(self):
		for i in range(10):
			for j in range(10):
				cell = (i, j)
				self.possible_coords .append(cell)

	def choose_next(self, round):
		# current random strategy
		return random.choice(self.possible_coords)
		# implement actual strategy

	def autoplay(self):
		t0 = time.time()
		while self.game_count < 100000:
			round = Board(rows=10, cols=10)
			while round.game_state in [GameState.ongoing, GameState.start]:
				guess = self.choose_next(round)
				round.click_square(guess[0], guess[1])
			if round.game_state == GameState.win:
				self.win_count += 1
			self.game_count += 1
		t1 = time.time()
		print("\nNumber of games won: " + str(self.win_count) + " out of " + str(self.game_count) + " games.")
		print("Total time to complete the " + str(self.game_count) + "  attempts: " + str(t1-t0) + "seconds!\n")


if __name__ == "__main__":
	while True:
		game = Game()
		print("\n\n ~~~ Welcome to Minesweeper in Terminal! ~~~")
		print("\n\nIf you would like to play, please enter 'p' or 'play'.")
		print("If you would like for a solver to play the game for you, \nplease instead enter 's' or 'solver'.")
		print("If you would like to exit, please enter 'q' or 'quit'.\n\n")
		raw = input("> ")
		if raw == 'p' or raw == 'play':
			game.play()
		elif raw == 's' or raw == 'solver':
			print("\n\nThis is going to take a while since SOLVER will be\nplaying 100,000 games for you!")
			solver = Solver()
			solver.autoplay()
		elif raw == 'q' or raw == 'quit':
			break
		else:
			print("Oops! Invalid option detected! Let's try again.")
			print("\n\nIf you would like to play, please enter 'p' or 'play'.")
			print("If you would like for a solver to play the game for you, \nplease instead enter 's' or 'solver'.")
			print("If you would like to exit, please enter 'q' or 'quit'.\n\n")
			continue
		if not game.play_again():
			break
