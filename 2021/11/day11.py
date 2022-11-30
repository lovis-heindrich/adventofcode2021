
def simulate(grid, n=100):
    total_flashes = 0
    for i in range(n):
        grid = [[x+1 for x in row] for row in grid]
        flashed = []
        flashes = 0
        done = False
        while not done:
            done = True
            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    if grid[x][y] > 9 and (x,y) not in flashed:
                        done = False
                        flashes += 1
                        flashed.append((x,y))
                        for nx in [x-1, x, x+1]:
                            for ny in [y-1, y, y+1]:
                                if (nx, ny) != (x, y) and nx>=0 and nx<len(grid) and ny>=0 and ny<len(grid[nx]):
                                    grid[nx][ny] += 1
        total_flashes += flashes
        for x in range(len(grid)):
                for y in range(len(grid[x])):
                    if grid[x][y] > 9:
                        grid[x][y] = 0
    return total_flashes

def synchronize(grid):
    num_octopuses = len(grid)*len(grid[0])
    i = 0
    while True:
        i += 1
        grid = [[x+1 for x in row] for row in grid]
        flashed = []
        flashes = 0
        done = False
        while not done:
            done = True
            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    if grid[x][y] > 9 and (x,y) not in flashed:
                        done = False
                        flashes += 1
                        flashed.append((x,y))
                        for nx in [x-1, x, x+1]:
                            for ny in [y-1, y, y+1]:
                                if (nx, ny) != (x, y) and nx>=0 and nx<len(grid) and ny>=0 and ny<len(grid[nx]):
                                    grid[nx][ny] += 1
        if flashes == num_octopuses:
            return i
        for x in range(len(grid)):
                for y in range(len(grid[x])):
                    if grid[x][y] > 9:
                        grid[x][y] = 0

if __name__ == "__main__":
    with open("./data/day11.txt") as f:
        input = [[int(x) for x in row] for row in f.read().splitlines()]
    
    print("Part 1:", simulate(input, 100))
    print("Part 2:", synchronize(input))
