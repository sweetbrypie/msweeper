import random
import itertools
from enum import Enum

""" 
    Generating playable objects and mechanics for implementation in Minesweeper.py
    - Created by Angelica Quach
"""

class GameState(Enum):
    start = 0
    win = 1
    lose = 2
    ongoing = 3


class Board:
    """ Represents a minesweeper board with squares. """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.game_state = GameState.start
        self.number_of_mines = 0
        self.max_mines = 10
        self.mines_coords = []
        self.__create_squares(self.cols, self.rows)
        self.set_mines(self.cols, self.rows, self.max_mines)

    def click_square(self, row, col):
        """ 
            Click the square and click its
            neighbors which don't have neighboring mines.
        """
        if not self.__valid_square(row, col) or self.__get_square(row, col).clicked:
            return
        square = self.squares[row][col]
        if self.game_state == GameState.start:
            square.mine = False
            for neighbor in square.neighbors():
                neighbor.mine = False
            self.game_state = GameState.ongoing
        if square.mine:
            self.game_state = GameState.lose
            return
        square.clicked = True
        if square.mine_neighbors() == 0:
            for neighbor in square.neighbors():
                if not neighbor.mine:
                    if neighbor.mine_neighbors() == 0:
                        self.click_square(neighbor.row, neighbor.col)
                    neighbor.clicked = True
        if self.__win():
            self.game_state = GameState.win

    def print_board_wrapper(self, print_hook):
        print("\n")
        col_print = "    "
        for i in range(0, self.cols):
            col_print += str(i) + "  "
        print(col_print + "\n")
        for i, row in enumerate(self.squares):
            row_print = str(i) + "  "
            for square in row:
                row_print += print_hook(square)
            print(row_print + "\n")

    def print_board_hook(self, square):
        """
            Prints the board. If a square is clicked, 
            print the number of neighboring mines.
            Else print "X".
        """
        if square.clicked:
            if square.mine_neighbors() == 0:
                return " . "
            return " " + str(square.mine_neighbors()) + " "
        return " X "

    def print_board_end_hook(self, square):
        if square.mine:
            return " M "
        return self.print_board_hook(square)

    def __win(self):
        for row in self.squares:
            for square in row:
                if not square.mine and not square.clicked:
                    return False
        return True

    def __get_square(self, row, col):
        """ Return the square at the given row and column."""
        return self.squares[row][col]

    def __valid_square(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __create_squares(self, cols, rows):
        """
            Create a grid of squares of size rows by cols.
        """
        self.squares = [[Square(self, row, col, mine = False)
                        for col in range(cols)] for row in range(rows)]

    def set_mines(self, row, col, mines):
        for _ in range(mines):
            cell = get_random(row, col)
            while cell in self.mines_coords:
                cell = get_random(row, col)
            self.mines_coords.append(cell)
        for j in self.mines_coords:
            sq_row = j[0]
            sq_col = j[1]
            self.squares[sq_row][sq_col].mine = True
        return self.mines_coords


class Square:
    """
        Represents a single square in the minesweeper board.
        A square may have or may not have a mine, may be clicked or unclicked.
    """
    def __init__(self, board, row, col, mine):
        self.board = board
        self.row = row
        self.col = col
        self.mine = mine
        self.clicked = False

    def mine_neighbors(self):
        return len(list(filter(
            lambda square: square.mine, [self.board.squares[point[0]][point[1]] for point in self.__point_neighbors()]
        )))

    def neighbors(self):
        return [self.board.squares[point[0]][point[1]] for point in self.__point_neighbors()]

    def __point_neighbors(self):
        row_neighbors = list(filter(lambda val: 0 <= val < self.board.rows, [self.row-1, self.row, self.row+1]))
        col_neighbors = list(filter(lambda val: 0 <= val < self.board.cols, [self.col-1, self.col, self.col+1]))
        neighbor_set = set(itertools.product(row_neighbors, col_neighbors))
        neighbor_set.remove((self.row, self.col))
        return list(neighbor_set)


def get_random(row, col):
    a = random.randint(0, row - 1)
    b = random.randint(0, col - 1)
    return a, b
