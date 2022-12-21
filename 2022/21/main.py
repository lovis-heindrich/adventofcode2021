import re

class Monkey:
    def __init__(self, str) -> None:
        name, command = str.split(":")
        self.name = name.strip()
        if command.strip().isnumeric():
            self.done = True
            self.value = int(command.strip())
        else:
            self.done = False
            self.inputs = re.findall(r"[a-z]{4}", command)
            self.command = re.findall(r"[-+*/]", command)[0]
    
    def try_compute(self, monkeys: list[any]):
        if self.done:
            return False
        changed = False
        for monkey in monkeys:
            if (type(self.inputs[0])==str) and (monkey.name==self.inputs[0]) and (monkey.done):
                self.inputs[0]=monkey.value
                changed = True
            elif (type(self.inputs[1])==str) and (monkey.name==self.inputs[1]) and (monkey.done):
                self.inputs[1]=monkey.value
                changed = True
        if (type(self.inputs[1])==str) or (type(self.inputs[0])==str):
            return changed
        first, second = self.inputs[0], self.inputs[1]
        match self.command:
            case "+":
                result = first+second
            case "-":
                result = first-second
            case "*":
                result =  first*second
            case "/":
                result =  first/second
            case _:
                print("Error", self.command)
        self.value = int(result)
        self.done = True
        return True

def trace_back(input: str|int, monkeys: list[Monkey]):
    if type(input)==int:
        return lambda x: input
    elif input=="humn":
        return lambda x: x
    else:
        monkey = [monkey for monkey in monkeys if monkey.name==input]
        assert len(monkey)==1, "Too many matches"
        monkey = monkey[0]
        left = monkey.inputs[0]
        right = monkey.inputs[1]
        command = monkey.command
        match command:
            case "+":
                return lambda x: trace_back(left, monkeys)(x) + trace_back(right, monkeys)(x)
            case "-":
                return lambda x: trace_back(left, monkeys)(x) - trace_back(right, monkeys)(x)
            case "*":
                return lambda x: trace_back(left, monkeys)(x) * trace_back(right, monkeys)(x)
            case "/":
                return lambda x: trace_back(left, monkeys)(x) / trace_back(right, monkeys)(x)

def undo_operation(current, command, value):
        match command:
            case "+":
                result = current - value
            case "-":
                result = current + value
            case "*":
                result = current / value
            case "/":
                result = current * value
        return result
    

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]

    monkeys = [Monkey(row) for row in input]
    root = [monkey for monkey in monkeys if monkey.name=="root"][0]
    not_done = [monkey for monkey in monkeys if not monkey.done]
    while not root.done:
        for monkey in not_done:
            monkey.try_compute(monkeys)
        not_done = [monkey for monkey in monkeys if not monkey.done]
    print("Part 1:", root.value)

    monkeys = [Monkey(row) for row in input]
    root = [monkey for monkey in monkeys if monkey.name=="root"][0]
    human = [monkey for monkey in monkeys if monkey.name=="humn"][0]
    human.done = False
    not_done = [monkey for monkey in monkeys if not monkey.done]
    changed = True
    while changed:
        changed = False
        for monkey in not_done:
            if (monkey.name!="humn"):
                res = monkey.try_compute(monkeys)
                changed = changed or res
        not_done = [monkey for monkey in monkeys if not monkey.done]

    left_side = root.inputs[0]
    monkey = [monkey for monkey in monkeys if monkey.name==left_side][0]
    current = -root.inputs[1]
    #print(monkey.inputs[0], monkey.command, monkey.inputs[1], "=", current)
    while (monkey.name!="humn") and ((type(monkey.inputs[1])==int) or (monkey.command!="/")):
        first, second = monkey.inputs[0], monkey.inputs[1]
        command = monkey.command
        assert (type(first)==str) or (type(second)==str), "Solved monkey"
        if (type(second)==int):
            current = undo_operation(current, command, second)
            monkey = [monkey for monkey in monkeys if monkey.name==first][0]
        elif (type(first)==int):
            current = undo_operation(current, command, first)
            monkey = [monkey for monkey in monkeys if monkey.name==second][0]
        #print(first,command,second,"=",current)
    
    # Hacky solution - account for rounding errors by testing potential values
    left_side = root.inputs[0]
    right_side = root.inputs[1]
    if type(left_side)==str:
        f_left_side = trace_back(left_side, monkeys)
    else:
        f_left_side = lambda x: left_side
    if type(right_side)==str:
        f_right_side = trace_back(right_side, monkeys)
    else:
        f_right_side = lambda x: right_side
    
    result = lambda x: int(f_left_side(x)) == int(f_right_side(x))
    for i in range(int(current)-1000, int(current)+1000):
        if result(i):
            print("Part 2:", i)
