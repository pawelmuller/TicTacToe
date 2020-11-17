class TicTacToe:
    def __init__(self):
        '''self._board = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]'''

        self._board = [[-1, -1, 0],
                       [1, -1, 1],
                       [0, 1, 0]]
        self._characters = [' ', '◯', '✕']

    def print_board(self):
        output = ""
        upper_frame = "┏━━━┳━━━┳━━━┓\n"
        inner_frame = "┣━━━╋━━━╋━━━┫\n"
        lower_frame = "┗━━━┻━━━┻━━━┛\n"

        output += upper_frame
        row_counter = 0
        for row in self._board:
            for element in row:
                output += f"┃ {self._characters[element]} "
            row_counter += 1
            output += f"┃\n{inner_frame if row_counter < 3 else lower_frame}"
        print(output)

    def get_possible_moves(self):
        possibilities = []
        for y in range(3):
            for x in range(3):
                if self._board[2-y][x] != 0:
                    possibilities.append((x, y))
        return possibilities if possibilities else False


class Node:
    def __init__(self):
        self._children = []

    def is_terminal(self):
        pass


def minimax():
    pass


if __name__ == "__main__":
    game = TicTacToe()
    game.print_board()

