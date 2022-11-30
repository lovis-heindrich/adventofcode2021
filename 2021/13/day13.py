def fold_dot(fold, dot): 
    if fold[0] == "x" and dot[0] > fold[1]:
        return dot[0] - ((dot[0] - fold[1]) * 2), dot[1]
    elif fold[0] == "y" and dot[1] > fold[1]:
        return dot[0], dot[1] - ((dot[1] - fold[1]) * 2)
    return dot

if __name__ == "__main__":
    with open("./data/day13.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    dots = []
    folds = []
    for row in input:
        if row == "":
            pass
        elif row.startswith("fold"):
            fold = row.split("=")
            folds.append((fold[0][-1], int(fold[1])))
        else:
            dot = row.split(",")
            dots.append((int(dot[0]), int(dot[1])))

    for i, fold in enumerate(folds):
        dots = [fold_dot(fold, dot) for dot in dots]
        if i == 0:
            print("Part 1:", len(set(dots)))
    
    max_x = max(dots, key=lambda x: x[0])[0] + 1
    max_y = max(dots, key=lambda x: x[1])[1] + 1
    dots = set(dots)

    for y in range(max_y):
        row = ""
        for x in range(max_x):
            if (x, y) in dots:
                row += ("#")
            else:
                row += (".")
        print(row)