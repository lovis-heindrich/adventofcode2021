if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    all_inventories = []
    current_inventory = 0
    for item in input:
        if item is not "":
            current_inventory += int(item)
        else:
            all_inventories.append(current_inventory)
            current_inventory = 0
    
    all_inventories.sort()
    print("Part 1:", all_inventories[-1])
    print("Part 2:", sum(all_inventories[-3:]))

