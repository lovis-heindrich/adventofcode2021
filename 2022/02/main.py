# Part 1
shape_points = {"X": 1, "Y": 2, "Z": 3}
win_points = {"AX": 3, "AY": 6, "AZ": 0,
    "BX": 0, "BY": 3, "BZ": 6,
    "CX": 6, "CY": 0, "CZ": 3}

# Part 2
win_points_2 = {"X": 0, "Y": 3, "Z": 6}
shape_points_2 = {"AX": 3, "AY": 1, "AZ": 2,
    "BX": 1, "BY": 2, "BZ": 3,
    "CX": 2, "CY": 3, "CZ": 1}

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row.replace(" ", "") for row in f.read().splitlines()]
    
    shape = sum([shape_points[game[-1]] for game in input])
    win = sum([win_points[game] for game in input])
    print("Part 1:", shape + win)

    shape_2 = sum([shape_points_2[game] for game in input])
    win_2 = sum([win_points_2[game[-1]] for game in input])
    print("Part 2:", shape_2 + win_2)