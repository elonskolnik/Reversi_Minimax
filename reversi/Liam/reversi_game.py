# Written by Toby Dragon

import copy
from datetime import datetime
from reversi.reversi_board import ReversiBoard
from reversi.reversi_players import HumanPlayer, GreedyPlayer, MiniMaxPlayer
from reversi.reversi_players import RandomComputerPlayer


class ReversiGame:

    def __init__(self, player1, player2, show_status=True, board_size=8):
        self.player1 = player1
        self.player2 = player2
        self.board = ReversiBoard(board_size)
        self.decision_times = {self.player1.symbol: 0, self.player2.symbol: 0}
        self.show_status = show_status
        self.play_game()

    def play_game(self):
        if self.show_status:
            self.board.draw_board()
        while self.board.game_continues():
            self.play_round()
        if self.show_status:
            print("Game over, Final Scores:")
            print_scores(self.board.calc_scores())

    def play_round(self):
        start = datetime.now()
        self.play_move(self.player1)
        self.decision_times[self.player1.symbol] += (datetime.now()-start).total_seconds()
        start = datetime.now()
        self.play_move(self.player2)
        self.decision_times[self.player2.symbol] += (datetime.now()-start).total_seconds()

    def play_move(self, player):
        if self.board.calc_valid_moves(player.symbol):
            chosen_move = player.get_move(copy.deepcopy(self.board))
            if not self.board.make_move(player.symbol, chosen_move):
                print("Error: invalid move made")
            elif self.show_status:
                self.board.draw_board()
                print_scores(self.board.calc_scores())
        elif self.show_status:
            print(player.symbol, "can't move.")

    def calc_winner(self):
        scores = self.board.calc_scores()
        if scores[self.player1.symbol] > scores[self.player2.symbol]:
            return self.player1.symbol
        if scores[self.player1.symbol] < scores[self.player2.symbol]:
            return self.player2.symbol
        else:
            return "TIE"

    def get_decision_times(self):
        return self.decision_times


def print_scores(score_map):
    for symbol in score_map:
        print(symbol, ":", score_map[symbol], end="\t")
    print()


def compare_players(player1, player2):
    game_count_map = {player1.symbol: 0, player2.symbol: 0, "TIE": 0}
    time_elapsed_map = {player1.symbol: 0, player2.symbol: 0}
    isFirst = False
    for i in range(1, 200):
        if i % 100 == 0:
            print(i, "games finished")

        #Alternates who gets to go first
        if isFirst:
            game = ReversiGame(player1, player2, show_status=False)
            isFirst = False
        else:
            game = ReversiGame(player2, player1, show_status=False)
            isFirst = True

        game_count_map[game.calc_winner()] += 1
        decision_times = game.get_decision_times()
        for symbol in decision_times:
            time_elapsed_map[symbol] += decision_times[symbol]
    print(game_count_map)
    print(time_elapsed_map)


def main():
    #ReversiGame(HumanPlayer("X"), RandomComputerPlayer("O"))
    #compare_players(RandomComputerPlayer("X"), RandomComputerPlayer("O"))
    print("Random Vs. Greedy")
    #compare_players(RandomComputerPlayer("O"), GreedyPlayer("X"))
    print("Random Vs. MiniMax")
    #compare_players(RandomComputerPlayer("O"), MiniMaxPlayer("X"))
    print("Greedy Vs. MiniMax")
    #compare_players(GreedyPlayer("X"), MiniMaxPlayer("O"))
    print("MiniMax Vs. MiniMax")
    compare_players(MiniMaxPlayer("X"), MiniMaxPlayer("O"))
    print("Greedy Vs. Greedy")
    #compare_players(GreedyPlayer("O"), GreedyPlayer("X"))
    print("Random Vs. Random")
    #compare_players(RandomComputerPlayer("O"), RandomComputerPlayer("X"))


if __name__ == "__main__":
    main()
