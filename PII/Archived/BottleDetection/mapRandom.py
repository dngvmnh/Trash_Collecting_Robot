import random
def generate_randomized_path():
    # Define the grid or map for navigation
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
     # Get the dimensions of the grid
    rows = len(grid)
    cols = len(grid[0])
     # Start position of the robot
    start = (0, 0)
     # End position of the robot
    end = (rows-1, cols-1)
     # Randomized path planning
    path = [start]
    current = start
    while current != end:
        # Generate random valid neighbor
        neighbors = []
         # Check all four directions (up, down, left, right)
        if current[0] > 0 and grid[current[0]-1][current[1]] == 0:
            neighbors.append((current[0]-1, current[1]))  # Up
        if current[0] < rows-1 and grid[current[0]+1][current[1]] == 0:
            neighbors.append((current[0]+1, current[1]))  # Down
        if current[1] > 0 and grid[current[0]][current[1]-1] == 0:
            neighbors.append((current[0], current[1]-1))  # Left
        if current[1] < cols-1 and grid[current[0]][current[1]+1] == 0:
            neighbors.append((current[0], current[1]+1))  # Right
        if neighbors:
            next_pos = random.choice(neighbors)
            path.append(next_pos)
            current = next_pos
        else:
            break
    return path
# Generate a randomized path
random_path = generate_randomized_path()
 # Print the path
print("Randomized Path:")
for position in random_path:
    print(position)