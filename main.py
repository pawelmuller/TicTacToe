import os
from math import inf
from random import choice
from copy import deepcopy

MIN = -1
MAX = 1
DRAW = 0


class TicTacToe:
    def __init__(self, depth, is_maximizing=True, board=None):
        """
        Initiates the board with empty values.
        """
        self._depth = depth
        self._is_maximizing = is_maximizing
        if board:
            self._board = board
        else:
            self._board = [[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]
        self._characters = [' ', '◯', '✕']
        self._value = 0
        self._player_value = MAX if is_maximizing else MIN

    def get_possible_moves(self):
        """
        Returns list of tuples containing possible moves on the board.
        """
        possibilities = []
        for x in range(3):
            for y in range(3):
                if self._board[y][x] == 0:
                    possibilities.append((x, y))
        return possibilities

    def get_children(self):
        return self._children

    def create_children(self):
        self._children = []
        possibilities = self.get_possible_moves()
        if possibilities:
            for x, y in possibilities:
                new_node = deepcopy(self._board)
                new_node[y][x] = self._player_value
                child = TicTacToe(self._depth, not self._is_maximizing,
                                  new_node)
                self._children.append(child)

    def check_if_over(self):
        """
        Checks whether anyone won the game.
        """
        win_situations = [
            (self._board[0][0], self._board[1][0], self._board[2][0]),
            (self._board[0][1], self._board[1][1], self._board[2][1]),
            (self._board[0][2], self._board[1][2], self._board[2][2]),
            (self._board[0][0], self._board[0][1], self._board[0][2]),
            (self._board[1][0], self._board[1][1], self._board[1][2]),
            (self._board[2][0], self._board[2][1], self._board[2][2]),
            (self._board[0][0], self._board[1][1], self._board[2][2]),
            (self._board[2][0], self._board[1][1], self._board[0][2]),
        ]

        if (MIN, MIN, MIN) in win_situations:
            return True
        if (MAX, MAX, MAX) in win_situations:
            return True
        else:
            return False

    def is_terminal(self):
        """
        Checks whether node is terminal.
        Returns proper boolean.
        """
        if self.check_if_over() or not self.get_possible_moves():
            return True
        return False

    def get_heuristic_value(self):
        """
        Calculates heuristic value of node.
        """
        if self.check_if_over():
            if self._is_maximizing:
                return inf
            else:
                return -1 * inf
        else:
            value = 0
            heuristics = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]

            for i in range(3):
                for j in range(3):
                    value += self._board[i][j] * heuristics[i][j]
            return value

    def ask_ai_for_move(self, player):
        """
        Gets the best possible move from AI.
        """
        if player == MAX:
            is_max = True
        else:
            is_max = False

        self._value = minimax(self, self._depth, is_max)
        self._board = self.get_best_move(is_max)

    def get_best_move(self, is_maximizing):
        values = []
        children = self.get_children()
        for child in children:
            value = minimax(child, 6, self._is_maximizing)
            values.append(value)

        m = max(values) if is_maximizing else min(values)
        indexes = [i for i, j in enumerate(values) if j == m]
        best_children = []
        for index in indexes:
            best_children.append(children[index])

        return choice(best_children)._board

    def ask_player_for_move(self, player):
        """
        Asks player for coordinates, then proceeds to performing the move.
        """
        print(f'{"What is your move?":^80}')
        print(f'{"Type in each value and press Enter:":^80}')
        while True:
            x = self.ask_player_for_value('x')
            y = self.ask_player_for_value('y')
            x, y = self.interpret_human_move(x, y)
            if (x, y) in self.get_possible_moves():
                break
            else:
                print(f'{"That place is already taken! Try again:":^80}')
        self.do_move(x, y, player)

    @staticmethod
    def ask_player_for_value(value_name):
        """
        Asks player for integer value between 1 and 3
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

    @staticmethod
    def interpret_human_move(x, y):
        """
        Converts human-friendly coordinates into computer-friendly ones,
        as indexes start from 0.
        """
        return x-1, 3-y

    def do_move(self, x, y, player):
        """
        Performs the move.
        """
        self._board[y][x] = player

    def generate_ascii_board(self):
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

    def print_ascii_layout(self, message=''):
        """
        Masterpiece of ASCII engineering.
        Not really important.
        """
        output = f'\n\n\n\n{"Tic Tac Toe":^80}\n\n'
        output += f'{message:^80}\n\n'
        counter = 0
        for line in self.generate_ascii_board():
            counter += 1
            temp = f'{4 - counter // 2 if counter % 2 == 0 else ""} {line}  '
            output += f'{temp:^80}\n'
        output += f'{"1   2   3":^80}\n\n\n'
        clear_screen()
        print(output)

    def print_ingame_layout(self, next_player):
        """
        Prints in-game layout.
        """
        message = f"It's {self._characters[next_player]} turn!"
        self.print_ascii_layout(message)

    def print_result_layout(self, result):
        """
        Prints results.
        """
        if result == MAX:
            message = '◯ won!'
        elif result == MIN:
            message = '✕ won!'
        else:
            message = "It's a draw!"
        self.print_ascii_layout(message)

    def conduct_game(self, player_1, player_2):
        """
        Conducts game.
        Allows players to perform their moves.
        """
        while True:
            self.print_ingame_layout(MIN)
            player_1(MIN)

            if self.check_if_over():
                return MIN
            if not self.get_possible_moves():
                return DRAW

            self.print_ingame_layout(MAX)
            player_2(MAX)

            if self.check_if_over():
                return MAX
            if not self.get_possible_moves():
                return DRAW

    def start(self, is_singleplayer=True, is_maximizing=True):
        """
        Starts the game.
        Allows AI to play in singleplayer mode.
        """
        if is_singleplayer:
            result = self.conduct_game(self.ask_player_for_move,
                                       self.ask_ai_for_move)
        else:
            result = self.conduct_game(self.ask_player_for_move,
                                       self.ask_player_for_move)
        self.print_result_layout(result)


def minimax(node, depth, maximizing_player):
    node.create_children()
    if depth == 0 or node.is_terminal():
        node.value = node.get_heuristic_value()
        return node.value
    if maximizing_player:
        node.value = -inf
        for child in node._children:
            node.value = max(node.value, minimax(child, depth-1, False))
        return node.value
    else:
        node.value = inf
        for child in node._children:
            node.value = min(node.value, minimax(child, depth-1, True))
        return node.value


def clear_screen():
    """
    Clears the screen both in Terminal and Command Prompt.
    Tested on macOS and Windows.
    """
    os.system('clear||cls')


if __name__ == "__main__":
    game = TicTacToe(6)
    game.start(True)
