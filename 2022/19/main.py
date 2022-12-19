import re
from functools import lru_cache
import tqdm
import math

class Blueprint:
    def __init__(self, costs) -> None:
        assert len(costs)==7, costs
        self.costs = costs
        self.id = costs[0]
        self.ore_cost_ore = costs[1]
        self.clay_cost_ore = costs[2]
        self.obsidian_cost_ore = costs[3]
        self.obsidian_cost_clay = costs[4]
        self.geode_cost_ore = costs[5]
        self.geode_cost_obsidian = costs[6]
    
    def __repr__(self) -> str:
        return str(self.costs)

def collect_ore(ores, robots, n=1):
    return [ore+(robot*n) for ore, robot in zip(ores, robots)]

@lru_cache(maxsize=2**24)
def factory_smart(step, blueprint: Blueprint, ores=None, robots=None):
    if (ores==None) or (robots==None):
        ores = [0, 0, 0, 0]
        robots = [1, 0, 0, 0]
    if step == 0:
        return ores[-1]
    values = []
    # Build ore robot
    remaining_steps = math.ceil(max(0, blueprint.ore_cost_ore-ores[0])/robots[0])+1
    if (step-2-blueprint.ore_cost_ore) > remaining_steps:
        next_ores = collect_ore(ores, robots, remaining_steps)
        next_robots = [robot for robot in robots]
        next_ores[0] -= blueprint.ore_cost_ore
        next_robots[0] += 1
        values.append(factory_smart(step-remaining_steps, blueprint, tuple(next_ores), tuple(next_robots)))
    # Build clay robot
    remaining_steps = math.ceil(max(0, blueprint.clay_cost_ore-ores[0])/robots[0])+1
    if (step-3) > remaining_steps:
        next_ores = collect_ore(ores, robots, remaining_steps)
        next_robots = [robot for robot in robots]
        next_ores[0] -= blueprint.clay_cost_ore
        next_robots[1] += 1
        #if (next_ores[1] + (step-remaining_steps-2)*next_robots[1])>blueprint.obsidian_cost_clay:
        values.append(factory_smart(step-remaining_steps, blueprint, tuple(next_ores), tuple(next_robots)))
    # Build obsidian robot
    if robots[1]>0:
        remaining_steps_ore = math.ceil(max(0, blueprint.obsidian_cost_ore-ores[0])/robots[0])
        remaining_steps_clay = math.ceil(max(0, blueprint.obsidian_cost_clay-ores[1])/robots[1])
        remaining_steps = max(remaining_steps_ore, remaining_steps_clay)+1
        if (step-2) > remaining_steps:
            next_ores = collect_ore(ores, robots, remaining_steps)
            next_robots = [robot for robot in robots]
            next_ores[0] -= blueprint.obsidian_cost_ore
            next_ores[1] -= blueprint.obsidian_cost_clay
            next_robots[2] += 1
            values.append(factory_smart(step-remaining_steps, blueprint, tuple(next_ores), tuple(next_robots)))
    # Build geode robot:
    if (robots[2]>0):
        remaining_steps_ore = math.ceil(max(0, blueprint.geode_cost_ore-ores[0])/robots[0])
        remaining_steps_obsidian = math.ceil(max(0, blueprint.geode_cost_obsidian-ores[2])/robots[2])
        remaining_steps = max(remaining_steps_ore, remaining_steps_obsidian)+1
        if (step) > remaining_steps:
            next_ores = collect_ore(ores, robots, remaining_steps)
            next_robots = [robot for robot in robots]
            next_ores[0] -= blueprint.geode_cost_ore
            next_ores[2] -= blueprint.geode_cost_obsidian
            next_robots[3] += 1
            values.append(factory_smart(step-remaining_steps, blueprint, tuple(next_ores), tuple(next_robots)))
    # Wait
    if len(values)==0:
        next_ores = collect_ore(ores, robots, step)
        values.append(next_ores[-1])
    return max(values)

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    blueprints = []
    for row in input:
        costs = [int(x) for x in re.findall(r"-?\d+", row)]
        blueprints.append(Blueprint(costs))
    
    values = []
    for blueprint in tqdm.tqdm(blueprints):
        values.append(blueprint.id*factory_smart(24, blueprint))
        factory_smart.cache_clear()
    print("Part 1:", sum(values))
    
    values = []
    # Takes about 1.5h
    for i in tqdm.tqdm(range(3)):
        values.append(factory_smart(32, blueprints[i]))
    print("Part 2:", values[0]*values[1]*values[2])