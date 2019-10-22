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
        for i in range(1, board.get_size()+1):
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
    #Greedy agent to maximize utility of each available move and decide which to take

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
    #Minimax agent that calculates 5 levels
    def __init__(self, symbol):
        self.symbol = symbol

    def move_score(self, board):
        score = board.calc_scores()

        #Subtract opponent from agent symbol
        myscore = score.get(self.symbol)
        if self.symbol == "X":
            opponentscore = score.get("O")
        else:
            opponentscore = score.get("X")
        return myscore - opponentscore

    #Returns move with min or max score
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

    #Calculate n moves ahead, then use greedy algorithm to assign a value
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
                score = self.move_score(board)
                movesdict.append([i, score])


            #Return move with correct score
            if opposite:
                return self.find_max_score_in_list(movesdict)

            else:
                return self.find_min_score_in_list(movesdict)

        #Call recursive function on board with moves made
        #Send with switched player
        for i in moves:

            newboard = board
            newboard.make_move(player, i)
            print("Moving To: ", i)
            move_value = self.get_move_recursive(newboard, not opposite, curr_depth - 1, i)
            movesdict.append([i, move_value[1]])

            #Return min or max move depending on symbol
            if opposite:
                return self.find_max_score_in_list(movesdict)
            else:
                return self.find_min_score_in_list(movesdict)

    def get_move(self, board):
        #Check list from recursive function and make move
        moves = board.calc_valid_moves(self.symbol)
        move = self.get_move_recursive(board, True, 200, moves[0])
        return move[0]

