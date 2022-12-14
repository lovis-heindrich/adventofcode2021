def parse_path(path):
    parsed = []
    for coordinate in path.split("->"):
        coordinate = coordinate.strip()
        x, y = coordinate.split(",")
        parsed.append((int(x), int(y)))
    return parsed

def get_path_coordinates(path):
    coordinates = set()
    coordinates.add(tuple(path[0]))
    for i in range(len(path)-1):
        current, next = path[i], path[i+1]
        if current[0] == next[0]:
            low = min(current[1], next[1])
            high = max(current[1], next[1])
            for i in range(low, high+1):
                coordinates.add((current[0], i))
        else:
            low = min(current[0], next[0])
            high = max(current[0], next[0])
            for i in range(low, high+1):
                coordinates.add((i, current[1]))
    return coordinates

def add_sand(x=500):
    global grid, offset
    sand_position = (-1, x-offset)
    while True:
        # Fallen off
        if sand_position[0] >= len(grid)-1:
            return -1, sand_position
        below = sand_position[0]+1, sand_position[1]
        left = sand_position[0]+1, sand_position[1]-1
        right = sand_position[0]+1, sand_position[1]+1
        if (grid[below[0]][below[1]] > 0) and (grid[left[0]][left[1]] > 0) and (grid[right[0]][right[1]] > 0):
            if sand_position[0] == 0:
                return 2, sand_position
            return 1, sand_position
        # Movement
        if grid[below[0]][below[1]] == 0:
            sand_position= below
        elif grid[left[0]][left[1]] == 0:
            sand_position = left
        elif grid[right[0]][right[1]] == 0:
            sand_position = right
        else:
            print("failed movement")

def init_grid(paths):
    coordinates = set()
    for path in paths:
        coordinates.update(get_path_coordinates(path))
    coordinates = list(coordinates)
    max_x = max(coordinates, key=lambda x: x[0])[0]
    max_y = max(coordinates, key=lambda x: x[1])[1]
    min_x = min(coordinates, key=lambda x: x[0])[0]
    offset = min_x-1   
    grid = [[0 for x in range(max_x-min_x+3)] for y in range(max_y+1)]
    for x, y in coordinates:
        grid[y][x-offset] = 1
    return grid, offset

def print_grid():
    global grid
    print("")
    for row in grid:
        print(row)

def init_large_grid(paths):
    coordinates = set()
    for path in paths:
        coordinates.update(get_path_coordinates(path))
    coordinates = list(coordinates)
    max_x = max(coordinates, key=lambda x: x[0])[0]
    max_y = max(coordinates, key=lambda x: x[1])[1] + 2
    min_x = min(coordinates, key=lambda x: x[0])[0]
    max_x = (max_x-min_x)+2*max_y
    offset = min_x-1-1*max_y  
    grid = [[0 for x in range(max_x)] for y in range(max_y)]
    grid.append([1 for x in range(max_x)])
    for x, y in coordinates:
        grid[y][x-offset] = 1
    return grid, offset

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [path for path in f.read().splitlines()]
    paths = [parse_path(path) for path in input]
    
    grid, offset = init_grid(paths)
    result = 1
    iterations = 0
    while result > 0:
        result, pos = add_sand()
        grid[pos[0]][pos[1]] = 2
        #print_grid()
        iterations+=1
    
    print("Part 1:", iterations-1)

    grid, offset = init_large_grid(paths)
    result = 1
    iterations = 0
    while result < 2:
        result, pos = add_sand()
        grid[pos[0]][pos[1]] = 2
        #print_grid()
        iterations+=1
    print("Part 2:", iterations)

