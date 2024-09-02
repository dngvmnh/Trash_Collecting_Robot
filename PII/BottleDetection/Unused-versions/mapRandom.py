import random
def generate_randomized_path():
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ]
    rows = len(grid)
    cols = len(grid[0])
    start = (0, 0)
    end = (rows-1, cols-1)
    path = [start]
    current = start
    visited = set([current])
    while current != end:
        neighbors = []
        if current[0] > 0 and grid[current[0]-1][current[1]] == 0 and (current[0]-1, current[1]) not in visited:
            neighbors.append((current[0]-1, current[1]))  # Up
        if current[0] < rows-1 and grid[current[0]+1][current[1]] == 0 and (current[0]+1, current[1]) not in visited:
            neighbors.append((current[0]+1, current[1]))  # Down
        if current[1] > 0 and grid[current[0]][current[1]-1] == 0 and (current[0], current[1]-1) not in visited:
            neighbors.append((current[0], current[1]-1))  # Left
        if current[1] < cols-1 and grid[current[0]][current[1]+1] == 0 and (current[0], current[1]+1) not in visited:
            neighbors.append((current[0], current[1]+1))  # Right
        if neighbors:
            next_pos = random.choice(neighbors)
            path.append(next_pos)
            current = next_pos
            visited.add(current)
        else:
            break
    return path
random_path = generate_randomized_path()
print("Randomized Path:")
for position in random_path:
    print(position)