from typing import List

index = {
    "w": 0,
    "x": 1,
    "y": 2,
    "z": 3
}

def run_program(commands: List[List[str]], inputs: List[int], state=(0, 0, 0, 0)):
    state = list(state)
    for command in commands:
        a_index = index[command[1]]
        a = state[a_index]
        if len(command) > 2:
            b = command[2]
            if not b.lstrip('-').isdigit():
                b = state[index[b]]
            else:
                b = int(b)
        match command[0]:
            case "inp":
                input = inputs.pop(0)
                state[a_index] = input
            case "add":
                state[a_index] = a + b
            case "mul":
                state[a_index] = a * b
            case "div":
                state[a_index] = a // int(b)
            case "mod":
                state[a_index] = a % b
            case "eql":
                state[a_index] = int(a==b)
    return tuple(state)

def run_commands(command_list, input_list, mode):
    if not command_list:
        solutions = []
        for state, previous_input in input_list:
            if state == 0:
                solutions.append(previous_input)
        if mode == "max":
            return max(solutions)
        else:
            return min(solutions)
    seen_states = {}
    n1, n2, n3 = parse_parameters(command_list[0])
    for state, previous_input in input_list:
        for i in range(1, 10):
            new_state = fast_program(i, state, n1, n2, n3)
            current_input = previous_input * 10 + i
            if new_state not in seen_states:
                seen_states[new_state] = current_input
            elif mode == "max" and seen_states[new_state] < current_input:
                seen_states[new_state] = current_input
            elif mode == "min" and seen_states[new_state] > current_input:
                seen_states[new_state] = current_input
    next_commands = None if len(command_list) == 1 else command_list[1:]
    return run_commands(next_commands, seen_states.items(), mode=mode)
    
def fast_program(w, z, n1, n2, n3):
    x = z%26
    z = z//n1
    x = int((x+n2)!=w)
    z = (25*x+1)*z
    z = (w+n3)*x+z
    return z

def parse_parameters(commands):
    n1 = int(commands[4][2])
    n2 = int(commands[5][2])
    n3 = int(commands[15][2])
    return n1, n2, n3

if __name__ == "__main__":
    with open("input.txt") as f:
        commands = [tuple(line.split(" ")) for line in f.read().splitlines()]

    split_commands = []
    current_commands = []
    for command in commands:
        if command[0] == "inp" and current_commands:
            split_commands.append(current_commands)
            current_commands = [command]
        else:
            current_commands.append(command)
    split_commands.append(current_commands)

    print("Part 1:", run_commands(split_commands, [(0, 0)], mode="max"))
    print("Part 2:", run_commands(split_commands, [(0, 0)], mode="min"))