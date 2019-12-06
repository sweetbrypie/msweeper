import sys
import os
import time
import random

from gameplay import Board, GameState
from multiprocessing import Pool, Value, Process

""" 
    Command Line / Terminal Version of Minesweeper
    - Created by Angelica Quach
"""


class Game:
    """
    Playable game with user input.
    """

    def __init__(self):
        self.board = Board(rows=10, cols=10)

    def play(self):
        welcome()
        while self.board.game_state in [GameState.ONGOING, GameState.START]:
            self.board.print_board(self.board.print_square)
            try:
                inp = input("> ")
                line = "".join(inp.split())
                if line[0] == "f":
                    point = list(map(int, line[1:].split(",")))
                    self.board.get_square(point[0], point[1]).flag_square()
                else:
                    point = list(map(int, line.split(",")))
                    self.board.click(point[0], point[1])
            except (IndexError, ValueError):
                instructions()
            except KeyboardInterrupt:
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
        if self.board.game_state == GameState.LOSE:
            print("\n\nOh no! Better luck next time! You hit a mine.\n")
            print("Here's the solution!\n")
        else:
            print("\n\nYou didn't hit any of the mines! You win!\n")            
        self.board.print_board(self.board.print_solution)


class Solver:
    """
    Plays 100,000 games, keeping track of time and games won.
    Average win rate is about 90%
    """

    def __init__(self):
        self.game_count = Value('i', 0)
        self.win_count = Value('i', 0)

    def autoplay(self):
        t0 = time.time()
        while self.game_count.value < 1000:
            processes = []
            for _ in range(16):
                p = Process(target=self.play_round)
                processes.append(p)
                p.start()
            for p in processes:
                p.join()
        t1 = time.time()
        minutes = int((t1-t0) / 60)
        seconds = int((t1-t0) % 60)
        print("\nNumber of games won: " + str(self.win_count.value) + " out of " + str(self.game_count.value) + " games.")
        print("Total time to complete the " + str(self.game_count.value) + " attempts: " + str(minutes) + " minutes and " + str(seconds) + " seconds!")
        print("Average win rate: " + str(int(((self.win_count.value / self.game_count.value) * 100))) + "%\n")

    def play_round(self):
        board = Board(rows=10, cols=10)
        current_round = Round(board)
        if current_round.play() == GameState.WIN:
            self.win_count.value += 1
        self.game_count.value += 1


class Round:

    def __init__(self, board):
        self.board = board
        self.possible_squares = set()
        self.make_squares()
        self.found_mines = 0

    def make_squares(self):
        for r in range(10):
            for c in range(10):
                self.possible_squares.add(self.board.get_square(r, c))

    def choose_next(self, round):
        """
        Old random selection strategy.
        """
        return random.choice(self.possible_squares)

    def choose_bestnext(self):
        """
        New optimal selection strategy.
        """
        lowest_percent = 100
        best_choice = None
        remove_squares = set()

        for iSq in self.possible_squares:
            if self.board.is_unknown(iSq):
                percentages = []
                neighbors = self.board.get_neighboring_squares(iSq)

                for jSq in neighbors:
                    if jSq.as_int():
                        count_x = 0
                        count_f = 0
                        check = self.board.get_neighboring_squares(jSq)
                        for kSq in check:
                            if self.board.is_unknown(kSq):
                                count_x += 1
                            elif kSq.flagged:
                                count_f += 1

                        if count_x != 0:
                            percentages.append((jSq.as_int() - count_f) / count_x)

                if len(percentages) == 0:
                    avg_percent = (10 - self.found_mines) / len(self.possible_squares)
                elif percentages.count(1) != 0:
                    avg_percent = 1
                    iSq.flag_square()
                    self.found_mines += 1
                    remove_squares.add(iSq)
                else:
                    sum_so_far = 0
                    for p in percentages:
                        sum_so_far += p
                    avg_percent = sum_so_far / len(percentages)

                if avg_percent < lowest_percent:
                    lowest_percent = avg_percent
                    best_choice = iSq

            else:
                remove_squares.add(iSq)

        best_coords = best_choice.get_coords() if best_choice else (0, 0)

        remove_squares.add(best_choice)
        self.possible_squares = self.possible_squares.difference(remove_squares)

        return best_coords

    def play(self):
        while self.board.game_state in [GameState.ONGOING, GameState.START]:
            guess = self.choose_bestnext()
            self.board.click(guess[0], guess[1])
        return self.board.game_state

def intro():
    print("\n\n ~~~ Welcome to Minesweeper in Terminal! ~~~")
    print("\n\nIf you would like to play, please enter 'p' or 'play'.")
    print("If you would like for a solver to play the game for you, \nplease instead enter 's' or 'solver'.")
    print("If you would like to exit, please enter 'q' or 'quit'.\n\n")


def welcome():
    print("\nLet's play Minesweeper in Terminal!")
    instructions()


def instructions():
    print("\nUse the following format to enter coordinates!")
    print("> <row>, <column>")
    print("> eg. 1, 1")
    print("\nIf you'd like to flag a coordinate, use the following format!")
    print("If you'd like to UNflag, please enter that same coordinate.")
    print("> f <row>, <column>")
    print("> eg. f 1, 1")


def play_again():
    ask = input('Would you like to go again? (y/n): ')
    return ask.lower() == 'y'


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
        if not play_again():
            break
