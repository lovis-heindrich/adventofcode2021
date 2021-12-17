import re

def hits_target(vx, vy, x1, x2, y1, y2):
    x, y = 0, 0
    highest_y = y
    while True:
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True, highest_y
        if x > x2 or y < y1:
            return False, highest_y
        x += vx
        y += vy
        vx = max(vx-1, 0)
        vy -= 1
        highest_y = max(y, highest_y)

if __name__ == "__main__":
    with open("./data/day17.txt") as f:
        x1, x2, y1, y2 = [int(s) for s in re.findall(r'(-?[\d]+)', f.read().strip())]

    max_hy = 0
    valid = 0
    for vx in range(x2+1):
        for vy in range(y1, 500):
            hits, hy = hits_target(vx, vy, x1, x2, y1, y2)
            if hits:
                max_hy = max(hy, max_hy)
                valid += 1

    print("Part 1:", max_hy)
    print("Part 2:", valid)