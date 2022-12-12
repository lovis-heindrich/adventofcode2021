def find_shortest_path():
    global grid_distances, grid, height_grid, goal_position
    changed = True
    while changed:
        changed = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                height = height_grid[(x, y)]
                neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                neighbors = [neighbor for neighbor in neighbors if (0<=neighbor[0]<len(grid))&(0<=neighbor[1]<len(grid[0]))]
                neighbors = [neighbor for neighbor in neighbors if (height-height_grid[neighbor])<=1]
                neighbor_distances = [grid_distances[neighbor] for neighbor in neighbors]
                if (len(neighbor_distances)>0) and ((min(neighbor_distances)+1)<grid_distances[(x,y)]):
                    grid_distances[(x,y)] = (min(neighbor_distances)+1)
                    changed = True

def init_grid_distances(start_only=True):
    global grid
    goal_position = (0, 0)
    grid_distances = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid_distances[(x,y)] = len(grid) * len(grid[0])
            if grid[x][y] == "E":
                goal_position = (x, y)
                grid[x][y] = "z"
            elif grid[x][y] == "S":
                grid[x][y] = "a"
                grid_distances[(x,y)] = 0
            elif (grid[x][y] == "a") and (start_only==False):
                grid_distances[(x,y)] = 0
    return grid_distances, goal_position

if __name__ == "__main__":
    with open("input.txt") as f:
        grid = [[x for x in row] for row in f.read().splitlines()]

    grid_distances, goal_position = init_grid_distances(start_only=True)
    height_grid = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            height_grid[(x,y)] = ord(grid[x][y])
    
    find_shortest_path()
    print("Part 1:", grid_distances[goal_position])

    grid_distances, _ = init_grid_distances(start_only=False)
    find_shortest_path()
    print("Part 2:", grid_distances[goal_position])
