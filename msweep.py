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
            self.board.pr_wrapper(self.board.pr_hook)
            try:
                inp = input("> ")
                line = "".join(inp.split())
                if line[0] == "f":
                    point = tuple(map(int, line[1:].split(",")))
                    self.board.flagSq(point[0], point[1])
                else:
                    point = tuple(map(int, line.split(",")))
                    self.board.click(point[0], point[1])
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
        self.board.pr_wrapper(self.board.pr_endhook)

    def welcome(self):
        print("\nLet's play Minesweeper in Terminal!")
        self.help()
    
    def help(self):
        print("\nUse the following format to enter coordinates!")
        print("> <row>, <column>")
        print("> eg. 1, 1")
        print("\nIf you'd like to flag a coordinate, use the following format!")
        print("If you'd like to UNflag, please enter that same coordinate.")
        print("> f <row>,<column>")
        print("> f 1,1")

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
        # planning to implement actual strategy after midterms

    def autoplay(self):
        t0 = time.time()
        while self.game_count < 100000:
            round = Board(rows=10, cols=10)
            while round.game_state in [GameState.ongoing, GameState.start]:
                guess = self.choose_next(round)
                round.click(guess[0], guess[1])
            if round.game_state == GameState.win:
                self.win_count += 1
            self.game_count += 1
        t1 = time.time()
        timeTaken = int(t1-t0)
        print("\nNumber of games won: " + str(self.win_count) + " out of " + str(self.game_count) + " games.")
        print("Total time to complete the " + str(self.game_count) + "  attempts: " + str(timeTaken)+ " seconds!\n")

def intro():
    print("\n\n ~~~ Welcome to Minesweeper in Terminal! ~~~")
    print("\n\nIf you would like to play, please enter 'p' or 'play'.")
    print("If you would like for a solver to play the game for you, \nplease instead enter 's' or 'solver'.")
    print("If you would like to exit, please enter 'q' or 'quit'.\n\n")

def oops():
    print("\nOops! Invalid option detected! Let's try again.")

if __name__ == "__main__":
    while True:
        game = Game()
        intro()
        raw = input("> ")
        if raw == 'p' or raw == 'play':
            game.play()
        elif raw == 's' or raw == 'solver':
            print("\n\nThis is going to take a while since SOLVER will be\nplaying 100,000 games for you!")
            solver = Solver()
            solver.autoplay()
        elif raw == 'q' or raw == 'quit':
            print("Thanks for playing!\n")
            break
        else:
            oops()
            continue
        if not game.play_again():
            break
