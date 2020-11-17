class TicTacToe:
    def __init__(self):
        '''self._board = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]'''

        self._board = [[-1, -1, 0],
                       [1, -1, 1],
                       [0, 1, 0]]
        self._characters = [' ', '◯', '✕']

    def generate_ascii_board(self):
        output = []
        upper_frame = "┏━━━┳━━━┳━━━┓"
        inner_frame = "┣━━━╋━━━╋━━━┫"
        lower_frame = "┗━━━┻━━━┻━━━┛"

        output.append(upper_frame)
        row_counter = 0
        for row in self._board:
            line = ""
            for element in row:
                line += f"┃ {self._characters[element]} "
            row_counter += 1
            line += "┃"
            output.append(line)
            output.append(inner_frame if row_counter < 3 else lower_frame)
        return tuple(output)

    def get_possible_moves(self):
        possibilities = []
        for y in range(3):
            for x in range(3):
                if self._board[2-y][x] != 0:
                    possibilities.append((x, y))
        return possibilities if possibilities else False

    def do_move(self, x, y, player):
        self._board[2-y][x] = 1 if player else -1


class Node:
    def __init__(self):
        self._children = []

    def is_terminal(self):
        pass


def minimax():
    pass


if __name__ == "__main__":
    game = TicTacToe()
    print(game.generate_ascii_board())
