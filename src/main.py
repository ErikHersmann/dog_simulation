from visualization import visualize_board, visualize_start_goals

def setup_board(player_count: int):
    board = [0 for _ in range(15*player_count)]
    mapping = {player_idx: player_idx*16 for player_idx in range(player_count)}
    safe_house = [[0,0,0,0] for _ in range(player_count)]
    
    return board


def simulation(n: int):
    board = setup_board(4)
    starts, goals = [4, 4, 4, 4], [[0, 0, 0, 0] for _ in range(4)]
    visualize_board(board)
    visualize_start_goals(starts, goals)
    for simulation_run in range(n):
        pass


if __name__ == "__main__":
    simulation(1000)
