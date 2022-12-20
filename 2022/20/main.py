import tqdm
import time

class Linked:
    def __init__(self, val) -> None:
        self.next = None
        self.back = None
        self.val = val

def move_linked(to_move: Linked, len):
    value = to_move.val
    if value == 0:
        return
    to_move.back.next = to_move.next
    to_move.next.back = to_move.back
    head = to_move
    if value < 0:
        head = head.back
        for i in range((abs(value)-1)%(len-1)):
            head = head.back
    if value > 0:
        head = head.next
        for i in range((abs(value))%(len-1)):
            head = head.next
    previous = head.back
    previous.next = to_move
    head.back = to_move
    to_move.back = previous
    to_move.next = head

def calc_result(linked: list[Linked]):
    values = []
    for element in linked:
        if element.val == 0:
            head = element
            for i in range(3):
                for _ in range(1000):
                    head = head.next
                values.append(head.val)
            return values
    return values

def init_linked(input):
    linked: list[Linked] = []
    for val in input:
        linked.append(Linked(val))
    for first, second in zip(linked, linked[1:]):
        first.next = second
        second.back = first
    linked[0].back = linked[-1]
    linked[-1].next = linked[0]
    return linked

if __name__ == "__main__":
    multiplier = 811589153
    with open("input.txt") as f:
        input = [int(row.strip()) for row in f.read().splitlines()]

    linked = init_linked(input)
    for element in linked:
            move_linked(element, len(linked))
    values = calc_result(linked)
    print("Part 1:", sum(values))

    input = [x*multiplier for x in input]
    linked = init_linked(input)
    bar = tqdm.tqdm(total = 10*len(linked))
    for i in range(10):
        for element in linked:
            move_linked(element, len(linked))
            bar.update(1)
    bar.close()
    time.sleep(2)
    values = calc_result(linked)
    print("Part 2:", sum(values))