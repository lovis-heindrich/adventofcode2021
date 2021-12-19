import numpy as np
from collections import Counter

def find_relative_position(scanner_points_a, scanner_points_b):
    # Assumes correct rotation!
    offset_counter = Counter()
    for point_a in scanner_points_a:
        for point_b in scanner_points_b:
            offset = tuple(np.array(point_a) - np.array(point_b))
            offset_counter[offset] += 1
    offset, count = offset_counter.most_common(1)[0]
    if count >= 12:
        new_points = np.array(scanner_points_b) + offset
        return True, [tuple(element) for element in new_points.tolist()], offset
    else:
        return False, None, None
    
def rotate_z(scanner):
    scanner = scanner[:,[1, 0, 2]]
    scanner[:,0] = scanner[:,0]*-1
    return scanner

def rotate_x(scanner):
    scanner = scanner[:,[0, 2, 1]]
    scanner[:,2] = scanner[:,2]*-1
    return scanner

def get_possible_orientations(scanner_b):
    orientations = []
    scanner = np.array(scanner_b)
    for _ in range(2):
        for _ in range(3):
            scanner = rotate_x(scanner)
            orientations.append([tuple(element) for element in scanner.tolist()])
            for _ in range(3):
                scanner = rotate_z(scanner)
                orientations.append([tuple(element) for element in scanner.tolist()])
        scanner = rotate_x(rotate_z(rotate_x(scanner)))
    return orientations

def test_overlap(scanner_a, scanner_b):
    orientations_b = get_possible_orientations(scanner_b)
    for orientation in orientations_b:
        overlap, points, offset = find_relative_position(scanner_a, orientation)
        if overlap:
            return True, points, offset
    return False, None, None

if __name__ == "__main__":
    with open("./data/day19.txt") as f:
        input = f.read().split("\n\n")
    
    scanners = []
    for scanner in input:
        scanners.append([tuple([int(x) for x in row.split(",")]) for row in scanner.splitlines()[1:]])

    unmatched_scanners = list(range(1, len(scanners)))
    
    positions = set(scanners[0])
    scanner_positions = [(0,0,0)]
    while unmatched_scanners:
        for candidate_index in range(len(unmatched_scanners)):
            candidate = scanners[unmatched_scanners[candidate_index]]
            match, matched_candidate, offset = test_overlap(list(positions), candidate)
            if match:
                unmatched_scanners.pop(candidate_index)
                scanner_positions.append(offset)
                positions = set.union(set(matched_candidate), positions)
                break   
    print("Part 1", len(positions))

    max_distance = 0
    for pos1 in scanner_positions:
        for pos2 in scanner_positions:
            distance = np.abs(np.array(pos1)-np.array(pos2)).sum()
            max_distance = max(max_distance, distance)
    print("Part 2:", max_distance)