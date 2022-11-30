INTERVAL = 7
DELAY = 2

def fast_day(population, n):
    counts = [population.count(x) for x in range(INTERVAL+DELAY)]
    for _ in range(n):
        new_spawns = counts.pop(0)
        counts[INTERVAL-1] += new_spawns
        counts.append(new_spawns)
    return sum(counts)

def efficient_day(population, n):
    max_count = INTERVAL+DELAY
    counts = [population.count(x) for x in range(max_count)]
    for i in range(n):
        zero_index = i % max_count
        counts[(zero_index + INTERVAL) % max_count] += counts[zero_index]
    return sum(counts)

if __name__ == "__main__":
    with open("input.txt") as f:
        population = [int(x) for x in f.read().split(",")]

    print("Part 1:", efficient_day(population, 80))
    print("Part 2:", efficient_day(population, 256))