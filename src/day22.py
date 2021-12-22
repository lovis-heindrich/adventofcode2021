import re

def overlap(range1, range2):
    x1, x2, y1, y2, z1, z2 = range1
    a1, a2, b1, b2, c1, c2 = range2
    x_overlap = max(min(a2,x2)-max(a1,x1),0)
    y_overlap = max(min(b2,y2)-max(b1,y1),0)
    z_overlap = max(min(c2,z2)-max(c1,z1),0)
    return x_overlap*y_overlap*z_overlap    

def count_cubes(range1):
    x1, x2, y1, y2, z1, z2 = range1
    return (x2-x1)*(y2-y1)*(z2-z1)

def remove_intersect_from_area(range1, area):
    x1, x2, y1, y2, z1, z2 = range1
    a1, a2, b1, b2, c1, c2 = area
    new_areas = []
    a_range = cut_x(a1, a2, x1, x2)
    b_range = cut_x(b1, b2, y1, y2)
    c_range = cut_x(c1, c2, z1, z2)
    for a1, a2 in zip(a_range, a_range[1:]):
        for b1, b2 in zip(b_range, b_range[1:]):
            for c1, c2 in zip(c_range, c_range[1:]):
                area = (a1, a2, b1, b2, c1, c2)
                if overlap(range1, area) == 0:
                    new_areas.append(area)
    return new_areas

def remove_intersects_from_areas(range1, areas):
    new_areas = []
    for area in areas:
        if overlap(range1, area) > 0:
            split_areas = remove_intersect_from_area(range1, area)
            new_areas.extend(split_areas)
        else:
            new_areas.append(area)
    return new_areas

def cut_x(x1, x2, y1, y2):
    if x1<y1<y2<x2:
        return (x1,y1,y2,x2)
    elif x1<y1<x2:
        return (x1,y1,x2)
    elif x1<y2<x2:
        return (x1,y2,x2)
    else:
        return (x1,x2)

if __name__ == "__main__":
    with open("./data/day22.txt") as f:
        input = f.read().splitlines()

    instructions = []
    for row in input:
        command, coordinates = row.split(" ")
        coordinates = re.findall('-?[0-9]+', coordinates)
        # Reformat ranges from [start,end] to [start,end)
        coordinates = [int(x)+(i%2) for i,x in enumerate(coordinates)]
        instructions.append([command, tuple(coordinates)])

    on_cubes = set()
    for instruction in instructions:
        command, (x1, x2, y1, y2, z1, z2) = instruction
        for x in range(max(-50, x1), min(51, x2)):
            for y in range(max(-50, y1), min(51, y2)):
                for z in range(max(-50, z1), min(51, z2)):
                    if command == "on":
                        on_cubes.add((x,y,z))
                    else:
                        on_cubes.discard((x,y,z))
    print("Part 1:", len(on_cubes))

    lit_areas = []
    for command, range1 in instructions:
        lit_areas = remove_intersects_from_areas(range1, lit_areas)
        if command == "on":
            lit_areas.append(range1)
    print("Part 2:", sum([count_cubes(area) for area in lit_areas]))