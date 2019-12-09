import pytest
from gameplay import Board, GameState

class TestClick:
    
    def test_setup_board(self):
        """
        Tests if the apppropriate dimensions have been set.
        Also checks to make sure no squares have been clicked.
        """

        board = Board(rows=10, cols=10, number_of_mines=0)

        rows, cols = board.get_dimensions()
        assert (rows, cols) == (10,10)

        for row in range(rows):
            for col in range(cols):
                assert not board.get_square(row, col).clicked

    def test_click_square(self):
        """
        Tests if a square's CLICK property is updating correctly.
        Also checks that neighboring squares with 0 mine neighbors are also clicked.
        """

        board = Board(rows=10, cols=10, number_of_mines=0)
        assert not board.get_square(0,0).clicked
        assert not board.get_square(9,9).clicked

        board.click(0,0)
        assert board.get_square(0,0).clicked
        assert board.get_square(9,9).clicked

    def test_hit_mine_first(self):
        """
        Tests if manually setting mines works.
        Tests if hitting a mine on the first square removes the mine from the game.
        """

        board = Board(rows=10, cols=10, number_of_mines=1)
        more_mines = [(0,0), (0,1), (0,2), (1,1)]
        board.set_mines(more_mines)

        assert not board.get_square(0,1).clicked
        assert board.get_square(0,1).mine

        board.click(0,1)
        assert board.get_square(0,1).clicked
        assert not board.get_square(0,1).mine
        assert board.game_state == GameState.ONGOING

    def test_hit_mine_second(self):
        """
        Tests if manually setting mines works.
        Tests if hitting a mine on the first square causes you to lose the game.
        """

        board = Board(rows=10, cols=10, number_of_mines=1)
        more_mines = [(0,0), (0,1), (0,2), (1,1)]
        board.set_mines(more_mines)

        assert not board.get_square(0,0).clicked
        assert board.get_square(0,0).mine

        board.click(0,1)
        assert board.game_state == GameState.ONGOING

        board.click(0,0)
        assert board.game_state == GameState.LOSE

    

class TestFlag:

    def test_flagging(self):
        """
        Tests whether the flagging method updates correctly.
        """

        board = Board(rows=10, cols=10, number_of_mines=0)
        square = board.get_square(0,0)

        assert not square.flagged

        square.flag_square()
        assert square.flagged

    def test_unflagging(self):
        """
        Tests whether the flagging method is removed correctly.
        """

        board = Board(rows=10, cols=10, number_of_mines=0)
        square = board.get_square(0,0)

        assert not square.flagged

        square.flag_square()
        assert square.flagged

        square.flag_square()
        assert not square.flagged

