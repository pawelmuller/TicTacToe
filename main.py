import os
from math import inf
from random import choice
from copy import deepcopy

MIN = -1
MAX = 1
DRAW = 0


class TicTacToe:
    def __init__(self):
        """
        Initiates the board with empty values.
        """
        self._board = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]
        self._characters = [' ', '◯', '✕']

    def get_possible_moves(self, board=None):
        """
        Returns list of tuples containing possible moves on the board.
        """
        if not board:
            board = self._board
        possibilities = []
        for y in range(3):
            for x in range(3):
                if board[y][x] == 0:
                    possibilities.append((x, y))
        return possibilities if possibilities else False

    def check_if_wins(self, player_value, board=None):
        if not board:
            board = self._board
        win_situations = [
            (board[0][0], board[1][0], board[2][0]),
            (board[0][1], board[1][1], board[2][1]),
            (board[0][2], board[1][2], board[2][2]),
            (board[0][0], board[0][1], board[0][2]),
            (board[1][0], board[1][1], board[1][2]),
            (board[2][0], board[2][1], board[2][2]),
            (board[0][0], board[1][1], board[2][2]),
            (board[2][0], board[1][1], board[0][2]),
        ]

        if (player_value, player_value, player_value) in win_situations:
            return True
        else:
            return False

    def _ask_AI_for_move(self, player):
        node = Node(deepcopy(self._board), player)
        x, y = node.get_best_move()
        self._do_move(x, y, player)

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
        self._board[y][x] = player

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
        message = f"It's {self._characters[next_player]} turn!"
        self._print_ascii_layout(message)

    def _print_result_layout(self, result):
        """
        Prints results.
        """
        if result == MAX:
            message = '◯ won!'
        elif result == MIN:
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
            self._print_ingame_layout(MIN)
            player_1(MIN)

            if self.check_if_wins(MIN):
                return MIN
            if not self.get_possible_moves():
                return DRAW

            self._print_ingame_layout(MAX)
            player_2(MAX)

            if self.check_if_wins(MAX):
                return MAX
            if not self.get_possible_moves():
                return DRAW

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
    def __init__(self, node, player, coordinates=None):
        self.node = node
        self.player = player
        self.coordinates = coordinates
        self.maximizing_player = True if player == MAX else MIN

    def evaluate(self, board):
        if TicTacToe.check_if_wins(self, MAX, board):
            return MAX
        elif TicTacToe.check_if_wins(self, MIN, board):
            return MIN
        else:
            return DRAW

    def is_terminal(self):
        """
        Checks whether node is terminal.
        Returns proper boolean.
        """
        if TicTacToe.check_if_wins(self, self.player, self.node):
            return True
        if not TicTacToe.get_possible_moves(self, self.node):
            return True
        return False

    def get_heuristic_value(self):
        """
        Calculates heuristic value of node.
        """
        value = 0
        heuristics = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]

        for i in range(3):
            for j in range(3):
                value += self.node[i][j] * heuristics[i][j]
        return value

    def get_children(self):
        children = []

        for x, y in TicTacToe.get_possible_moves(self, self.node):
            new_node = deepcopy(self.node)
            new_node[x][y] = self.player
            new_player = MIN if self.player == MAX else MAX
            child = Node(new_node, new_player, (x, y))
            children.append(child)

        return children

    def get_best_move(self):
        depth = len(TicTacToe.get_possible_moves(self, self.node))
        values = []
        children = self.get_children()
        for child in children:
            value = minimax(child, depth-1, self.maximizing_player)
            values.append(value)

        m = max(values)
        indexes = [i for i, j in enumerate(values) if j == m]
        best_children = []
        for index in indexes:
            best_children.append(children[index])

        return choice(best_children).coordinates


def minimax(node, depth, maximizing_player):
    if depth == 0 or node.is_terminal():
        return node.get_heuristic_value()
    if maximizing_player:
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
    game.start(True)
