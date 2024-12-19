import board_operations as bo
import time as t
import random
import concurrent.futures
import pickle

boards = dict()
st = t.time()

# This is the function that will process each board state
def make_boards(board=0, depth=15, mem={}):
    player = 1 if depth % 2 == 1 else 2
    opponent = 2 if player == 1 else 1

    # if at the desired depth, we want the win
    if depth <= 0:
        return 0, mem

    valid_positions = bo.find_valid_positions(board)
    best_score = -float('inf') if player == 1 else float('inf')
    best_mem = mem

    for pos in valid_positions:
        # Set the X or O on the board
        test_board = bo.set_position(board, pos, player)

        win = bo.find_win(test_board)
        if win == player:
            score = 100 if player == 2 else -100
            return score, mem

        # Check if the opponent can win on their next move
        opponent_wins = False
        opponent_positions = bo.find_valid_positions(test_board)
        for opp_pos in opponent_positions:
            opponent_board = bo.set_position(test_board, opp_pos, opponent)
            if bo.find_win(opponent_board) == opponent:
                opponent_wins = True
                break

        if not opponent_wins:
            if test_board not in mem:
                score, new_mem = make_boards(test_board, depth - 1, mem)
                mem[test_board] = (score, depth - 1)
            else:
                if mem[test_board][1] < depth - 1:
                    score, new_mem = make_boards(test_board, depth - 1, mem)
                    mem[test_board] = (score, depth - 1)
                else:
                    score = mem[test_board][0]
                    new_mem = mem

            if player == 1:
                if score > best_score:
                    best_score = score
                    best_mem = new_mem
            else:
                if score < best_score:
                    best_score = score
                    best_mem = new_mem

    # If no valid move prevents opponent's win, make any valid move
    if best_score == -float('inf') or best_score == float('inf'):
        pos = valid_positions[0]
        test_board = bo.set_position(board, pos, player)
        score, new_mem = make_boards(test_board, depth - 1, mem)
        best_score = score
        best_mem = new_mem

    return best_score, best_mem  # Return the best score and memory


# Wrapper function for parallel processing
# depth of 17 uses 20gb of memory, so i would not recommend going over that or risk crashing
def parallel_make_boards(starting_board=0, depth=9, mem={}):
    valid_positions = bo.find_valid_positions(starting_board)

    # Using ProcessPoolExecutor to run the board generation in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(make_boards, bo.set_position(starting_board, pos, 1), depth - 1, mem=mem) for pos in valid_positions]

        # Wait for all the threads to finish and get their results
        for future in concurrent.futures.as_completed(futures):
            results = future.result()  # Optionally collect results
            for result in results:
                if type(result) != type(0):
                    boards.update(result)

def save_boards_to_pickle(boards, filename="boards.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(boards, file)
    print(f"Boards saved to {filename}")

def load_boards_from_pickle(filename="boards.pkl"):
    try:
        with open(filename, "rb") as file:
            boards = pickle.load(file)
        print(f"Boards loaded from {filename}")
        return boards
    except FileNotFoundError:
        print(f"{filename} not found, starting with an empty board set.")
        return {}

if __name__ == '__main__':
    boards = load_boards_from_pickle()
    parallel_make_boards()
    for key, value in boards.items():
        if value[0] != 0:
            bo.print_board(key)
            print(key, value)
    #print("Num boards:", len(boards))
    #save_boards_to_pickle(boards)
    print(f"Time taken: {t.time() - st} seconds")
