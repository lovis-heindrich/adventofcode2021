def move_right(grid):
    valid = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == ">" and grid[x][(y+1)%len(grid[x])] == ".":
                valid.append((x,y))
    for x, y in valid:
        grid[x][y] = "."
        grid[x][(y+1)%len(grid[x])] = ">"
    return grid, len(valid)

def move_down(grid):
    valid = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == "v" and grid[(x+1)%len(grid)][y] == ".":
                valid.append((x,y))
    for x, y in valid:
        grid[x][y] = "."
        grid[(x+1)%len(grid)][y] = "v"
    return grid, len(valid)

def move(grid):
    grid, moved_right = move_right(grid)
    grid, moved_down = move_down(grid)
    return grid, moved_down+moved_right

def print_grid(grid):
    print()
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    with open("input.txt") as f:
        grid = [[c for c in line.strip()] for line in f.read().splitlines()]

    moved = 1
    steps = 0
    while moved > 0:
        grid, moved = move(grid)
        steps += 1

    print("Part 1:", steps)