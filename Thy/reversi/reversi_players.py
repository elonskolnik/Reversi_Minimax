# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons
# license: https://inventwithpython.com/#donate
import random
import copy


class GreedyPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    # Also look at whether a move gives you a corner piece! These are valuable too!

    def greediest_move(self, list_of_moves):
        # keep in mind that list_of_moves will be a dictionary of lists and values
        # like this {[1,2]: 5, [2,3]: 3} where the values represent the tiles that move can flip

        max_move = ""
        max_tiles = 0
        first = True
        for move in list_of_moves:
            current_tiles = list_of_moves[move]
            if first:
                max_move = move
                max_tiles = current_tiles
                first = False
            elif not first:
                if current_tiles > max_tiles:
                    max_move = move
                    max_tiles = current_tiles

        return max_move

    def get_move(self, board):
        possible_moves = board.calc_valid_moves(self.symbol)
        moves_and_tiles = {}
        for i in range(len(possible_moves)):
            tiles_to_flip = len(board.is_valid_move(self.symbol, possible_moves[i]))
            moves_and_tiles[i] = tiles_to_flip
        return possible_moves[self.greediest_move(moves_and_tiles)]


class MinimaxPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    # creates a dictionary of current board state
    def board_to_table(self, board, dict):
        size = board.get_size()
        tile = 'X'
        otherTile = 'O'
        current_string = ""
        for i in size:
            for k in size:
                if board[k][i] == tile:
                    current_string += tile
                elif board[k][i] == otherTile:
                    current_string += otherTile
                else:
                    current_string += " "
                current_string += ', '
            dict[current_string] = True
            current_string = ""
        return dict

    # checks to see if current board state has been seen before
    # returns True if board has been seen
    #         False if board hasn't been seen
    def board_is_seen(self, current, transposition_table):
        different = False
        current_list = current.keys()
        transposition_list = transposition_table.keys()
        for i, k in current_list, transposition_list:
            if not i == k:
                different = True
        return not different


    def max_score(self, states):
        # takes in a list, with list elements [ [[1,2], 3], [[2,3], 4], ...]
        max_score = 0
        max_move = 0
        for i in range(len(states)):
            current_move = states[i][0]
            current_score = states[i][1]
            if current_score > max_score:
                max_score = current_score
                max_move = current_move
        return [max_move, max_score]

    def min_score(self, states):
        min_score = states[0][1]
        min_move = states[0][0]
        for i in range(len(states)):
            current_score = states[i][1]
            current_move = states[i][0]
            if current_score < min_score:
                min_score = current_score
                min_move = current_move
        return [min_move, min_score]

    def get_score(self, board):
        score = board.calc_scores()
        return score[self.symbol] - score[board.get_opponent_symbol(self.symbol)]

    def minimax_move(self, board, my_turn, depth, move):
        if my_turn:
            player = self.symbol
        else:
            player = board.get_opponent_symbol(self.symbol)

        moves = board.calc_valid_moves(player)
        states = []

        if depth == 0 or len(moves) < 2:
            if len(move) == 0:
                return [move, self.get_score(board)]
            else:
                for i in moves:
                    copyboard = copy.deepcopy(board)
                    copyboard.make_move(player, i)
                    states.append([i, self.get_score(copyboard)])
                if my_turn:
                    return self.max_score(states)
                else:
                    return self.min_score(states)

        else:
            for i in moves:
                copyboard = copy.deepcopy(board)
                copyboard.make_move(player,i)
                score = self.minimax_move(copyboard, not my_turn, depth - 1, i)
                states.append([i, score])
            if my_turn:
                return self.max_score(states)
            else:
                return self.min_score(states)

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        move = moves[0][0]
        chosen = self.minimax_move(board, True, 3, move)
        print(chosen)
        return chosen


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))
