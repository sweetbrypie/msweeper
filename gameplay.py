import random
import itertools
from enum import Enum

""" 
    Generating playable objects and mechanics for implementation in Minesweeper.py
    - Created by Angelica Quach
"""


class GameState(Enum):
    START = 0
    WIN = 1
    LOSE = 2
    ONGOING = 3


class SquareType(Enum):
    UNKNOWN = ' X '
    FLAG = ' f '
    EMPTY = ' . '


class Board:
    """ 
        Creates a playable board that can be clicked.
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.game_state = GameState.START
        self.number_of_mines = 0
        self.max_mines = 10
        self.mines_coords = []
        self.make_board(self.cols, self.rows)
        self.set_mines(self.cols, self.rows, self.max_mines)

    def click(self, row, col):
        """ 
            Clicks the square and, if the square does not contain a mine, also clicks its neighbors that do not contain mines.
        """
        if not self.is_valid_square(row, col) or self.get_square(row, col).clicked:
            return
        square = self.squares[row][col]
        if self.game_state == GameState.START:
            square.mine = False
            for neighbor in self.get_neighboring_squares(square):
                neighbor.mine = False
            self.game_state = GameState.ONGOING
        if square.mine:
            self.game_state = GameState.LOSE
            return
        square.clicked = True
        if square.mine_neighbors() == 0:
            for neighbor in self.get_neighboring_squares(square):
                if not neighbor.mine:
                    if neighbor.mine_neighbors() == 0:
                        self.click(neighbor.row, neighbor.col)
                    neighbor.clicked = True
        if self.winner():
            self.game_state = GameState.WIN

    def print_board(self, print_square):
        """
        Prints the border of the board, showing the numbers associated with row and column.
        """
        print("\n")
        col_print = "    "
        for i in range(0, self.cols):
            col_print += str(i) + "  "
        print(col_print + "\n")
        for i, row in enumerate(self.squares):
            row_print = str(i) + "  "
            for square in row:
                row_print += print_square(square)
            print(row_print + "\n")

    def print_square(self, square):
        """
            If the square does not neighbor mines, return a dot.
            If it does, return the number of mines it neighbors.
            If the square is flagged, return f.
            Else, return an unclicked square X.
        """
        if square.clicked:
            if square.mine_neighbors() == 0:
                return " . "
            return " " + str(square.mine_neighbors()) + " "
        elif square.flagged:
            return " f "
        return " X "
        return None

    def print_solution(self, square):
        if square.mine:
            return " M "
        return self.print_square(square)

    def get_dimensions(self):
        return self.rows, self.cols

    def winner(self):
        """
        Establishes the win condition, where all the remaining unclicked squares
        on the board must be mines.

        !!  Does  not implement the secondary win mechanic where a player can win
        a game by correctly flagging all mines.
        """
        for row in self.squares:
            for square in row:
                if not square.mine and not square.clicked:
                    return False
        return True

    def get_square(self, row, col):
        """ Return the square at the given row and column."""
        return self.squares[row][col]

    def is_unknown(self, square):
        return self.print_square(square) == SquareType.UNKNOWN.value

    def get_neighboring_squares(self, square):
        assert type(square) is Square
        r, c = square.get_coords()
        row_neighbors = list(filter(lambda val: 0 <= val < self.rows, [r - 1, r, r + 1]))
        col_neighbors = list(filter(lambda val: 0 <= val < self.cols, [c - 1, c, c + 1]))
        neighbor_set = set(itertools.product(row_neighbors, col_neighbors))
        neighbor_set.remove((r, c))
        neighboring_squares = []
        for coord in neighbor_set:
            neighboring_squares.append(self.get_square(coord[0], coord[1]))
        return neighboring_squares

    def is_valid_square(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def make_board(self, cols, rows):
        """
            Create a grid of squares of size rows by cols.
        """
        self.squares = [[Square(self, row, col)
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
        A square may have a mine (or not), may be clicked (or not), and may be flagged (or not).
    """
    def __init__(self, board, row, col):
        self.board = board
        self.row = row
        self.col = col
        self.mine = False
        self.flagged = False
        self.clicked = False

    def mine_neighbors(self):
        # filter takes in a function and a list of elements and only returns the elements that
        # return true through the function
        # in this case, filtering out all neighbors of self that are NOT mines
        return len(list(filter(
            lambda square: square.mine, self.board.get_neighboring_squares(self)
        )))

    def get_coords(self):
        return self.row, self.col

    def as_int(self):
        if self.clicked:
            return self.mine_neighbors()

    def flag_square(self):
        self.flagged = True

def get_random(row, col):
    a = random.randint(0, row - 1)
    b = random.randint(0, col - 1)
    return a, b
