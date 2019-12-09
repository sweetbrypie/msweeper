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

class Solver:
    """
    Plays a changable amount of games, keeping track of time and games won.
    """

    def __init__(self):
        self.game_count = Value('i', 0)
        self.win_count = Value('i', 0)
        self.max_games = 1000

    def autoplay(self):
        t0 = time.time()
        while self.game_count.value < self.max_games:
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


def dimensions():
    print("\nEnter the dimensions of the board as ROWS, COLS (i.e. '20, 30').")
    print("Type 'd' for default dimensions of 10 rows by 10 cols.")
    print("For better visual gameplay, we recommend using the default dimensions.\n\n")
    try:
        inp = input("> ")
        line = "".join(inp.split())
        if line[0] == "d":
            return 10, 10
        else:
            size = list(map(int, line.split(",")))
            if size[0] <= 0 or size[1] <= 0:
                raise ValueError
            return size[0], size[1]
    except (ValueError):
        print("\nInvalid input, setting board as default dimensions.")
        return 10, 10


def number_of_mines(rows, cols):
    print("\nEnter the number of mines to randomly distribute across your board (i.e. '15').")
    print("Type 'd' for default mine amount of 10.\n\n")
    try:
        inp = input("> ")
        if int(inp) < 0 or int(inp) > rows*cols:
            raise ValueError
        return int(inp)
    except (ValueError):
        default_mines = int(0.1*rows*cols)
        print("\nInvalid input, distributing " + str(default_mines) + " mines randomly.")
        return default_mines


def play():
    """
    Playable game of Minesweeper.
    """

    num_rows, num_cols = dimensions()
    num_mines = number_of_mines(int(num_rows), int(num_cols))

    welcome()

    board = Board(rows=int(num_rows), cols=int(num_cols), number_of_mines=int(num_mines))

    while board.game_state in [GameState.ONGOING, GameState.START]:
        board.print_board(board.print_square)
        try:
            inp = input("> ")
            line = "".join(inp.split())
            if line[0] == "f":
                point = list(map(int, line[1:].split(",")))
                board.get_square(point[0], point[1]).flag_square()
            else:
                point = list(map(int, line.split(",")))
                board.click(point[0], point[1])
        except (IndexError, ValueError):
            oops()
            instructions()
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
    if board.game_state == GameState.LOSE:
        print("\n\nOh no! Better luck next time! You hit a mine.\n")
        print("Here's the solution!\n")
    else:
        print("\n\nYou didn't hit any of the mines! You win!\n")            
    board.print_board(board.print_solution)


def play_again():
    ask = input('Would you like to go again? (y/n): ')
    return ask.lower() == 'y'


def oops():
    print("\nOops! Invalid option detected! Let's try again.")

if __name__ == "__main__":
    while True:
        intro()
        raw = input("> ")
        if raw == 'p' or raw == 'play':
            play()
        elif raw == 's' or raw == 'solver':
            solver = Solver()
            print("\n\nThis might take a while since SOLVER will be\nplaying " + str(solver.max_games) + " games for you!")
            solver.autoplay()
        elif raw == 'q' or raw == 'quit':
            print("Thanks for playing!\n")
            break
        else:
            oops()
            continue
        if not play_again():
            break
