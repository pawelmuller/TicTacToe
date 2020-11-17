import os


class TicTacToe:
    def __init__(self):
        """
        Initiates the board with empty values.
        """
        self._board = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]
        self._characters = [' ', '◯', '✕']

    def get_possible_moves(self):
        """
        Returns list of tuples containing possible moves on the board.
        """
        possibilities = []
        for y in range(3):
            for x in range(3):
                if self._board[2-y][x] == 0:
                    possibilities.append((x, y))
        return possibilities if possibilities else False

    def _ask_player_for_move(self, player):
        """
        Asks player for coordinates, then proceeds to performing the move.
        """
        print(f'{"What is your move?":^80}')
        print(f'{"Type in each value and press Enter:":^80}')
        while True:
            x = self._ask_player_for_value('x')
            y = self._ask_player_for_value('y')
            x, y = self._interpret_human_move(x, y)
            if (x, y) in self.get_possible_moves():
                break
            else:
                print(f'{"That place is already taken! Try again:":^80}')
        self._do_move(x, y, player)

    def _ask_player_for_value(self, value_name):
        """
        Asks player for integer balue between 1 and 3
        as long as it is correct.
        """
        while True:
            try:
                value = int(input(f'{f"{value_name} = ":>40}'))
                if value < 1 or value > 3:
                    raise ValueError
                else:
                    return value
            except ValueError:
                print(f'{"Oops! The input must be an int from 1 to 3!":^80}')

    def _interpret_human_move(self, x, y):
        """
        Converts human-friendly coordinates into computer-friendly ones,
        as indexes start from 0.
        """
        return x-1, 3-y

    def _do_move(self, x, y, player):
        """
        Performs the move.
        """
        self._board[y][x] = 1 if player else -1

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

    def start(self, is_singleplayer=True, is_impossible=False):
        pass


class Node:
    def __init__(self):
        self._children = []

    def is_terminal(self):
        pass


def minimax():
    pass


def clear_screen():
    """
    Clears the screen both in Terminal and Command Prompt.
    Tested on macOS and Windows.
    """
    os.system('clear||cls')


if __name__ == "__main__":
    game = TicTacToe()
    x, y = game._interpret_human_move(3, 3)
    game._do_move(x, y, True)
    game.print_ascii_layout()
    game._ask_player_for_move(False)
    game.print_ascii_layout()
    game._ask_player_for_move(True)
    game.print_ascii_layout()
    game._ask_player_for_move(False)
    game.print_ascii_layout()
