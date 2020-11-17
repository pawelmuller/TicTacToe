'''try:
    from termcolor import cprint, colored
    COLOR_INSTALLED = True
except ModuleNotFoundError:
    COLOR_INSTALLED = False
'''
import os


class TicTacToe:
    def __init__(self):
        self._board = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]
        self._characters = [' ', '◯', '✕']

    def get_possible_moves(self):
        possibilities = []
        for y in range(3):
            for x in range(3):
                if self._board[2-y][x] == 0:
                    possibilities.append((x, y))
        return possibilities if possibilities else False

    def interpret_human_move(self, x, y, player):
        self.do_move(x-1, 3-y, player)

    def do_move(self, x, y, player):
        self._board[y % 3][x % 3] = 1 if player else -1

    def _generate_ascii_board(self):
        """
        Generates and returns tuple of strings that represent the board.
        """
        output = []
        upper_frame = '┏━━━┳━━━┳━━━┓'
        inner_frame = '┣━━━╋━━━╋━━━┫'
        lower_frame = '┗━━━┻━━━┻━━━┛'

        output.append(upper_frame)
        row_counter = 0
        for row in self._board:
            line = ''
            for element in row:
                line += f'┃ {self._characters[element]} '
            row_counter += 1
            line += '┃'
            output.append(line)
            output.append(inner_frame if row_counter < 3 else lower_frame)
        return tuple(output)

    def print_ascii_layout(self, next_player=True):
        """
        Masterpiece of ASCII engineering.
        Not really important.
        """
        output = f'\n\n\n\n{"Tic Tac Toe":^80}\n\n'
        temp = f"It's {'◯' if next_player else '✕'} turn!"
        output += f'{temp:^80}\n\n'
        counter = 0
        for line in self._generate_ascii_board():
            counter += 1
            temp = f'{4 - counter // 2 if counter % 2 == 0 else ""} {line}  '
            output += f'{temp:^80}\n'
        output += f'{"1   2   3":^80}\n\n\n'
        clear_screen()
        print(output)


class Node:
    def __init__(self):
        self._children = []

    def is_terminal(self):
        pass


def minimax():
    pass


def clear_screen():
    os.system('clear||cls')


if __name__ == "__main__":
    game = TicTacToe()
    game.interpret_human_move(3, 3, True)
    game.interpret_human_move(1, 2, False)
    game.print_ascii_layout()
