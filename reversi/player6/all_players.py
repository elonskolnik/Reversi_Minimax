from reversi.player6.reversi_players import MiniMaxPlayer, TranspositionTablePlayer


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
    return TranspositionTablePlayer(symbol)


def get_player_b(symbol):
    """
    :author: Elon Skolnik
    :enchancement: Beam search
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxPlayer(symbol, True, False, False, False)


def get_player_c(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


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
    pass
