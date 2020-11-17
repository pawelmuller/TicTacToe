class TicTacToe:
    def __init__(self):
        '''self._board = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]'''

        self._board = [[2, 2, 0],
                       [1, 2, 1],
                       [0, 1, 0]]
        self._characters = [' ', '◯', '✕']

    def print_board(self):
        output = ""
        upper_frame = "┏━━━┳━━━┳━━━┓\n"
        inner_frame = "┣━━━╋━━━╋━━━┫\n"
        bottom_frame = "┗━━━┻━━━┻━━━┛\n"

        output += upper_frame
        row_counter = 0
        for row in self._board:
            for element in row:
                output += f"┃ {self._characters[element]} "
            row_counter += 1
            output += f"┃\n{inner_frame if row_counter < 3 else bottom_frame}"
        print(f"{output:^80}")


def minimax():
    pass


if __name__ == "__main__":
    game = TicTacToe()
    game.print_board()
