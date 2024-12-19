import time
import board_operations as bo
   
def make_boards(depth, start_board=None):
    boards = []
    # if depth is negative, return nothing
    if (depth < 0):
        return None
    # the 0 depth board is just the start board, otherwise it is the same process
    d0_boards = []
    if start_board != None:
        boards.append([start_board])
    else:
        # make the 0 depth boards
        for i in range(7):
            board = 0
            board = bo.set_position(board, i, 1)
            d0_boards.append(board)
        boards.append(d0_boards)
    
    for i in range(1, depth):
        depth_boards = []
        for board in boards[i-1]:
            valid_positions = bo.find_valid_positions(board)
            for position in valid_positions:
                boardcpy = bo.set_position(boardcpy, position, i%2 + 1)
                depth_boards.append(boardcpy)
        boards.append(depth_boards)
    return boards

# evaluates the position 100 to -100, giving 100 to O winning next move, and -100 to X winning next move
def evaluate_position(board, depth=7, memo=None):
    if memo is None:
        memo = {}

    # If the board and depth combination is already in the memo, return the cached score
    if (board, depth) in memo:
        return memo[(board, depth)]

    # Check if there is a winner
    winner = find_win(board)
    if winner != 0:
        if winner == 1:
            return -100  # Player X wins (we don't care about X's score)
        elif winner == 2:
            return 100  # Player O wins (maximizing player)

    # If depth is 0 or no winner, return 0 (draw or end of search)
    if depth == 0:
        return 0

    best_score = -float('inf')  # We are only maximizing for Player O

    valid_positions = bo.find_valid_positions(board)

    # Loop through all valid positions and evaluate the resulting board
    for position in valid_positions:
        new_board = bo.set_position(board, position, 2)  # Always make Player O's move (player 2)
        score = evaluate_position(new_board, depth - 1, memo)

        best_score = max(best_score, score)

    memo[(board, depth)] = best_score
    
    return best_score

# will suggest the next move that best favors player 2 (assumes its player 2's turn)
# will return a number 0-6 (0b000 - 0b110) to represent which column to put O
def next_move(board, depth=7):
    # idea: what if i generate every board, starting from with the most pieces played down, since it is clear what to play when there is
    # only one move, or a win in 1 for either side, and once you have all the boards, go one down, pick the board that leads to the best
    # board after it
    pass

def main():
    st = time.time() # get the start time
    
    #offense_test_board = 0x810205081
    #defense_test_board = 0x10204081
    #print_board(offense_test_board)
    #print_board(defense_test_board)
    
    #rand_board = make_random_board(5)
    board = 0x108041020
    
    print_board(board)
    #print(hex(rand_board))
    #print(evaluate_position(board, 7))
    
    et = time.time() # get the end time
    # calculate time taken and print it
    print("Time taken: " + str(et-st) + " seconds")

if __name__ == "__main__":
    main()

# will use a dictionary (hash map) to store the boards