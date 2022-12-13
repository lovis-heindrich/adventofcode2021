import json

def check_pair(left, right):
    for l, r in zip(left, right):
        if (type(l) == int) and (type(r) == int):
            if l < r:
                return True
            elif l > r:
                return False
        else:
            if type(l) == int:
                l = [l]
            elif type(r) == int:
                r = [r]
            result = check_pair(l, r)
            if result is not None:
                return result
    if len(left)<len(right):
        return True
    elif len(left)>len(right):
        return False
    else:
        return None

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [pair for pair in f.read().split("\n\n")]
    
    pairs = []
    for pair in input:
        pair = pair.splitlines()
        left, right = json.loads(pair[0]), json.loads(pair[1])
        pairs.append([left, right])

    correct = 0
    for i, pair in enumerate(pairs):
        result = check_pair(pair[0], pair[1])
        if result:
            correct += (i+1)
    
    print("Part 1:", correct)

    all_packets = [[[6]], [[2]]]
    for pair in pairs:
        all_packets.extend(pair)
    
    for end in range(len(all_packets)-1, 1, -1):
        for i in range(end):
            left = all_packets[i]
            right = all_packets[i+1]
            correct = check_pair(left, right)
            if not correct:
                all_packets[i] = right
                all_packets[i+1] = left
    
    indices = []
    for i, packet in enumerate(all_packets):
        if packet == [[2]]:
            indices.append(i+1)
        elif packet == [[6]]:
            indices.append(i+1)
    
    print("Part 2:", indices[0]*indices[1])