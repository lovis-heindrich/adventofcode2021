def get_priority(item: str) -> int:
    assert len(item) == 1
    if item.islower():
        return ord(item) - 96
    else:
        return ord(item) - 64 + 26

def get_common_element(first: str, second: str, third: str | None = None) -> str:
    common = set(first).intersection(set(second))
    if third is not None:
        common = common.intersection(set(third))
    assert len(common) == 1
    return common.pop()

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    value = 0
    for backpack in input:
        size = len(backpack)
        first, second = backpack[:size//2], backpack[size//2:]
        common = get_common_element(first, second)
        value += get_priority(common)
    
    badge_value = 0
    for i in range(0, len(input), 3):
        first, second, third = input[i:i+3]
        common = get_common_element(first, second, third)
        badge_value += get_priority(common)
    
    print("Part 1:", value)
    print("Part 2:", badge_value)

    