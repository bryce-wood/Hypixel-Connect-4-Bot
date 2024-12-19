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

    # if at the desired depth, we want the win
    if depth == 0:
        win = bo.find_win(board)
        if win == 2:
            return 100, mem
        elif win == 1:
            return (-100), mem
        else:
            return 0, mem

    valid_positions = bo.find_valid_positions(board)
    for pos in valid_positions:
        # Set the X or O on the board
        test_board = bo.set_position(board, pos, player)

        win = bo.find_win(test_board)
        if win == 0:
            if test_board not in mem:
                mem[test_board] = (make_boards(test_board, depth - 1, mem)[0], depth - 1)
            else: 
                if mem[test_board][1] < depth - 1:
                    mem[test_board] = (make_boards(test_board, depth - 1, mem)[0], depth - 1)
                return mem[test_board][0], mem
        elif win == 2:
            return 100, mem
        else: # win == 1
            return (-100), mem

    return 0, mem  # Default return if no valid moves left


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
        if value[0] == 100:
            bo.print_board(key)
            print(key, value)
    #print("Num boards:", len(boards))
    #save_boards_to_pickle(boards)
    print(f"Time taken: {t.time() - st} seconds")
