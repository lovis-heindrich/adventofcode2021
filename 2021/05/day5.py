import re

def inclusive_range(start, end):
    if start > end:
        return list(range(start,end,-1)) + [end]
    elif end > start:
        return list(range(start,end)) + [end]
    else:
        return [end]
    
def count_overlap(size, pairs, diagonal=False):
    grid = [[0 for _ in range(size)] for _ in range(size)]

    for x1, y1, x2, y2 in pairs:  
        if x1 == x2:
            for y in inclusive_range(y1,y2):
                grid[x1][y] += 1
        elif y1 == y2:
            for x in inclusive_range(x1,x2):
                grid[x][y1] += 1
        elif abs(x1-x2) == abs(y1-y2) and diagonal:
            for x,y in zip(inclusive_range(x1,x2), inclusive_range(y1,y2)):
                grid[x][y] += 1

    return sum([sum([x>1 for x in row]) for row in grid])

if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.read().splitlines()

    pairs = [[int(s) for s in re.findall(r'\b\d+\b', line)] for line in lines]
    size = max([max(pair) for pair in pairs]) + 1
    
    print("Part 1", count_overlap(size, pairs, False))
    print("Part 2", count_overlap(size, pairs, True))