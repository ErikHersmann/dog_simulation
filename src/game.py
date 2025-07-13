from visualization import visualize_board, visualize_start_goals
from cards_tokens import spot_base, empty_spot, card_base, card_enum
from random import choice, shuffle
from strategies import strategy_enum, move, move_type
import logging


class game:
    def __init__(self, player_count, simulation_run_count):
        self.logger = logging.getLogger(game.__name__)
        self.player_count = player_count
        self.N = simulation_run_count
        self.setup_board()
        self.setup_card_pool()
        self.starts = [
            [spot_base(player, index) for index in range(4)]
            for player in range(player_count)
        ]
        self.safe_house = [
            [empty_spot() for _ in range(4)] for _ in range(player_count)
        ]
        self.logger.debug(self.generate_start_log_string())
        self.logger.debug(self.generate_safe_house_log_string())
        self.current_round_card_draw_count = 6
        self.current_player_cards = [[] for _ in range(player_count)]
        self.discard_pool = []
        self.current_player = choice(range(player_count))
        self.current_round_dealer = self.current_player
        # TODO: Fix hardcoding
        self.teams = [[0, 2], [1, 3]]
        # TODO: Vary these with testing and take this from the constructor
        self.strategies = [
            strategy_enum.RANDOM,
            strategy_enum.RANDOM,
            strategy_enum.RANDOM,
            strategy_enum.RANDOM,
        ]
        self.player_start_locations = [0, 15, 30, 45]

    def generate_safe_house_log_string(self):
        return "safe house:\n" + "\n".join(
            ",".join([str(spot) for spot in player]) for player in self.safe_house
        )

    def generate_start_log_string(self):
        return "starts:\n" + "\n".join(
            ",".join([str(spot) for spot in player]) for player in self.starts
        )

    def setup_board(self):
        self.board = [empty_spot() for _ in range(15 * self.player_count)]
        self.logger.info(f"Constructed board:\n{[str(spot) for spot in self.board]}")

    def setup_card_pool(self):
        self.card_pool = []
        for enum_variant in card_enum:
            self.card_pool.extend(
                [
                    card_base(len(self.card_pool) + t_index, enum_variant)
                    for t_index in range(6 if enum_variant == card_enum.JOKER else 8)
                ]
            )
        self.logger.info(
            f"Constructed card pool:\n{self.generate_card_pool_log_string()}"
        )

    def simulate(self):
        """One simulation run"""
        visualize_board(self.board)
        visualize_start_goals(self.starts, self.safe_house)
        end = False
        while not end:
            end = self.step()
            self.update_dealer()
        self.logger.info(f"Winning team is {self.get_winning_team()}")

    def get_winning_team(self):
        return "team 1" if self.team_has_won()[1] == 0 else "team 2"
    
    def update_dealer(self):
        self.current_round_dealer = self.current_round_dealer + 1 if self.current_round_dealer < (self.player_count-1) else 0
        self.current_player = self.current_round_dealer
        self.logger.debug(f"Starting next dealing round with the following arguments:\ndealer/player:{self.current_round_dealer}\nnumber of cards:{self.current_round_card_draw_count}")

    def generate_card_pool_log_string(self):
        return [str(card) + f"_{idx}" for idx, card in enumerate(self.card_pool)]

    def generate_discard_pile_log_string(self):
        return [str(card) + f"_{idx}" for idx, card in enumerate(self.discard_pool)]

    def deal_cards(self):
        if len(self.card_pool) < (self.current_round_card_draw_count * self.player_count):
            self.reshuffle_pools()
        for _ in range(self.current_round_card_draw_count):
            for player_idx in range(self.player_count):
                chosen_card_idx = choice(range(len(self.card_pool)))
                self.card_pool[player_idx].append(self.card_pool.pop(chosen_card_idx))
        self.current_round_card_draw_count = (
            self.current_round_card_draw_count - 1 if self.current_round_card_draw_count > 2 else 6
        )

    def reshuffle_pools(self):
        """
        Verify this actually works with the log strings
        """
        self.logger.debug(
            f"Card pool before reshuffling:\n{self.generate_card_pool_log_string()}"
        )
        self.logger.debug(
            f"Discard pile before reshuffling:\n{self.generate_discard_pile_log_string()}"
        )
        shuffle(self.discard_pool)
        self.card_pool = self.discard_pool.extend(self.card_pool)
        self.discard_pool = []
        self.logger.debug(
            f"Card pool after reshuffling:\n{self.generate_card_pool_log_string()}"
        )
        self.logger.debug(
            f"Discard pile after reshuffling:\n{self.generate_discard_pile_log_string()}"
        )

    def team_has_won(self) -> tuple:
        """Checks for a winner
        Returns:
            bool: true if a team has won and false if not
        """
        if all(spot.value != 0 for spot in self.safe_house[0]) and all(
            spot.value != 0 for spot in self.safe_house[2]
        ):
            # Team 1 has won
            return (True, 0)
        if all(spot.value != 0 for spot in self.safe_house[1]) and all(
            spot.value != 0 for spot in self.safe_house[3]
        ):
            # Teams 2 has won
            return (True, 1)
        # Neither team has won
        return (False, -1)

    def make_move(self):
        """Takes into account the current player's hand and the selected strategies (individually for each player so a comparison is possible)
        Moves cards from the hand into the discard piles
        """
        match self.strategies[self.current_player]:
            case strategy_enum.RANDOM:
                self.execute_card(choice(self.get_moves(self.current_player)))
            case default:
                raise NotImplementedError()
            

    def execute_card(self, move: move):
        """Remove card from players hand, move to discard pile, move token and update board"""
        # TODO
        match move.move_type:
            case move_type.MOVE_OUT_FROM_START:
                # Ignore source here
                token = self.get_next_free_token_from_start()
                self.board[self.player_start_locations[self.current_player]] = token
            case move_type.NORMAL:
                temp = self.board[move.source_location]
                self.board[move.source_location] = empty_spot()
                self.board[move.target_location] = temp
            case move_type.MOVE_INTO_SAFE_HOUSE:
                temp = self.board[move.source_location]
                self.board[move.source_location] = empty_spot()
                self.safe_house[self.current_player][move.target_location] = temp
            case move_type.TELEPORT:
                temp = self.board[move.source_location]
                # Target token gets moved to current
                self.board[move.source_location] = self.board[move.target_location]
                # Own token gets move to token
                self.board[move.target_location] = temp
            case move_type.MULTI_MOVE:
                raise NotImplementedError()
        pass

    def advance_player(self) -> bool:
        """Tries to set the current player index to the next player

        Returns:
            bool: True if successful, False if no players can make a move anymore
        """
        end = False
        c_player = self.current_player
        # TODO: Verify this isn't an infinite loop
        while not end:
            c_player = c_player + 1 if c_player < (self.player_count - 1) else 0
            # Check if the next player can actually still move
            if self.player_can_move(self, c_player):
                self.current_player = c_player
                return True
            if c_player == self.current_player:
                # we have looped around and no player could move
                return False
        return False

    def player_can_move(self, player_index: int) -> bool:
        return len(self.get_moves(player_index)) == 0

    def get_moves(self, player_index: int) -> list:
        # TODO
        # Iterate through the entire board until 4-safe_house_count-start_count are found
         
        moves = []

        return moves
    
    def trade(self):
        # TODO: Allow for trading between team members here
        pass

    def step(self) -> bool:
        """Simulated a full "step" of the game, in other words a full hand for each player played out until exhausted or forced to discard"""
        # draw card amount from pool
        self.deal_cards()
        self.trade()
        # trade cards and execute moves until all cards are exhausted (check win conditions/force quits after each move)
        moves_possible = True
        while moves_possible:
            self.make_move()
            if self.team_has_won()[0]:
                return True
            moves_possible = self.advance_player()
            # Advance the current player if there are cards left
        return False
