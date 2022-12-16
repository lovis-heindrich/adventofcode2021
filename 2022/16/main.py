import re
import tqdm
from functools import lru_cache

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    valves = []
    destinations = []
    flow_rates = []
    for row in input:
        parsed_valves = re.findall(r"\b[A-Z]{2}\b", row)
        valves.append(parsed_valves[0])
        destinations.append(parsed_valves[1:])
        flow_rates.append(int(re.findall(r"-?\d+", row)[0]))

    tree = [[valves.index(d) for d in dests] for dests in destinations]
    opened = tuple([0 for _ in range(len(valves))])

    @lru_cache(maxsize=None)
    def get_available_targets(opened, split=None):
        if split is not None:
            return [i for i in range(len(opened)) if (flow_rates[i] > 0) and (opened[i] == 0) and (i in split)]
        else:
            return [i for i in range(len(opened)) if (flow_rates[i] > 0) and (opened[i] == 0)]
    
    @lru_cache(maxsize=None)
    def get_distance(position, target, visited=None):
        if visited == None:
            visited = (position,)
        else:
            visited = tuple(list(visited) + [position])
        if target == position:
            return 0
        elif target in tree[position]:
            return 1
        elif all([pos in visited for pos in tree[position]]):
            return len(tree)+1
        else:
            next_distances = []
            for next_pos in tree[position]:
                if next_pos not in visited:
                    next_distance = get_distance(next_pos, target, visited)
                    next_distances.append(next_distance)
            return 1 + min(next_distances)

    def simulate(opened, pos, step, path=None, split=None):
        if path==None:
            path=[]
        targets = get_available_targets(opened, split)
        distances = [get_distance(pos, target)+1 for target in targets]
        values = []
        valid_targets = []
        paths = []
        for target, distance in zip(targets, distances):
            if distance <= 30 - step:
                next_opened = tuple([val if i!=target else 1 for i, val in enumerate(opened)])
                next_step = step + distance
                new_value = flow_rates[target]*(30-next_step)
                next_value, next_path = simulate(next_opened, target, next_step, path + [valves[target]], split)
                value = new_value + next_value
                valid_targets.append(target)
                values.append(value)
                paths.append(next_path)
        if len(values) > 0:
            max_value = max(values)
            index = [i for i in range(len(values)) if values[i]==max_value][0]
            return max_value, paths[index]
        else:
            return 0, path

    position = valves.index("AA")
    available_targets = get_available_targets(opened)
    print("Part 1:", simulate(opened, position, 0)[0])
    
    # Generate subsets - only works for uneven numbers of possible targets
    assert(len(available_targets)%2==1)

    def create_splits(targets):
        def create_split(targets, n):
            if n==1:
                for target in targets:
                    yield [target]
            else:
                for i, target in enumerate(targets):
                    if len(targets[i:]) >= n:
                        next_splits = create_split(targets[i+1:], n-1)
                        for next_split in next_splits:
                            yield [target] + next_split

        for len_x in range(1, (len(targets)//2)+1):
            x_splits = create_split(targets, len_x)
            for x_split in x_splits:
                y_split = [target for target in targets if target not in x_split]
                yield (tuple(x_split), tuple(y_split))
                
    scores = []
    for x_split, y_split in tqdm.tqdm(list(create_splits(available_targets))):
        x_score = simulate(opened, position, 4, split=x_split)[0]
        y_score = simulate(opened, position, 4, split=y_split)[0]
        scores.append(x_score+y_score)
    print("Part 2:", max(scores))
        



