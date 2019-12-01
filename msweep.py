import sys, os
from gameplay import Board, GameState, Square
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
        print("> f <row>, <column>")
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
                self.possible_coords.append(cell)

    def cornered(self, round, neighboring_squares):
        for n in neighboring_squares:
            nSq = round.getSq(n[0], n[1])

            edge = 0
            if round.pr_hook(nSq) == ' 1 ':
                edge += 1

            if edge >= 2:
                return True
            return False


    def choose_next(self, round):
        """
        Old random selection strategy.
        """
        return random.choice(self.possible_coords)

    def choose_bestnext(self, round):
        """
        New optimal selection strategy.
        """
        board_percentage = []
        
        for i in self.possible_coords:
            iSq = round.getSq(i[0], i[1])
            
            if round.pr_hook(iSq) == ' X ':
                sq_percentage = []
                surroundings = iSq.point_neighbors()
  
                for j in surroundings:
                    jSq = round.getSq(j[0], j[1])

                    if round.as_int(jSq) != None:
                        count_X = 0
                        count_F = 0
                        check = jSq.point_neighbors()

                        for k in check:
                            kSq = round.getSq(k[0], k[1])
                            if round.pr_hook(kSq) == ' X ':
                                count_X += 1
                            elif round.pr_hook(kSq) == ' f ':
                                count_F += 1  
                        if count_X != 0:
                            sq_percentage.append((jSq.mine_neighbors() - count_F)/ count_X)

                avg_percent = 0
                if len(sq_percentage) == 0:
                    avg_percent = 0.8
                elif sq_percentage.count(1) != 0:
                    avg_percent = 1
                    round.flagSq(i[0], i[1])
                else:
                    sum_so_far = 0
                    for p in sq_percentage:
                        sum_so_far += p
                    avg_percent = sum_so_far / len(sq_percentage)
            
                board_percentage.append(avg_percent)

            else:
                board_percentage.append(100)

        sorted_percentages = board_percentage.copy()
        sorted_percentages.sort()

        best_choice = board_percentage.index(sorted_percentages[0])

        return self.possible_coords[best_choice]

    def autoplay(self):
        t0 = time.time()
        while self.game_count < 100000:                      # runtime was about 3 hours and 15 minutes
            round = Board(rows=10, cols=10)
            while round.game_state in [GameState.ongoing, GameState.start]:
                # guess = self.choose_next(round)            # original guess random cell strategy
                guess = self.choose_bestnext(round)          # new guess best cell strategy
                round.click(guess[0], guess[1])
            if round.game_state == GameState.win:
                self.win_count += 1
            self.game_count += 1
        t1 = time.time()
        time_taken = int(t1-t0)
        print("\nNumber of games won: " + str(self.win_count) + " out of " + str(self.game_count) + " games.")
        print("Total time to complete the " + str(self.game_count) + " attempts: " + str(time_taken)+ " seconds!")
        print("Average win rate: " + str(((self.win_count / self.game_count) *100)) + "%\n")

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
