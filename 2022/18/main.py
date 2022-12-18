def get_adjacent(position):
    x,y,z=position
    return [(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]

def get_offsets():
    return [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

def check_inside(position, min_limit, max_limit, input):
    insides = [position]
    queue = [position]
    while len(queue)>0:
        current = queue.pop(0)
        neighbors = get_adjacent(current)
        for neighbor in neighbors:
            if (neighbor not in input) and (neighbor not in insides):
                if (min(neighbor)<min_limit) or (max(neighbor)>max_limit):
                    return False, None
                else:
                    insides.append(neighbor)
                    queue.append(neighbor)
    return True, insides

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [tuple([int(x.strip()) for x in row.split(",")]) for row in f.read().splitlines()]
    
    open_sides = 0
    for position in input:
        offsets = get_offsets()
        for offset in offsets:
            side = tuple([pos+off for pos, off in zip(position, offset)])
            if side not in input:
                open_sides += 1
    print("Part 1:", open_sides)

    open_sides = 0
    min_x, min_y, min_z = min(input, key=lambda x: x[0])[0], min(input, key=lambda x: x[1])[1], min(input, key=lambda x: x[2])[2]
    max_x, max_y, max_z = max(input, key=lambda x: x[0])[0], max(input, key=lambda x: x[1])[1], max(input, key=lambda x: x[2])[2]
    min_axis = min(min_x, min_y, min_z)
    max_axis = max(max_x, max_y, max_z) +1

    inside_positions = []
    for position in input:
        offsets = get_offsets()
        for offset in offsets:
            side = tuple([pos+off for pos, off in zip(position, offset)])
            if (side not in input) and (side not in inside_positions):
                is_inside, insides = check_inside(side, min_axis, max_axis, input)
                if not is_inside:
                    open_sides += 1
                else:
                    inside_positions.extend(insides)
    print("Part 2:", open_sides)