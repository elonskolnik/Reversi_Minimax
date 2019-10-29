from reversi.player6.reversi_players import MiniMaxPlayer


def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxPlayer(symbol, False, False, False, False)


def get_player_a(symbol):
    """
    :author: Thy Doan Mai le
    :enchancement: Transposition table
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxPlayer(symbol, False, False, True, False)


def get_player_b(symbol):
    """
    :author: Elon Skolnik
    :enchancement: Beam search
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxPlayer(symbol, True, False, False, False)


def get_player_c(symbol):
    """
    :author: Liam Pfaff
    :enchancement: Quiescense to speed up the function
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
                calculates whether or not a given move will have a large change in score,
                if not, it will not recursively calculate that move.
    """
    return MiniMaxPlayer(symbol, False, False, False, True)


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return MiniMaxPlayer(symbol, True, True, True, True)
