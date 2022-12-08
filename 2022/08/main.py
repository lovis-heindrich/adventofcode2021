def check_visibility(grid):
    """Checks visibility of trees from left to right."""
    grid_visibility = []
    for row in grid: 
        row_visibility = []
        for i in range(len(row)):
            if (i==0) or (row[i] > max(row[0:i])):
                row_visibility.append(1)
            else:
                row_visibility.append(0)
        grid_visibility.append(row_visibility)
    return grid_visibility

def combine_visibilities(vis_1, vis_2):
    """Combines two lists of visibilities carrying over all 1s in both grids."""
    return [[max(tree_1, tree_2) for tree_1, tree_2 in zip(row_1, row_2)] 
        for row_1, row_2 in zip(vis_1, vis_2)]

def combine_distances(dis_1, dis_2):
    """Combines two lists of distances by multiplying the view distances."""
    return [[tree_1*tree_2 for tree_1, tree_2 in zip(row_1, row_2)] 
        for row_1, row_2 in zip(dis_1, dis_2)]

def rotate_90(grid):
    """Rotates a nested list by -90 degrees so that the last column becomes the first row."""
    length = len(grid[0])
    height = len(grid)
    new_grid = []
    for col in range(height)[::-1]:
        new_row = []
        for row in range(length):
            new_row.append(grid[row][col])
        new_grid.append(new_row)
    return new_grid

def check_distance(grid):
    """Checks the view distance of all trees from left to right."""
    grid_distance = []
    for row in grid: 
        row_distance = []
        for i in range(len(row)-1):
            view = 0
            for tree in row[i+1:]:
                view += 1
                if tree >= row[i]:
                    break
            row_distance.append(view)
        row_distance.append(0)
        grid_distance.append(row_distance)
    return grid_distance

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    grid = [[int(char) for char in row] for row in input]
    length = len(grid[0])
    height = len(grid)
    visible = [[0 for x in range(length)] for y in range(height)]
    distances = [[1 for x in range(length)] for y in range(height)] 
    
    for _ in range(4):
        grid = rotate_90(grid)
        visible = rotate_90(visible)
        new_visibility = check_visibility(grid)
        visible = combine_visibilities(visible, new_visibility)
        distances = rotate_90(distances)
        new_distance = check_distance(grid)
        distances = combine_distances(distances, new_distance)

    print("Part 1:", sum([sum(row) for row in visible]))
    print("Part 2:", max([max(row) for row in distances]))