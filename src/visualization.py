from copy import deepcopy

def print_at(x: int, value: int):
    print(" " * (x) + str(value), end="")


def visualize_start_goals(starts, goals):
    for player in range(4):
        print(f'{player}: start ({[spot.value for spot in starts[player]]}) saved {[spot.value for spot in goals[player]]}')

def visualize_board(board_ref):
    if len(board_ref) != 60: return
    board = [spot.value for spot in board_ref]
    row_mapping = {
        0: [0, 1, 2, 3, 4, 5],
        1: [6, 59],
        2: [7, 58],
        3: [8, 57],
        4: [9, 56],
        5: [10, 11, 12, 13, 14, 15, 50, 51, 52, 53, 54, 55],
        6: [16, 49],
        7: [17, 48],
        8: [18, 47],
        9: [19, 46],
        10: [20, 21, 22, 23, 24, 25, 40, 41, 42, 43, 44, 45, 46],
        11: [26, 39],
        12: [27, 38],
        13: [28, 37],
        14: [29, 36],
        15: [30, 31, 32, 33, 34, 35],
    }
    left, right = 5, 4
    for row in range(16):
        indices = row_mapping[row]
        match row:
            case 0:
                print(" " * 5 + "".join(str(board[x]) for x in range(0, 6)))
            case 5:
                print(
                    "".join(str(board[x]) for x in range(50, 56))
                    + " " * 4
                    + "".join(str(board[x]) for x in range(10, 16))
                )
                left, right = 0, 14
            case 10:
                print(
                    "".join(str(board[x]) for x in range(45, 39, -1))
                    + " " * 4
                    + "".join(str(board[x]) for x in range(25, 19, -1))
                )
                left, right = 5,4
            case 15:
                print(" " * 5 + "".join(str(board[x]) for x in range(35, 29, -1)))
            case default:
                print_at(left, board[indices[0]])
                print_at(right, board[indices[1]])
                print()
                pass
