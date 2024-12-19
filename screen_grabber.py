import cv2
import numpy as np
from PIL import ImageGrab, Image
from typing import List, Tuple

# Capture the screen (or a portion of it) using ImageGrab
def capture_screen(region=None):
    screen = ImageGrab.grab(bbox=region)  # bbox=(left, top, right, bottom)
    screen.save('screen.png')  # Optional: Save the screenshot for debugging
    return np.array(screen)

# Define absolute coordinates for the subregions (computerColor and userColor)
computerColor = (1048, 543, 1078, 578)  # Absolute coordinates for computerColor (left, top, right, bottom)
userColor = (1478, 543, 1508, 578)  # Absolute coordinates for userColor (left, top, right, bottom)

# Define the grid region, adjusted to exclude the computerColor and userColor areas
grid_region = (1043, 428, 1520, 748)

# Capture the main image (grid)
main_image = capture_screen(region=grid_region)

# Convert the image from PIL format to OpenCV format (BGR)
main_image_cv = cv2.cvtColor(main_image, cv2.COLOR_RGB2BGR)

# Convert the grid image to grayscale (this is important for template matching)
main_image_gray = cv2.cvtColor(main_image_cv, cv2.COLOR_BGR2GRAY)

# Extract the subregions (computerColor and userColor) from the screen using the absolute coordinates
computer_color_region = main_image[computerColor[1] - grid_region[1]:computerColor[3] - grid_region[1], 
                                   computerColor[0] - grid_region[0]:computerColor[2] - grid_region[0]]

user_color_region = main_image[userColor[1] - grid_region[1]:userColor[3] - grid_region[1], 
                               userColor[0] - grid_region[0]:userColor[2] - grid_region[0]]

# Convert subregions to grayscale (template matching works better in grayscale)
computer_color_gray = cv2.cvtColor(computer_color_region, cv2.COLOR_RGB2GRAY)
user_color_gray = cv2.cvtColor(user_color_region, cv2.COLOR_RGB2GRAY)

# Perform template matching for computerColor
res_computer = cv2.matchTemplate(main_image_gray, computer_color_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.99  # Match threshold, adjust as needed
computer_matches = np.where(res_computer >= threshold)

# Perform template matching for userColor
res_user = cv2.matchTemplate(main_image_gray, user_color_gray, cv2.TM_CCOEFF_NORMED)
user_matches = np.where(res_user >= threshold)

# Now, restrict the search to only the region between computerColor and userColor
# The area of interest is between the right edge of computerColor and the left edge of userColor
left_limit = computerColor[2] - grid_region[0]  # Right edge of computerColor region (relative to grid)
right_limit = userColor[0] - grid_region[0] - 1  # Left edge of userColor region (relative to grid) minus 1 to exclude it

# Filter out matches that fall outside the allowed region (only between computerColor and userColor)
def filter_matches(matches, left_limit, right_limit):
    filtered_matches = []
    for pt in zip(*matches[::-1]):  # (x, y) -> (row, column)
        x, y = pt
        if left_limit <= x <= right_limit:
            filtered_matches.append(pt)
    return filtered_matches

# Filter out computer and user color matches
computer_matches_filtered = filter_matches(computer_matches, left_limit, right_limit)
user_matches_filtered = filter_matches(user_matches, left_limit, right_limit)

# let the computer be 'x' and the user be 'o'

rows = 6
cols = 7
universalGrid = [['b' for _ in range(cols)] for _ in range(rows)]

def print_matches_grid(computer_matches: List[Tuple[int, int]], user_matches: List[Tuple[int, int]], grid_width: int, grid_height: int, image_width: int, image_height: int, left_limit: int):
    # Create an empty grid
    grid = [['.'] * grid_width for _ in range(grid_height)]
    
    # Calculate cell width and height
    cell_width = image_width // grid_width
    cell_height = image_height // grid_height
    
    # Place computer matches
    for x, y in computer_matches:
        grid_x = (x - left_limit) // cell_width
        grid_y = y // cell_height
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            grid[grid_y][grid_x] = 'x'
            universalGrid[grid_y][grid_x] = 'x'
    
    # Place user matches
    for x, y in user_matches:
        grid_x = (x - left_limit) // cell_width
        grid_y = y // cell_height
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            grid[grid_y][grid_x] = 'o'
            universalGrid[grid_y][grid_x] = 'o'
    
    # Print the grid
    print("Game Board Grid (CPU: x, User: o):")
    for i, row in enumerate(grid):
        print(f"{6-i} {' '.join(row)}")
    print("  " + " ".join(str(chr(i+97)) for i in range(grid_width)))

image_width = right_limit - left_limit + 1
image_height = main_image_gray.shape[0]
#print_matches_grid(computer_matches_filtered, user_matches_filtered, 7, 6, image_width, image_height, left_limit)

#print("\n")
#for row in range(len(universalGrid)):
#    print(universalGrid[row])
#    print("")