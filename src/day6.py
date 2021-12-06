INTERVAL = 7
DELAY = 2

def fast_day(population, n):
    counts = [population.count(x) for x in range(INTERVAL+DELAY)]
    for _ in range(n):
        new_spawns = counts.pop(0)
        counts[INTERVAL-1] += new_spawns
        counts.append(new_spawns)
    return sum(counts)

if __name__ == "__main__":
    with open("./data/day6.txt") as f:
        population = [int(x) for x in f.read().split(",")]
    print("Part 1:", fast_day(population, 80))
    print("Part 2:", fast_day(population, 256))