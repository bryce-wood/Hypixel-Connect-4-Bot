import random

def set_position(board, position, value):
    # Direct clear and set in one step
    return (board & ~(3 << (position * 2))) | (value << (position * 2))

# Get the value at a position on the board
def get_position(board, position):
    # Shift right to get the two relevant bits and mask them to get the value (00, 01, or 10)
    return (board >> (position * 2)) & 3  # 3 is 11 in binary, masking out the 2 bits

def extract_player_bitboards(board):
    player1_board = 0  # Bitboard for Player 1 (01)
    player2_board = 0  # Bitboard for Player 2 (10)
    
    for pos in range(42):  # Iterate through all 42 positions (7x6 board)
        piece = (board >> (pos * 2)) & 3  # Get the 2 bits at the position
        
        if piece == 1:  # Player 1's piece (01)
            player1_board |= (1 << pos)  # Set the corresponding bit in player 1's board
        elif piece == 2:  # Player 2's piece (10)
            player2_board |= (1 << pos)  # Set the corresponding bit in player 2's board
            
    return player1_board, player2_board

# returns 1 if player 1 has a winning position, 2 if player 2 has a winning position, 0 if neither
def find_win(board):
    win_masks = [ # masks for all valid wins
                # horizontal wins
                0xf,0x1e,0x3c,0x78,0x780,0xf00,0x1e00,0x3c00,0x3c000,0x78000,0xf0000,0x1e0000,0x1e00000,0x3c00000,0x7800000,0xf000000,0xf0000000,0x1e0000000,0x3c0000000,0x780000000,0x7800000000,0xf000000000,0x1e000000000,0x3c000000000,
                # vertical wins
                0x204081,0x10204080,0x810204000,0x408102,0x20408100,0x1020408000,0x810204,0x40810200,0x2040810000,0x1020408,0x81020400,0x4081020000,0x2040810,0x102040800,0x8102040000,0x4081020,0x204081000,0x10204080000,0x8102040,0x408102000,0x20408100000,
                # diagonal (\) wins
                0x1010101,0x2020202,0x4040404,0x8080808,0x80808080,0x101010100,0x202020200,0x404040400,0x4040404000,0x8080808000,0x10101010000,0x20202020000,
                # diagonal (/) wins
                0x208208,0x410410,0x820820,0x1041040,0x10410400,0x20820800,0x41041000,0x82082000,0x820820000,0x1041040000,0x2082080000,0x4104100000
                ]
    player1_board, player2_board = extract_player_bitboards(board)
    
    # Check if any win mask matches for Player 1
    for mask in win_masks:
        if (player1_board & mask) == mask:
            return 1  # Player 1 wins
    
    # Check if any win mask matches for Player 2
    for mask in win_masks:
        if (player2_board & mask) == mask:
            return 2  # Player 2 wins
    
    return 0  # No win found


def print_board(board):
    for row in range(5, -1, -1):  # 6 rows
        row_str = str(row) + " "
        for col in range(7):  # 7 columns
            position = row * 7 + col  # Calculate position index in bitboard
            value = get_position(board, position)
            if value == 0:
                row_str += " . "  # Empty spot
            elif value == 1:
                row_str += " X "  # Player 1 piece
            elif value == 2:
                row_str += " O "  # Player 2 piece
            elif value == 3:
                row_str += " # "  # Highlight piece
        print(row_str)
    print("  " + "-" * 21)  # Separator for the bottom of the board
    print("   A  B  C  D  E  F  G ")  # Column labels

def make_random_board(depth):
    board = 0
    for _ in range(depth):
        valid_positions = find_valid_positions(board)
        position = random.choice(valid_positions)
        board = set_position(board, position, _%2 + 1)
    return board

# Find all valid positions to put an X or O on the board
def find_valid_positions(board):
    # a position is valid if it is in a blank spot on row 0 or has a non-blank spot below it
    valid_positions = []
    # Predefined bottom row mask (all 0s)
    bottom_row_mask = 0b0000000000000000000000000000111111111111111111111111111111111111
    
    # Apply the mask to the board to get the bottom row values
    bottom_row = board & bottom_row_mask
    
    occupied_positions = []
    for col in range(7):  # Iterate through the columns
        # Check if the bottom row value is empty (value is 0)
        if (bottom_row >> (col * 2)) & 3 == 0:
            valid_positions.append(col)
        else:
            occupied_positions.append(col)
    
    # Check above the occupied positions until it is an empty spot or out of range
    for col in occupied_positions:
        for row in range(1,6):
            position = row * 7 + col  # Calculate position index in bitboard
            value = get_position(board, position)
            if value == 0:
                valid_positions.append(position)
                break  # Break the loop once an empty spot is found
        
    return valid_positions