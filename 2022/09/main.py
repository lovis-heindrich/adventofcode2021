def move_head(dir, head):
    match dir:
        case "U":
            head = (head[0], head[1]+1)
        case "D":
            head = (head[0], head[1]-1)
        case "L":
            head = (head[0]-1, head[1])
        case "R":
            head = (head[0]+1, head[1])
    return head

def adjust_tail(head, tail):
    hor_step = 1 if head[0]>tail[0] else -1
    vert_step = 1 if head[1]>tail[1] else -1
    # Diagonal movement
    if (abs(head[0] - tail[0]) > 1) and (abs(head[1] - tail[1]) > 0) or (abs(head[0] - tail[0]) > 0) and (abs(head[1] - tail[1]) > 1):
        tail = (tail[0] + hor_step, tail[1] + vert_step)
    # Horizontal movement
    elif (abs(head[0] - tail[0]) > 1):
        tail = (tail[0] + hor_step, tail[1])
    # Vertical movement
    elif (abs(head[1] - tail[1]) > 1):
        tail = (tail[0], tail[1] + vert_step)
    return tail

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row.split(" ") for row in f.read().splitlines()]
        input = [(row[0], int(row[1])) for row in input]
    
    head = (0,0)
    tail = (0,0)
    visited = set()
    for dir, n in input:
        for _ in range(n):
            head = move_head(dir, head)
            tail = adjust_tail(head, tail)
            visited.add(tail)
        
    print("Part 1:", len(visited))
    
    visited = set()
    knots = [(0, 0)]*10
    for dir, n in input:
        for _ in range(n):
            knots[0] = move_head(dir, knots[0])
            for head_index in range(len(knots)-1):
                head, tail = knots[head_index], knots[head_index+1]
                tail = adjust_tail(head, tail)
                knots[head_index+1] = tail
            visited.add(knots[-1])

    print("Part 2:", len(visited))