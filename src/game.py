from visualization import visualize_board, visualize_start_goals
from cards_tokens import spot_base, empty_spot, card_base, card_enum
from random import choice, shuffle
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
        self.logger.info("starts:\n"+"\n".join(",".join([str(spot) for spot in player]) for player in self.starts))
        self.safe_house = [[empty_spot() for _ in range(4)] for _ in range(player_count)]
        self.logger.info(
            "safe house:\n"+"\n".join(",".join([str(spot) for spot in player]) for player in self.safe_house)
        )
        self.current_card_draw_count = 6
        self.current_player_cards = [[] for _ in range(player_count)]
        self.discard_pool = []
        self.current_player = choice(range(player_count))
        self.current_round_dealer = self.current_player

    def setup_board(self):
        self.board = [empty_spot() for _ in range(15 * self.player_count)]
        self.logger.info(f'Constructed board:\n{[str(spot) for spot in self.board]}')

    def setup_card_pool(self):
        self.card_pool = []
        for enum_variant in card_enum:
            self.card_pool.extend([card_base(len(self.card_pool) + t_index, enum_variant) for t_index in range(6 if enum_variant == card_enum.JOKER else 8)])
        self.logger.info(f'Constructed card pool:\n{[str(card) + f"_{idx}" for idx, card in enumerate(self.card_pool)]}')

    def simulate(self):
        """One simulation run
        """
        # TODO
        visualize_board(self.board)
        visualize_start_goals(self.starts, self.safe_house)

    def deal_cards(self):
        if len(self.card_pool) < (self.current_card_draw_count * self.player_count):
            self.reshuffle_pools()
        for _ in range(self.current_card_draw_count):
            for player_idx in range(self.player_count):
                chosen_card_idx = choice(range(len(self.card_pool)))
                self.card_pool[player_idx].append(self.card_pool.pop(chosen_card_idx))
        if self.current_card_draw_count > 2:
            self.current_card_draw_count -= 1
        else:
            self.current_card_draw_count = 6

    def reshuffle_pools(self):
        """
        Verify this actually works
        """
        shuffle(self.discard_pool)
        self.card_pool = self.discard_pool.extend(self.card_pool)
        self.discard_pool = []

    def player_has_won(self) -> int:
        """Checks for a winner

        Returns:
            int: The index of the winning player or -1 if none found
        """
        # TODO
        pass

    def make_move(self):
        """Takes into account the current player's hand and the selected strategies (individually for each player so a comparison is possible)
        Moves cards from the hand into the discard piles
        """
        # TODO
        pass
    
    def execute_card(self):
        """Remove card from players hand, move to discard pile, move token and update board
        """
        # TODO
        pass

    def advance_player(self) -> bool:
        # TODO
        end = False
        c_player = self.current_player
        while not end:
            """Avoid infinite loop here"""
            if c_player < self.player_count-1 : 
                c_player += 1
            else:
                c_player = 0
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
        moves = []
        
        return moves

    def step(self):
        """Simulated a full "step" of the game, in other words a full hand for each player played out until exhausted or forced to discard
        """
        # draw card amount from pool
        self.deal_cards()
        # trade cards and execute moves until all cards are exhausted (check win conditions/force quits after each move)
        moves_possible = True
        while moves_possible:

            self.make_move()
            if self.player_has_won(): return 
            moves_possible = self.advance_player()
            # Advance the current player if there are cards left
