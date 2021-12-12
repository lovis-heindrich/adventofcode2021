def count_paths(cave_map, current_path=["start"], allow_duplicate=False):
    location = current_path[-1]
    if location == "end":
        return 1
    visited_twice = [cave for cave in set(current_path) if cave.islower() and (current_path.count(cave)>=2)]
    if len(visited_twice) or not allow_duplicate:
        unavailable = [cave for cave in set(current_path) if cave.islower()]
    else:
        unavailable = ["start"]
    destinations = [cave for cave in cave_map[location] if cave not in unavailable]
    if len(destinations):
        return sum([count_paths(cave_map, current_path+[destination], allow_duplicate=allow_duplicate) for destination in destinations])
    else:
        return 0

if __name__ == "__main__":
    with open("./data/day12.txt") as f:
        input = [row.strip().split("-") for row in f.read().splitlines()]
    
    cave_map = {}
    for cave_a, cave_b in input:
        if cave_a in cave_map.keys():
            cave_map[cave_a] = cave_map[cave_a] + [cave_b]
        else:
            cave_map[cave_a] = [cave_b]
        if cave_b in cave_map.keys():
            cave_map[cave_b] = cave_map[cave_b] + [cave_a]
        else:
            cave_map[cave_b] = [cave_a]
    
    print("Part 1:", count_paths(cave_map, allow_duplicate=False))
    print("Part 2:", count_paths(cave_map, allow_duplicate=True))
