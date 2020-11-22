import os
from math import inf
from random import shuffle
from copy import deepcopy

MIN = -1
MAX = 1
DRAW = 0


class TicTacToe:
    def __init__(self, depth, is_maximizing=True, board=None):
        """
        Initiates the object with given parameters.
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

    def __repr__(self):
        return f"{str(self._board)}; {self._value}"

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
        """
        Returns node's children.
        """
        return self._children

    def create_children(self):
        """
        Creates a child node for all empty places on board.
        """
        self._children = []
        possibilities = self.get_possible_moves()
        if possibilities:
            for x, y in possibilities:
                new_node = deepcopy(self._board)
                new_node[y][x] = MAX if self._is_maximizing else MIN
                child = TicTacToe(self._depth, not self._is_maximizing,
                                  new_node)
                self._children.append(child)

    def get_winner(self):
        """
        Checks whether a player has won the game.
        """
        if not self.check_diagonals():
            if not self.check_columns():
                if not self.check_rows():
                    return False
                else:
                    return self.check_rows()
            else:
                return self.check_columns()
        else:
            return self.check_diagonals()

    def check_diagonals(self):
        """
        Checks whether any diagonal belongs to one player.
        """
        if abs(self._board[0][0] + self._board[1][1] + self._board[2][2]) == 3:
            return self._board[0][0]
        if abs(self._board[0][2] + self._board[1][1] + self._board[2][0]) == 3:
            return self._board[0][2]
        return False

    def check_columns(self):
        """
        Checks whether any column belongs to one player.
        """
        for column in range(3):
            sum = 0
            for row in range(3):
                sum += self._board[row][column]
            if abs(sum) == 3:
                return self._board[0][column]
        return False

    def check_rows(self):
        """
        Checks whether any row belongs to one player.
        """
        for row in range(3):
            sum = 0
            for column in range(3):
                sum += self._board[row][column]
            if abs(sum) == 3:
                return self._board[row][0]
        return False

    def is_terminal(self):
        """
        Checks whether node is terminal.
        Returns proper boolean.
        """
        if self.get_winner() != 0 or not self.get_possible_moves():
            return True
        return False

    def get_heuristic_value(self):
        """
        Calculates heuristic value of node.
        """
        if self.is_terminal():
            winner = self.get_winner()
            if winner:
                return winner * inf
            else:
                return 0
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
            self._is_maximizing = True
        else:
            self._is_maximizing = False

        self._value = minimax(self, self._depth, self._is_maximizing)
        self._board = self.get_best_move()

    def get_best_move(self):
        """
        Shuffles children (to keep randomness). Then orders them from the best
        to the worst (depending on maxi- or minimalizing), then chooses the
        first one to be glorified.
        """
        shuffle(self._children)
        sorted_children = sorted(self._children,
                                 key=lambda child: child._value,
                                 reverse=self._is_maximizing)
        return sorted_children[0]._board

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

            if self.get_winner() == MIN:
                return MIN
            if not self.get_possible_moves():
                return DRAW

            self.print_ingame_layout(MAX)
            player_2(MAX)

            if self.get_winner() == MAX:
                return MAX
            if not self.get_possible_moves():
                return DRAW

    def start(self, is_singleplayer=True, does_ai_start=False):
        """
        Starts the game.
        Allows AI to play in singleplayer mode.
        """
        if is_singleplayer:
            if does_ai_start:
                result = self.conduct_game(self.ask_ai_for_move,
                                           self.ask_player_for_move)
            else:
                result = self.conduct_game(self.ask_player_for_move,
                                           self.ask_ai_for_move)
        else:
            result = self.conduct_game(self.ask_player_for_move,
                                       self.ask_player_for_move)
        self.print_result_layout(result)


def minimax(node, depth, maximizing_player):
    node.create_children()
    if depth == 0 or node.is_terminal():
        node._value = node.get_heuristic_value()
        return node._value
    elif maximizing_player:
        node._value = -inf
        for child in node._children:
            node._value = max(node._value, minimax(child, depth-1, False))
        return node._value
    else:
        node._value = inf
        for child in node._children:
            node._value = min(node._value, minimax(child, depth-1, True))
        return node._value


def clear_screen():
    """
    Clears the screen both in Terminal and Command Prompt.
    Tested on macOS and Windows.
    """
    os.system('clear||cls')


if __name__ == "__main__":
    game = TicTacToe(4)
    game.start(True, False)
