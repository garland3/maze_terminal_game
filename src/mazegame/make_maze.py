import numpy as np
import random


# def create_maze(width, height):
#     # Helper function to check if a cell is within maze boundaries
#     def is_valid(x, y):
#         return 0 <= x < height and 0 <= y < width

#     # Initialize maze with walls
#     maze = np.ones((height, width), dtype=np.uint8)

#     # Choose random starting point
#     start_x, start_y = random.randint(0, height - 1) // 2 * 2, random.randint(0, width - 1) // 2 * 2
#     maze[start_x, start_y] = 2

#     # List of available walls
#     walls = [(start_x, start_y, dx, dy) for (dx, dy) in ((0, 1), (1, 0), (0, -1), (-1, 0))]

#     while walls:
#         x, y, dx, dy = random.choice(walls)
#         walls.remove((x, y, dx, dy))

#         nx, ny = x + dx * 2, y + dy * 2

#         if is_valid(nx, ny) and maze[nx, ny] == 1:
#             maze[nx - dx, ny - dy] = 0
#             maze[nx, ny] = 0

#             # Add adjacent walls
#             for ndx, ndy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
#                 nnx, nny = nx + ndx * 2, ny + ndy * 2
#                 if is_valid(nnx, nny) and maze[nnx, nny] == 1:
#                     walls.append((nx, ny, ndx, ndy))

#     # Choose random end point
#     end_x, end_y = random.randint(0, height - 1) // 2 * 2, random.randint(0, width - 1) // 2 * 2
#     maze[end_x, end_y] = 3

#     # Create the symbol mapping
#     symbols = {0: "0", 1: "1", 2:"*", 3:"$"}

#     # Convert the maze to the specified symbols
#     maze = np.vectorize(symbols.get)(maze)

#     return maze, (start_x, start_y), (end_x, end_y)
import numpy as np
import random

def create_maze(width, height, num_intermediate_points=5, num_wrong_paths=10):
    # Initialize the maze with all wall values
    maze = np.ones((height, width), dtype=int)


    def get_neighbors(x, y):
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    def is_valid(x, y):
        return 0 < x < height-1 and 0 < y < width-1

    def create_path(points):
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            while x1 != x2 or y1 != y2:
                neighbors = [n for n in get_neighbors(x1, y1) if is_valid(*n)]
                x1, y1 = min(neighbors, key=lambda p: abs(p[0]-x2) + abs(p[1]-y2))
                maze[x1, y1] = 0

    # Create correct path
    correct_path_points = [(1, 1)] # start point
    for _ in range(num_intermediate_points):
        x, y = random.randint(1, height-2), random.randint(1, width-2)
        correct_path_points.append((x, y))
    correct_path_points.append((height-2, width-2)) # end point

    create_path(correct_path_points)

    # Create wrong paths
    for _ in range(num_wrong_paths):
        wrong_path_start = random.choice(correct_path_points)
        wrong_path_end = (random.randint(1, height-2), random.randint(1, width-2))
        create_path([wrong_path_start, wrong_path_end])
    
    
    # Set start and goal points
    maze[1, 1] = 2
    maze[height-2, width-2] = 3

    return maze, (1, 1), (height-2, width-2)

# Example usage
# maze = create_maze(15, 15)
# print(maze)

  
def convert_array_to_maze(array, verbose=False, symbols=None):
    # Define the mapping between array values and maze symbols
    # * is the start
    # $ is the end
    # 0 is a path no obstacle
    # 1 is a wall
    symbols = {0: " ", 1: "#", 2:"*", 3:"$"} if symbols is None else symbols

    # Convert the array to a list of strings representing the maze
    maze = []
    for row in array:
        maze_row = [symbols[val] for val in row]
        row = "".join(maze_row)
        if verbose:
            print(row)
        maze.append(row)
    return maze

if __name__ == "__main__":
    # Example usage
    # maze_array, start, end = generate_random_maze((10,20), p=0.5, verbose=True)
    # maze = convert_array_to_maze(maze_array, verbose=True)
    # print(maze)

    width, height = 21, 11  # Dimensions should be odd for the algorithm to work properly
    maze_array, start, end = create_maze(width, height)
    print("start: ", start)
    print("end: ", end)
    

    maze = convert_array_to_maze(maze_array, verbose=True)
    # print(maze)
    # Print the maze
    # for row in maze:
        # print("".join(["#" if cell else " " for cell in row]))