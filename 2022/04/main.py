def parse_range(input: str) -> tuple[int, int]:
    start, end = input.strip().split("-")
    return int(start), int(end)

def parse_pair(input: str) -> tuple[tuple[int, int], tuple[int, int]]:
    first, second = input.split(",")
    return parse_range(first), parse_range(second) 

def contains(first: tuple[int, int], second: tuple[int, int]) -> bool:
    first_contains = (first[0] <= second[0]) & (first[1] >= second[1])
    second_contains = (second[0] <= first[0]) & (second[1] >= first[1])
    return first_contains or second_contains

def overlaps(first: tuple[int, int], second: tuple[int, int]) -> bool:
    return not ((first[1] < second[0]) or (second[1] < first[0]))

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [parse_pair(row) for row in f.read().splitlines()]
    
    num_contains = sum([contains(first, second) for first, second in input])
    print("Part 1:", num_contains)

    num_overlaps = sum([overlaps(first, second) for first, second in input])
    print("Part 2:", num_overlaps)