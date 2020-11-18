import os
from math import inf

O_value = True
X_value = False


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
                if self._board[y][x] == 0:
                    possibilities.append((x, y))
        return possibilities if possibilities else False

    def is_the_game_over(self):
        """
        Checks whether a player has won the game.
        """
        if not self._check_diagonals():
            if not self._check_columns():
                if not self._check_rows():
                    return False
        return True

    def _check_diagonals(self):
        """
        Checks whether any diagonal belongs to one player.
        """
        if abs(self._board[0][0] + self._board[1][1] + self._board[2][2]) == 3:
            return True
        if abs(self._board[0][2] + self._board[1][1] + self._board[2][0]) == 3:
            return True
        return False

    def _check_columns(self):
        """
        Checks whether any column belongs to one player.
        """
        for column in range(3):
            sum = 0
            for row in range(3):
                sum += self._board[row][column]
            if abs(sum) == 3:
                return True
        return False

    def _check_rows(self):
        """
        Checks whether any row belongs to one player.
        """
        for row in range(3):
            sum = 0
            for column in range(3):
                sum += self._board[row][column]
            if abs(sum) == 3:
                return True
        return False

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
                value = int(input(f'{f"{value_name} = ":>41}'))
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

    def _print_ascii_layout(self, message=''):
        """
        Masterpiece of ASCII engineering.
        Not really important.
        """
        output = f'\n\n\n\n{"Tic Tac Toe":^80}\n\n'
        output += f'{message:^80}\n\n'
        counter = 0
        for line in self._generate_ascii_board():
            counter += 1
            temp = f'{4 - counter // 2 if counter % 2 == 0 else ""} {line}  '
            output += f'{temp:^80}\n'
        output += f'{"1   2   3":^80}\n\n\n'
        clear_screen()
        print(output)

    def _print_ingame_layout(self, next_player):
        """
        Prints in-game layout.
        """
        message = f"It's {'◯' if next_player else '✕'} turn!"
        self._print_ascii_layout(message)

    def _print_result_layout(self, result):
        """
        Prints results.
        """
        if result == 1:
            message = '◯ won!'
        elif result == -1:
            message = '✕ won!'
        else:
            message = "It's a draw!"
        self._print_ascii_layout(message)

    def _conduct_game(self, player_1, player_2):
        """
        Conducts game.
        Allows players to perform their moves.
        """
        while True:
            self._print_ingame_layout(True)
            player_1(True)

            if self.is_the_game_over():
                return 1
            if not self.get_possible_moves():
                return 0

            self._print_ingame_layout(False)
            player_2(False)

            if self.is_the_game_over():
                return -1
            if not self.get_possible_moves():
                return 0

    def start(self, is_singleplayer=True):
        """
        Starts the game.
        Allows AI to play in singleplayer mode.
        """
        if is_singleplayer:
            result = self._conduct_game(self._ask_player_for_move,
                                        self._ask_AI_for_move)
        else:
            result = self._conduct_game(self._ask_player_for_move,
                                        self._ask_player_for_move)
        self._print_result_layout(result)


class Node:
    def __init__(self):
        self._children = []

    def is_terminal(self):
        pass

    def get_heuristic_value(self):
        pass

    def get_children(self):
        pass


def minimax(node, depth, maximizingPlayer):
    if depth == 0 or node.is_terminal():
        return node.get_heuristic_value()
    if maximizingPlayer:
        value = -inf
        for child in node.get_children():
            value = max(value, minimax(child, depth-1, False))
        return value
    else:
        value = inf
        for child in node.get_children():
            value = min(value, minimax(child, depth-1, True))
        return value


def clear_screen():
    """
    Clears the screen both in Terminal and Command Prompt.
    Tested on macOS and Windows.
    """
    os.system('clear||cls')


if __name__ == "__main__":
    game = TicTacToe()
    game.start(False)
