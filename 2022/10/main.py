def draw_cycle(cycle, value, width=40):
    position = (cycle-1)%width
    if value-1 <= position <= value+1:
        return "#"
    else:
        return "."

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [tuple(row.split(" ")) for row in f.read().splitlines()]
    
    value = 1
    cycle = 0
    milestones = [20, 60, 100, 140, 180, 220, len(input)*3]
    next_milestone = milestones.pop(0)
    milestone_values = []
    output = ""
    for i, instruction in enumerate(input):
        if len(instruction) == 2:
            next_cycle = cycle + 2
            if next_cycle >= next_milestone:
                milestone_values.append(value*next_milestone)
                next_milestone = milestones.pop(0)
            output += draw_cycle(cycle+1, value) + draw_cycle(cycle+2, value)
            cycle = next_cycle
            value += int(instruction[1])
        else:
            cycle += 1
            if cycle == next_milestone:
                milestone_values.append(value*next_milestone)
                next_milestone = milestones.pop(0)
            output += draw_cycle(cycle, value)
                
    print("Part 1:", sum(milestone_values))
    
    print("Part 2:")
    for i in range(6):
        print(output[i*40:(40+i*40)])