# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size() + 1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, (x, y)):
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


class GreedyPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    # Greedy agent to maximize utility of each available move and decide which to take

    def get_move(self, board):
        choices = board.calc_valid_moves(self.symbol)
        next_score = 0
        move = choices[0]
        for i in choices:
            testboard = board
            testboard.make_move(self.symbol, i)
            score = testboard.calc_scores()
            if score.get(self.symbol) > next_score:
                next_score = score.get(self.symbol)
                move = i

        return move


class MiniMaxPlayer:
    # Minimax agent that calculates 5 levels
    def __init__(self, symbol, beamSearch, killerMove, transposition, qui):
        self.symbol = symbol
        if beamSearch:
            self.beamSearch = True
        if killerMove:
            self.killerMove = True
        if transposition:
            self.transposition = True
        if qui:
            self.qui = True

    def move_score(self, board):
        score = board.calc_scores().get(self.symbol) - board.calc_scores().get(board.get_opponent_symbol(self.symbol))
        size = board.get_size() - 1
        for x in range(0, size):
            for y in range(0, size):
                pos = x, y
                if board.get_symbol_for_position(pos) == self.symbol:
                    if pos == [0, 0] or pos == [0, size] or pos == [size, 0] or pos == [size, size]:
                        score += 12
                    elif x == 0 or x == size or y == 0 or y == size:
                        score += 5
        return score

    # Returns move with min or max score
    def find_max_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] > score:
                score = i[1]
                move = i[0]
        return [move, score]

    def find_min_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] < score:
                score = i[1]
                move = i[0]
        return [move, score]

    def transpositiontable(self, board):
        newtable = TranspositionTable()
        newtable.board_to_table(board)
        return board.seen_board(newtable)

    # Calculate n moves ahead, then use greedy algorithm to assign a value
    def get_move_recursive(self, board, opposite, curr_depth, move):
        if opposite:
            player = self.symbol
        else:
            if self.symbol == "X":
                player = "O"
            else:
                player = "X"

        # Get all moves available
        if self.beamSearch:
            moves = self.beam_search(board)
        else:
            moves = board.calc_valid_moves(player)
        print(moves)
        movesdict = []
        # Base case reached bottom
        # Return max score if opposite = true
        if curr_depth < 1 or len(moves) < 2:
            if len(moves) == 0:
                return [move, self.move_score(board)]
            for i in moves:
                newboard = board
                newboard.make_move(player, i)

                if self.transposition:
                    if self.transpositiontable(newboard):
                        if opposite:
                            return [i, board.calc_scores()[self.symbol]]
                        else:
                            return [i, board.calc_scores()[board.get_opponent_symbol(self.symbol)]]
                    else:
                        score = self.move_score(board)
                        movesdict.append([i, score])
                else:
                    score = self.move_score(board)
                    movesdict.append([i, score])

            # Return move with correct score
            if opposite:
                return self.find_max_score_in_list(movesdict)

            else:
                return self.find_min_score_in_list(movesdict)

        # Call recursive function on board with moves made
        # Send with switched player
        for i in moves:

            newboard = board
            newboard.make_move(player, i)
            if self.transposition:
                if self.transpositiontable(newboard):
                    if opposite:
                        return [i, board.calc_scores()[self.symbol]]
                    else:
                        return [i, board.calc_scores()[board.get_opponent_symbol(self.symbol)]]
                else:
                    move_value = self.get_move_recursive(newboard, not opposite, curr_depth - 1, i)
                    movesdict.append([i, move_value[1]])
            else:
                move_value = self.get_move_recursive(newboard, not opposite, curr_depth - 1, i)
                movesdict.append([i, move_value[1]])

            # Return min or max move depending on symbol
            if opposite:
                return self.find_max_score_in_list(movesdict)
            else:
                return self.find_min_score_in_list(movesdict)

    def beam_search(self, board):
        moves = board.calc_valid_moves(self.symbol)

        if len(moves) > 3:
            size = int(len(moves) / 2)
        else:
            return moves

        bestmoves = []
        scores = {}
        i = 0

        for move in moves:
            newboard = copy.deepcopy(board)
            newboard.make_move(self.symbol, move)
            scores[i] = self.move_score(newboard)
            i += 1

        for i in range(0, size):
            indx = max(scores, key=scores.get)
            bestmoves.append(moves[indx])
            scores.pop(indx)

        return bestmoves

    def get_move(self, board):
        # Check list from recursive function and make move
        moves = board.calc_valid_moves(self.symbol)
        move = self.get_move_recursive(board, True, 200, moves[0])
        return move[0]

class TranspositionTable:

    def __init__(self):
        self.table = {}

    def board_to_table(self, board):
        size = board.get_size()
        current_row = ""
        self.table = {}
        for i in range(size):
            for k in range(size):
                current_pos = [i,k]
                current_symbol = board.get_symbol_for_position(current_pos)
                if current_symbol == "X":
                    current_row += "X"
                elif current_symbol == "O":
                    current_row += "O"
                else:
                    current_row += " "
            self.table[current_row] = True
            current_row = ""

    def seen_board(self, compare_table):
        compare = compare_table.table.keys()
        seen_states = self.table.keys()

        seen = True

        for i in compare:
            if i not in seen_states:
                seen = False
        return seen


class TranspositionTablePlayer:

    def __init__(self, symbol):
        self.symbol = symbol
        self.table = TranspositionTable()

    def move_score(self, board):
        score = board.calc_scores().get(self.symbol) - board.calc_scores().get(board.get_opponent_symbol(self.symbol))
        size = board.get_size() - 1
        for x in range(0, size):
            for y in range(0, size):
                pos = x, y
                if board.get_symbol_for_position(pos) == self.symbol:
                    if pos == [0, 0] or pos == [0, size] or pos == [size, 0] or pos == [size, size]:
                        score += 12
                    elif x == 0 or x == size or y == 0 or y == size:
                        score += 5
        return score

    # Returns move with min or max score
    def find_max_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] > score:
                score = i[1]
                move = i[0]
        return [move, score]

    def find_min_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] < score:
                score = i[1]
                move = i[0]
        return [move, score]

    # Calculate n moves ahead, then use greedy algorithm to assign a value
    def get_move_recursive(self, board, opposite, curr_depth, move):
        if opposite:
            player = self.symbol
        else:
            if self.symbol == "X":
                player = "O"
            else:
                player = "X"

        # Get all moves available
        moves = board.calc_valid_moves(player)
        print(moves)
        movesdict = []

        # Base case reached bottom
        # Return max score if opposite = true
        if curr_depth < 1 or len(moves) < 2:
            if len(moves) == 0:
                return [move, self.move_score(board)]
            for i in moves:
                newboard = board
                newboard.make_move(player, i)

                newtable = TranspositionTable()
                newtable.board_to_table(newboard)

                if self.table.seen_board(newtable):
                    if opposite:
                        return [i, board.calc_scores()[self.symbol]]
                    else:
                        return [i, board.calc_scores()[board.get_opponent_symbol(self.symbol)]]
                else:
                    score = self.move_score(board)
                    movesdict.append([i, score])

            # Return move with correct score
            if opposite:
                return self.find_max_score_in_list(movesdict)

            else:
                return self.find_min_score_in_list(movesdict)

        # Call recursive function on board with moves made
        # Send with switched player
        for i in moves:

            newboard = board
            newboard.make_move(player, i)
            # print("Moving To: ", i)
            newtable = TranspositionTable()
            newtable.board_to_table(newboard)

            if self.table.seen_board(newtable):
                # send to base case if table is already seen
                if opposite:
                    return [i, board.calc_scores()[self.symbol]]
                else:
                    return [i, board.calc_scores()[board.get_opponent_symbol(self.symbol)]]
            else:
                move_value = self.get_move_recursive(newboard, not opposite, curr_depth - 1, i)
                movesdict.append([i, move_value[1]])

                # Return min or max move depending on symbol
                if opposite:
                    return self.find_max_score_in_list(movesdict)
                else:
                    return self.find_min_score_in_list(movesdict)

    def get_move(self, board):
        # Check list from recursive function and make move
        moves = board.calc_valid_moves(self.symbol)
        self.table.board_to_table(board)
        move = self.get_move_recursive(board, True, 200, moves[0])
        return move[0]


class KillerMovePlayer:
    # Minimax agent that calculates 5 levels
    def __init__(self, symbol, beamSearch, killerMove, transposition, qui):
        self.symbol = symbol
        if beamSearch:
            self.beamSearch = True
        if killerMove:
            self.killerMove = True
        if transposition:
            self.transposition = True
        if qui:
            self.qui = True

    def move_score(self, board):
        score = board.calc_scores().get(self.symbol) - board.calc_scores().get(board.get_opponent_symbol(self.symbol))
        size = board.get_size() - 1
        for x in range(0, size):
            for y in range(0, size):
                pos = x, y
                if board.get_symbol_for_position(pos) == self.symbol:
                    if pos == [0, 0] or pos == [0, size] or pos == [size, 0] or pos == [size, size]:
                        score += 12
                    elif x == 0 or x == size or y == 0 or y == size:
                        score += 5
        return score

    # Returns move with min or max score
    def find_max_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] > score:
                score = i[1]
                move = i[0]
        return [move, score]

    def find_min_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] < score:
                score = i[1]
                move = i[0]
        return [move, score]

    # Calculate n moves ahead, then use greedy algorithm to assign a value
    def get_move_recursive(self, board, opposite, curr_depth, move):
        if opposite:
            player = self.symbol
        else:
            if self.symbol == "X":
                player = "O"
            else:
                player = "X"

        # Get all moves available
        if self.beamSearch:
            moves = self.beam_search(board)
        else:
            moves = board.calc_valid_moves(player)
        print(moves)
        movesdict = []
        # Base case reached bottom
        # Return max score if opposite = true
        if curr_depth < 1 or len(moves) < 2:
            if len(moves) == 0:
                return [move, self.move_score(board)]
            for i in moves:
                newboard = board
                newboard.make_move(player, i)
                score = self.move_score(board)
                movesdict.append([i, score])

            # Return move with correct score
            if opposite:
                return self.find_max_score_in_list(movesdict)

            else:
                return self.find_min_score_in_list(movesdict)

        # Call recursive function on board with moves made
        # Send with switched player
        for i in moves:

            newboard = board
            newboard.make_move(player, i)

            # print("Moving To: ", i)
            move_value = self.get_move_recursive(newboard, not opposite, curr_depth - 1, i)
            movesdict.append([i, move_value[1]])

            # Return min or max move depending on symbol
            if opposite:
                return self.find_max_score_in_list(movesdict)
            else:
                return self.find_min_score_in_list(movesdict)

    def beam_search(self, board):
        moves = board.calc_valid_moves(self.symbol)

        if len(moves) > 3:
            size = int(len(moves) / 2)
        else:
            return moves

        bestmoves = []
        scores = {}
        i = 0

        for move in moves:
            newboard = copy.deepcopy(board)
            newboard.make_move(self.symbol, move)
            scores[i] = self.move_score(newboard)
            i += 1

        for i in range(0, size):
            indx = max(scores, key=scores.get)
            bestmoves.append(moves[indx])
            scores.pop(indx)

        return bestmoves

    def killer_move_check(self, board):  # add block moves
        val_moves = board.calc_valid_moves(self.symbol)
        valid_digits = []
        for i in range(1, board.get_size() + 1):
            valid_digits.append(str(i))

            for x in val_moves:
                if x[0] == valid_digits[0] and x[1] == valid_digits[0]:
                    self.killerMove = True
                    return x[0], x[1]

                elif x[0] == valid_digits[0] and x[1] == valid_digits[len(valid_digits) - 1]:
                    self.killerMove = True
                    return x[0], x[1]

                elif x[0] == valid_digits[len(valid_digits) - 1] and x[1] == valid_digits[0]:
                    self.killerMove = True
                    return x[0], x[1]

                elif x[0] == valid_digits[len(valid_digits) - 1] and x[1] == valid_digits[len(valid_digits) - 1]:
                    self.killerMove = True
                    return x[0], x[1]

        self.killerMove = False
        return None

    def get_move(self, board):
        # Check list from recursive function and make move
        possible_move = self.killer_move_check(board)
        if self.killerMove is True:
            return possible_move
        moves = board.calc_valid_moves(self.symbol)
        move = self.get_move_recursive(board, True, 200, moves[0])
        return move[0]


class UltimatePlayer:

    def __init__(self, symbol):
        self.symbol = symbol
        self.table = TranspositionTable()

    def move_score(self, board):
        score = board.calc_scores().get(self.symbol) - board.calc_scores().get(board.get_opponent_symbol(self.symbol))
        size = board.get_size() - 1
        for x in range(0, size):
            for y in range(0, size):
                pos = x, y
                if board.get_symbol_for_position(pos) == self.symbol:
                    if pos == [0, 0] or pos == [0, size] or pos == [size, 0] or pos == [size, size]:
                        score += 12
                    elif x == 0 or x == size or y == 0 or y == size:
                        score += 5
        return score

    # Returns move with min or max score
    def find_max_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] > score:
                score = i[1]
                move = i[0]
        return [move, score]

    def find_min_score_in_list(self, moves_list):
        score = moves_list[0][1]
        move = moves_list[0][0]
        for i in moves_list:
            if i[1] < score:
                score = i[1]
                move = i[0]
        return [move, score]

    # Calculate n moves ahead, then use greedy algorithm to assign a value
    def get_move_recursive(self, board, opposite, curr_depth, move):
        if opposite:
            player = self.symbol
        else:
            if self.symbol == "X":
                player = "O"
            else:
                player = "X"

        # Get all moves available

        moves = self.beam_search(board)

        print(moves)
        movesdict = []
        # Base case reached bottom
        # Return max score if opposite = true
        if curr_depth < 1 or len(moves) < 2:
            if len(moves) == 0:
                return [move, self.move_score(board)]
            for i in moves:
                newboard = board
                newboard.make_move(player, i)

                newtable = TranspositionTable()
                newtable.board_to_table(newboard)

                if self.table.seen_board(newtable):
                    if opposite:
                        return [i, board.calc_scores()[self.symbol]]
                    else:
                        return [i, board.calc_scores()[board.get_opponent_symbol(self.symbol)]]
                else:

                    score = self.move_score(board)
                    movesdict.append([i, score])

            # Return move with correct score
            if opposite:
                return self.find_max_score_in_list(movesdict)

            else:
                return self.find_min_score_in_list(movesdict)

        # Call recursive function on board with moves made
        # Send with switched player
        for i in moves:

            newboard = board
            newboard.make_move(player, i)

            newtable = TranspositionTable()
            newtable.board_to_table(newboard)
            if self.table.seen_board(newtable):
                if opposite:
                    return [i, board.calc_scores()[self.symbol]]
                else:
                    return[i, board.calc_Scores()[board.get_opponent_symbol(self.symbol)]]
            # print("Moving To: ", i)
            else:

                move_value = self.get_move_recursive(newboard, not opposite, curr_depth - 1, i)
                movesdict.append([i, move_value[1]])

            # Return min or max move depending on symbol
            if opposite:
                return self.find_max_score_in_list(movesdict)
            else:
                return self.find_min_score_in_list(movesdict)

    def beam_search(self, board):
        moves = board.calc_valid_moves(self.symbol)

        if len(moves) > 3:
            size = int(len(moves) / 2)
        else:
            return moves

        bestmoves = []
        scores = {}
        i = 0

        for move in moves:
            newboard = copy.deepcopy(board)
            newboard.make_move(self.symbol, move)
            scores[i] = self.move_score(newboard)
            i += 1

        for i in range(0, size):
            indx = max(scores, key=scores.get)
            bestmoves.append(moves[indx])
            scores.pop(indx)

        return bestmoves

    def get_move(self, board):
        # Check list from recursive function and make move
        moves = board.calc_valid_moves(self.symbol)
        move = self.get_move_recursive(board, True, 200, moves[0])
        return move[0]
