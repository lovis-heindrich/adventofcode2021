closing_dict = {")":"(", "]":"[", "}":"{", ">":"<"}
illegal_scores = {")":3, "]":57, "}":1197, ">":25137}
missing_scores = {"(":1, "[":2, "{":3, "<":4}
opening_characters = ["(", "[", "{", "<"]

def find_illegal_closing_char(row):
    queue = []
    for char in row:
        if char in opening_characters:
            queue.append(char)
        elif queue[-1] == closing_dict[char]:
            queue.pop()
        else:
            return illegal_scores[char]
    return 0

def find_missing_chars(row):
    queue = []
    for char in row:
        if char in opening_characters:
            queue.append(char)
        elif queue[-1] == closing_dict[char]:
            queue.pop()
    score = 0
    for element in queue[::-1]:
        score = (score*5) + missing_scores[element]
    return score
    
if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    corrupted_sum = 0
    missing_row = []
    for row in input:
        corrupted_value = find_illegal_closing_char(row)
        corrupted_sum += corrupted_value
        if corrupted_value == 0:
            missing_row.append(find_missing_chars(row))

    print("Part 1:", corrupted_sum)

    missing_row.sort()
    print("Part 2:", missing_row[len(missing_row)//2])

    
