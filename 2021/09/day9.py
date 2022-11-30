def is_low_point(x, y, heights):
    valid_neighbors = [(cx,cy) for cx, cy in [(x-1,y), (x+1,y), (x, y-1), (x,y+1)] if cx>=0 and cx<len(heights) and cy>=0 and cy<len(heights[x])]
    return all(heights[x][y]<heights[nx][ny] for nx,ny in valid_neighbors)

def get_basin_size(x,y,heights):
    queue = [(x,y)]
    basin = []
    while queue:
        x, y = queue.pop(0)
        is_valid = lambda cx,cy: cx>=0 and cx<len(heights) and cy>=0 and cy<len(heights[x]) and (cx,cy) not in basin
        valid_neighbors = [(cx,cy) for cx, cy in [(x-1,y), (x+1,y), (x, y-1), (x,y+1)] if is_valid(cx,cy)]
        if heights[x][y] != 9 and all(heights[x][y]<=heights[nx][ny] for nx,ny in valid_neighbors):
            basin.append((x,y))
            queue = list(set(queue+valid_neighbors))
    return len(basin)
    
if __name__ == "__main__":
    with open("input.txt") as f:
        heights = [[int(x) for x in row] for row in f.read().splitlines()]

    low_points = []
    for x in range(len(heights)):
        for y in range(len(heights[x])):
            if is_low_point(x, y, heights):
                low_points.append((x,y))
    
    print("Part 1:", sum([heights[x][y] for x,y in low_points])+len(low_points))

    basin_sizes = [get_basin_size(x,y,heights) for x,y in low_points]
    basin_sizes.sort()
    print("Part 2:", basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1])