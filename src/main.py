from visualization import visualize_board, visualize_start_goals


class game():
    def __init__(self, player_count, simulation_run_count):
        self.player_count = player_count
        self.N = simulation_run_count
        self.board = self.setup_board(player_count=player_count)
        self.starts = [4 for _ in range(player_count)]
        self.safe_house = [[0,0,0,0] for _ in range(player_count)]
    

    def setup_board(self):
        board = [0 for _ in range(15*self.player_count)]
        return board


    def simulate(self):
        visualize_board(self.board)
        visualize_start_goals(self.starts, self.safe_house)
        for simulation_run in range(self.N):
            pass


if __name__ == "__main__":
    game = game(4, 1000)
    game.simulate()