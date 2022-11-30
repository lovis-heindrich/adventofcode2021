def fuel_consumption(positions, target):
    return sum([abs(pos-target) for pos in positions])

def fuel_consumption_increasing(positions, target):
    distances = [abs(pos-target) for pos in positions]
    return sum([x*(x+1)//2 for x in distances])

if __name__ == "__main__":
    with open("./data/day7.txt") as f:
        positions = [int(x) for x in f.read().split(",")]
    candidates = range(min(positions), max(positions))
    best_target = min(candidates, key=lambda x: fuel_consumption(positions, x))
    print("Part 1:", fuel_consumption(positions, best_target))
    best_target = min(candidates, key=lambda x: fuel_consumption_increasing(positions, x))
    print("Part 2:", fuel_consumption_increasing(positions, best_target))