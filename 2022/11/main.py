import re
import math

def parse_operation(input: str):
    operator = re.findall(r"\*|\+", input)[0]
    factor = re.findall(r"\d+", input)
    assert len(factor) < 2
    if operator == "*":
        if len(factor) == 0:
            return lambda x: x * x
        else:
            return lambda x: x * int(factor[0])
    else:
        if len(factor) == 0:
            return lambda x: x + x
        else:
            return lambda x: x + int(factor[0])

def parse_test(inputs: list[str]):
    divisor = int(re.findall(r"\d+", inputs[0])[0])
    target_1 = int(re.findall(r"\d+", inputs[1])[0])
    target_2 = int(re.findall(r"\d+", inputs[2])[0])
    return lambda x: target_1 if (x%divisor)==0 else target_2, divisor

class Monkey():
    def __init__(self, input: str):
        input_rows = input.splitlines()
        self.id = int(re.findall(r"\d+", input_rows[0])[0])
        self.items = [int(x) for x in re.findall(r"\d+", input_rows[1])]
        self.operation = parse_operation(input_rows[2])
        self.test, self.divisor = parse_test(input_rows[3:])
        self.num_inspected = 0
    
    def turn(self, divide=True):
        outputs = []
        for item in self.items:
            self.num_inspected += 1
            item = self.operation(item)
            if divide:
                item = item // 3
            target = self.test(item)
            outputs.append((target, item))
        self.items = []
        return outputs
    
    def update(self, item):
        self.items.append(item)

    def reduce_items(self, fun):
        self.items = [fun(x) for x in self.items]

def play_rounds(monkeys, n, divide=True):
    common_divisor = math.prod([monkey.divisor for monkey in monkeys])
    for _ in range(n):
        for monkey in monkeys:
            monkey.reduce_items(lambda x: x%common_divisor)
            throws = monkey.turn(divide=divide)
            for target, item in throws:
                monkeys[target].update(item)

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [monkey for monkey in f.read().split("\n\n")]
    
    monkeys = [Monkey(monkey) for monkey in input]
    play_rounds(monkeys, n=20, divide=True)
    inspections = [monkey.num_inspected for monkey in monkeys]
    inspections.sort(reverse=True)
    print("Part 1:", inspections[0]*inspections[1])
    
    monkeys = [Monkey(monkey) for monkey in input]
    play_rounds(monkeys, n=10000, divide=False)
    inspections = [monkey.num_inspected for monkey in monkeys]
    inspections.sort(reverse=True)
    print("Part 2:", inspections[0]*inspections[1])