def parse_number(snail_string):
    open = 0
    for i, char in enumerate(snail_string):
        if char == "[":
            open += 1
        elif char == "]":
            open -= 1
        elif char == "," and open == 1:
            comma_index = i
            break
    first_digit = comma_index == 2 and snail_string[1].isdigit()
    second_digit = len(snail_string) - comma_index == 3 and snail_string[comma_index+1].isdigit()
    if first_digit and second_digit:
        return [int(snail_string[1]), int(snail_string[comma_index+1])]
    elif first_digit:
        return [int(snail_string[1]), parse_number(snail_string[comma_index+1:len(snail_string)-1])]
    elif second_digit:
        return [parse_number(snail_string[1:comma_index]), int(snail_string[comma_index+1])]
    else:
        return [parse_number(snail_string[1:comma_index]),  parse_number(snail_string[comma_index+1:len(snail_string)-1])]

def reduce(num):
    while True:
        exploded_num = explode(num)
        if exploded_num == num:
            split_num = split(num)
            if split_num == num:
                return num
            else:
                num = split_num
        else:
            num = exploded_num

def add(num1, num2):
    return ["["] + num1 + [","] + num2 + ["]"]

def explode(num):
    depth = 0
    explode_index = -1
    for i,char in enumerate(num):
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        if depth > 4 and type(num[i+1])==int and type(num[i+3])==int:
            explode_index = i
            break
    if explode_index == -1:
        return num
    else:
        left = num[explode_index+1]
        right = num[explode_index+3]
        num = num[:explode_index] + [0] + num[explode_index+5:]
        for right_index in range(explode_index+1,len(num),1):
            if type(num[right_index]) == int:
                new_digit = right + num[right_index]
                num = num[:right_index] + [new_digit] + num[right_index+1:]
                break
        for left_index in range(explode_index-1,0,-1):
            if type(num[left_index]) == int:
                new_digit = left + num[left_index]
                num = num[:left_index] + [new_digit] + num[left_index+1:]
                break
    return num

def split(num):
    for i in range(len(num)):
        if type(num[i]) == int and num[i] > 9:
            digit = num[i]
            return num[:i]+ ["[",digit//2,",",digit//2+digit%2,"]"] + num[i+1:]
    return num

def parse(input_str):
    parsed = []
    for char in input_str:
        if char.isdigit():
            parsed.append(int(char))
        else: parsed.append(char)
    return parsed

def magnitude(input):
    if type(input) == int:
        return input
    return 3*magnitude(input[0])+2*magnitude(input[1])

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [parse(x) for x in f.read().strip().splitlines()]

    summed = input[0]
    for row in input[1:]:
        summed = reduce(add(summed, row))
    print("Part 1:", magnitude(parse_number("".join([str(x) for x in summed]))))

    max_magnitude = 0
    for x in range(len(input)):
        for y in range(len(input)):
            if x != y:
                reduced = reduce(add(input[x], input[y]))
                mag = magnitude(parse_number("".join([str(x) for x in reduced])))
                max_magnitude = max(max_magnitude, mag)
    print("Part 2:", max_magnitude)