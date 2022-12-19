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

def available_actions(blueprint: Blueprint, ores: list[int]):
    ore, clay, obsidian, _ = ores
    actions = [0] # 0=wait, 1=ore, 2=clay, 3=obsidian, 4=geode
    if ore >= blueprint.ore_cost_ore:
        actions.append(1)
    if ore >= blueprint.clay_cost_ore:
        actions.append(2)
    if (ore >= blueprint.obsidian_cost_ore) and (clay >= blueprint.obsidian_cost_clay):
        actions.append(3)
    if (ore >= blueprint.geode_cost_ore) and (obsidian >= blueprint.geode_cost_obsidian):
        actions.append(4)
    return actions

def available_actions_prune(step, blueprint: Blueprint, ores: list[int]):
    ore, clay, obsidian, _ = ores
    if (ore >= blueprint.geode_cost_ore) and (obsidian >= blueprint.geode_cost_obsidian) and (step>=2):
        return [4]
    actions = [0] # 0=wait, 1=ore, 2=clay, 3=obsidian, 4=geode
    if (ore >= blueprint.ore_cost_ore) and (step>=3+blueprint.geode_cost_ore):
        actions.append(1)
    if (ore >= blueprint.clay_cost_ore) and (step>=4):
        actions.append(2)
    if (ore >= blueprint.obsidian_cost_ore) and (clay >= blueprint.obsidian_cost_clay) and (step>=3):
        actions.append(3)
    return actions

def collect_ore(ores, robots, n=1):
    return [ore+(robot*n) for ore, robot in zip(ores, robots)]

def build(action, blueprint: Blueprint, ores, robots):
    next_ores = [ore for ore in ores]
    next_robots = [robot for robot in robots]
    match action:
        case 0:
            return next_ores, next_robots
        case 1:
            next_ores[0] -= blueprint.ore_cost_ore
            next_robots[0]+= 1
        case 2:
            next_ores[0] -= blueprint.clay_cost_ore
            next_robots[1]+= 1
        case 3:
            next_ores[0] -= blueprint.obsidian_cost_ore
            next_ores[1] -= blueprint.obsidian_cost_clay
            next_robots[2]+= 1
        case 4:
            next_ores[0] -= blueprint.geode_cost_ore
            next_ores[2] -= blueprint.geode_cost_obsidian
            next_robots[3]+= 1
    return next_ores, next_robots

@lru_cache(maxsize=None)
def factory_rec(step, blueprint, ores=None, robots=None):
    #global global_steps
    #global_steps += 1
    if (ores==None) or (robots==None):
        ores = [0, 0, 0, 0]
        robots = [1, 0, 0, 0]
    if step == 0:
        return ores[-1]
    # Decide what to build
    #actions = available_actions(blueprint, ores)
    actions = available_actions_prune(step, blueprint, ores)
    # Collect
    ores = collect_ore(ores, robots)
    # Build
    values = []
    for action in actions:
        next_ores, next_robots = build(action, blueprint, ores, robots)
        #print(f"step{step} action {action}, ore {ores}->{next_ores}, robots {robots}->{next_robots}")
        values.append(factory_rec(step-1, blueprint, tuple(next_ores), tuple(next_robots)))
    #print(step, actions, values)
    return max(values)

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
    
    #test_print = Blueprint([1,4,2,3,14,2,7])
    #global_steps = 0
    # test_print = Blueprint([2,2,3,3,8,3,12])
    
    #test_print = Blueprint([1,1,2,3,3,1,1])
    # test_robots = None#tuple([1,0,1,1])
    # test_ore = None#tuple([1,1,1,2])
    # import time
    # # start = time.time()
    # value = factory_rec(24, test_print, robots=test_robots, ores=test_ore)
    # first = time.time()
    # value_smart = factory_smart(24, test_print, robots=test_robots, ores=test_ore)
    # second = time.time()
    # print("Part 1:", value, value_smart)
    # print("Time", first-start, second-first)
    #print(global_steps, "steps")

    import time
    for steps in range(32,33):
        start = time.time()
        print(factory_smart(steps, blueprints[2]))
        factory_smart.cache_clear()
        print(steps, int((time.time()-start)*100)/100)
    # values = []
    # #for i in tqdm.tqdm(range(1)):
    # values.append(factory_smart(32, blueprints[2]))
    # print(factory_smart.cache_info())
    # print(values)
    # blueprint1 = 12
    # blueprint2 = 35
    # blueprint3 = 52
    #print("Part 2:", values[0]*values[1]*values[2])

