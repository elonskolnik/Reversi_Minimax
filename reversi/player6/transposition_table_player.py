from reversi.player6.reversi_players import MiniMaxPlayer


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
            if not i in seen_states:
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

