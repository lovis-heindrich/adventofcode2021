def window_sum(numbers, length):
    counter = 0
    for i in range(len(numbers)-length):
        if sum(numbers[i:i+length]) < sum(numbers[i+1:i+length+1]):
            counter += 1
    return counter

if __name__ == "__main__":
    with open('./data/day1.txt') as f:
        lines = [int(x) for x in f.read().splitlines()]
    
    print("Part 1:", window_sum(lines, 1)) 
    print("Part 2:", window_sum(lines, 3))