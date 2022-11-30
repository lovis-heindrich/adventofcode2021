import math

type_mapping = {0: "sum", 1: "prod", 2: "min", 3: "max", 5: "gt", 6: "lt", 7: "eq"}

def bit_length(binary, num_subpackets):
    length = 0
    for _ in range(num_subpackets):
        type_id = int(binary[3:6], 2)
        binary = binary[6:]
        length += 6
        if type_id == 4:
            label = int(binary[0])
            binary = binary[5:]
            length += 5
            while label:
                label = int(binary[0])
                binary = binary[5:]
                length += 5
        else:
            length_type = int(binary[0], 2)
            binary = binary[1:]
            length += 1
            if length_type == 0:
                sub_length = int(binary[0:15], 2)
                length += sub_length + 15
                binary = binary[sub_length+15:]
            elif length_type == 1:
                num_sub_subpackets = int(binary[0:11], 2)
                binary = binary[11:]
                length += 11
                sub_length = bit_length(binary, num_sub_subpackets)
                binary = binary[sub_length:]
                length += sub_length
    return length

def parse_rec(binary, depth=0):
    if not binary or not int(binary):
        return [], 0
    parse = []
    version = int(binary[0:3], 2)
    type_id = int(binary[3:6], 2)
    binary = binary[6:]
    if type_id == 4:
        label = int(binary[0])
        number = binary[1:5]
        binary = binary[5:]
        while label:
            label = int(binary[0])
            number += binary[1:5]
            binary = binary[5:]
        number = int(number, 2)
        parse.append(number)
        #print("-"*depth + str(number))
    else:
        length_type = int(binary[0])
        binary = binary[1:]
        if length_type == 0:
            length = int(binary[0:15], 2)
            binary = binary[15:]
        elif length_type == 1:
            num_subpackets = int(binary[0:11], 2)
            binary = binary[11:]
            length = bit_length(binary, num_subpackets)
        #print("-"*depth + type_mapping[type_id], length_type)
        subpacket_content, subpacket_version = parse_rec(binary[0:length], depth+1)
        binary = binary[length:]
        parse.append([type_mapping[type_id], subpacket_content])
        version += subpacket_version
    next_parse, next_version = parse_rec(binary, depth)
    return parse + next_parse, version + next_version

def evaluate(transmission):
    if type(transmission)==int:
        return transmission
    elif type(transmission[0])==list and len(transmission) == 1:
        return evaluate(transmission[0])
    elif type(transmission[0]) == str:
        arguments = [evaluate(x) for x in transmission[1]]
        match (transmission[0]):
            case "sum":
                return sum(arguments)
            case "prod":
                return math.prod(arguments)
            case "min":
                return min(arguments)
            case "max":
                return max(arguments)
            case "gt":
                return int(arguments[0] > arguments[1])
            case "lt":
                return int(arguments[0] < arguments[1])
            case "eq":
                return int(arguments[0] == arguments[1])
            case _:
                print("Unknown command", transmission[0])
    else:
        assert 0, "Unknown transmission" + str(transmission)

if __name__ == "__main__":
    with open("input.txt") as f:
        hex_str = f.read().strip()
        
    input = int(hex_str, 16)
    binary = str(bin(input))[2:]
    if len(binary)<len(hex_str)*4:
        binary = "0"*(len(hex_str)*4-len(binary)) + binary

    parse, ver = parse_rec(binary)
    print("Part 1:", ver)
    print("Part 2:", evaluate(parse))