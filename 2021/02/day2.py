if __name__ == "__main__":
    with open('./data/day2.txt') as f:
        lines = [x.split(" ") for x in f.read().splitlines()]

    aim = 0
    position = 0
    depth = 0
    for direction, amount in lines:
        if direction == "down":
            aim += int(amount)
        elif direction == "up":
            aim -= int(amount)
        elif direction == "forward":
            position += int(amount)
            depth += aim * int(amount)

    print("Part 1", aim * position)
    print("Part 2", depth * position)