"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    # use a difference between number of player and opponent moves
    # it is a basic score
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    return float(len(player_moves) - len(opponent_moves))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # use a difference between number of player and opponent moves
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    # additionally check the number of player moves that matches the opponent moves
    # since the number of player and opponent moves is pretty low, we can
    # use simple nested loop here with a complexity O(n^2).
    num_matched_moves = 0
    for player_move in player_moves:
        for opponent_move in opponent_moves:
            if player_move[0] == opponent_move[0] and player_move[1] == opponent_move[1]:
                num_matched_moves += 1

    # the weight of a calcualted metric is an empirical value
    weight = 0.25

    # improve a basis score with weighted metric
    return float(len(player_moves) - len(opponent_moves)) + num_matched_moves * weight


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you shoif game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")uld not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    # use a difference between number of player and opponent moves
    player_moves = game.get_legal_moves(player)
    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)

    # additionally check Manhattan distance to the center of the board of moves
    # for player and its opponent to calculate positional advantages
    player_pos = game.get_player_location(player)
    opponent_pos = game.get_player_location(opponent)
    center_pos = (float(game.height) / 2.0, float(game.width) / 2.0)

    player_dist = abs(player_pos[0] - center_pos[0]) + abs(player_pos[1] - opponent_pos[1])
    opponent_dist = abs(opponent_pos[0] - center_pos[0]) + abs(opponent_pos[1] - opponent_pos[1])

    # the weight of a calcualted advantage is an empirical value
    weight = 0.075

    # improve a basis score with weighted positional advantage
    return float(len(player_moves) - len(opponent_moves)) + \
           float(player_dist - opponent_dist) * weight


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # if there is no legal moves left - return (-1, -1)
        if not game.get_legal_moves():
            return (-1, -1)

        # if the game just started - select center position
        if game.move_count == 0:
            return (int(game.height / 2), int(game.width / 2))

        # do we need to go deeper or are we at the last level already?
        if depth <= 1:
            highest_score = float("-inf")
            best_move = (-1, -1)
            for move in game.get_legal_moves():
                score = self.score(game.forecast_move(move), self)
                if highest_score < score:
                    highest_score = score
                    best_move = move
            return best_move

        # in other cases select maxium from legal moves that has a highest advantage for
        # the player
        return max(game.get_legal_moves(),
                   key=lambda move: self.min_value(game.forecast_move(move), depth - 1))

    def is_game_over(self, game):
        """
        Helper method for minimax algorithm. Checks whether an active player has moves

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        Returns
        -------
        (bool)
            True if an active player does not have moves and the game is over,
            False - otherwise
        """
        return len(game.get_legal_moves()) == 0

    def min_value(self, game, depth):
        """
        Helper method for minimax algorithm. Implements MIN-VALUE as described in the
        minimax algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Current depth is an to search in the game tree before aborting

        Returns
        -------
        (int)
            +inf if the game is over, otherwise - minimum value of over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.is_game_over(game):
            return float("inf")

        lowest_score = float("inf")
        for move in game.get_legal_moves():
            if depth <= 1:
                lowest_score = min(lowest_score, self.score(game.forecast_move(move), self))
            else:
                lowest_score = min(
                    lowest_score,
                    self.max_value(game.forecast_move(move), depth - 1))

        return lowest_score

    def max_value(self, game, depth):
        """
        Helper method for minimax algorithm. Implements MAX-VALUE as described in the
        minimax algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Current depth is an to search in the game tree before aborting

        Returns
        -------
        (int)
            -inf if the game is over, otherwise - maximum value of over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.is_game_over(game):
            return float("-inf")

        highest_score = float("-inf")
        for move in game.get_legal_moves():
            if depth <= 1:
                highest_score = max(highest_score, self.score(game.forecast_move(move), self))
            else:
                highest_score = max(
                    highest_score,
                    self.min_value(game.forecast_move(move), depth - 1))

        return highest_score

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            depth = 1
            while True:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            return best_move  # return the best move, found so far

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # if there is no legal moves left - return (-1, -1)
        if not game.get_legal_moves():
            return (-1, -1)

        # if the game just started - select center position
        if game.move_count == 0:
            return (int(game.height / 2), int(game.width / 2))

        # we could prune nodes also at the beginning.
        # so we start max_value loop here, additionally saving the best move
        highest_score = float("-inf")
        best_move = (-1, -1)
        for move in game.get_legal_moves():
            if depth <= 1:
                score = self.score(game.forecast_move(move), self)
            else:
                score = self.min_value(game.forecast_move(move), depth - 1, alpha, beta)

            # save the new highest score and a move as a best move
            if highest_score < score:
                highest_score = score
                best_move = move

            # return score if it greater or equal to beta - we can skip the subtree of a node
            if highest_score >= beta:
                return best_move

            # update alpha only of we're not at the last level
            if depth > 1:
                alpha = max(alpha, highest_score)

        return best_move

    def is_game_over(self, game):
        """
        Helper method for minimax algorithm. Checks whether an active player has moves

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        Returns
        -------
        (bool)
            True if an active player does not have moves and the game is over,
            False - otherwise
        """
        return len(game.get_legal_moves()) == 0

    def min_value(self, game, depth, alpha, beta):
        """
        Helper method for minimax algorithm. Implements MIN-VALUE as described in the
        minimax algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Current depth is an to search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int)
            +inf if the game is over, otherwise - minimum value of over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.is_game_over(game):
            return float("inf")

        lowest_score = float("inf")
        for move in game.get_legal_moves():
            if depth <= 1:
                lowest_score = min(lowest_score, self.score(game.forecast_move(move), self))
            else:
                lowest_score = min(
                    lowest_score,
                    self.max_value(game.forecast_move(move), depth - 1, alpha, beta))

            # return score if it less or equal to alpha - we can skip the subtree of a node
            if lowest_score <= alpha:
                return lowest_score

            # update beta only of we're not at the last level
            if depth > 1:
                beta = min(beta, lowest_score)

        return lowest_score

    def max_value(self, game, depth, alpha, beta):
        """
        Helper method for minimax algorithm. Implements MAX-VALUE as described in the
        minimax algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Current depth is an to search in the game tree before aborting

        Returns
        -------
        (int)
            -inf if the game is over, otherwise - maximum value of over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.is_game_over(game):
            return float("-inf")

        highest_score = float("-inf")
        for move in game.get_legal_moves():
            if depth <= 1:
                highest_score = max(highest_score, self.score(game.forecast_move(move), self))
            else:
                highest_score = max(
                    highest_score,
                    self.min_value(game.forecast_move(move), depth - 1, alpha, beta))

            # return score if it greater or equal to beta - we can skip the subtree of a node
            if highest_score >= beta:
                return highest_score

            # update alpha only of we're not at the last level
            if depth > 1:
                alpha = max(alpha, highest_score)

        return highest_score
