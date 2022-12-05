import re
import copy

def move(stacks, num, source, dest, reverse=True):
    source -= 1
    dest -= 1
    if reverse:
        stacks[dest] = stacks[dest] + list(reversed(stacks[source][-num:]))
    else:
        stacks[dest] = stacks[dest] + stacks[source][-num:]
    stacks[source] = stacks[source][:-num]
    return stacks

def read_message(stacks):
    message = ""
    for stack in stacks:
        message += stack[-1]
    return message

if __name__ == "__main__":
    with open("input.txt") as f:
        stacks, steps = f.read().split("\n\n")
        
    stacks = [stack for stack in stacks.splitlines()]
    processed_stacks = []
    for i, stack_number in enumerate(stacks[-1]):
        if stack_number != " ":
            processed_stacks.append(
                [stack[i] for stack in reversed(stacks[:-1]) if stack[i] != " "]
            )

    # num, from, to
    steps = [step for step in steps.splitlines()]
    steps = [re.findall(r"\d+", step) for step in steps]

    part_1_stacks = copy.deepcopy(processed_stacks)
    for num, source, dest in steps:
        stacks = move(part_1_stacks, int(num), int(source), int(dest))
    
    message = read_message(part_1_stacks)
    print("Part 1:", message)

    # Part 2
    part_2_stacks = copy.deepcopy(processed_stacks)
    for num, source, dest in steps:
        stacks = move(part_2_stacks, int(num), int(source), int(dest), reverse=False)
        
    message = read_message(part_2_stacks)
    print("Part 2:", message)
    