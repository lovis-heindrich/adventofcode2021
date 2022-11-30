from collections import Counter

def pair_insertion(polymer, rules):
    new_polymer = ""
    for pair in zip(polymer, polymer[1:]):
        new_polymer += pair[0] + rules[pair[0]+pair[1]]
    new_polymer += polymer[-1]
    return new_polymer

def apply_insertions(polymer, rules, n):
    for _ in range(n):
        polymer = pair_insertion(polymer, rules)
    return polymer

def character_count(polymer):
    counter = Counter(polymer)
    counts = counter.most_common()
    return counts[0][1] - counts[-1][1]

def count_pairs(polymer, n, rules):
    pair_counter = {pair:0 for pair in rules.keys()}
    for pair in zip(polymer, polymer[1:]):
        pair_counter[pair[0] + pair[1]] += 1
    for _ in range(n):
        pair_counter_2 = {pair:0 for pair in rules.keys()}
        for key, count in pair_counter.items():
            if count > 0:
                new_pairs = key[0] + rules[key], rules[key] + key[1]
                pair_counter_2[new_pairs[0]] += count
                pair_counter_2[new_pairs[1]] += count
        pair_counter = pair_counter_2
    char_counter = {}
    for key, count in pair_counter.items():
        char_counter[key[0]] = char_counter.get(key[0], 0) + count
        char_counter[key[1]] = char_counter.get(key[1], 0) + count
    # Pairs count all characters twice except for starting and end character
    for char, count in char_counter.items():
        if count % 2 != 0:
            char_counter[char] += 1
        char_counter[char] = char_counter[char] // 2
    return max(char_counter.values()) - min(char_counter.values())

if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read().split("\n\n")

    template = input[0]
    rules = {rule.split(" -> ")[0]:rule.split(" -> ")[1] for rule in input[1].splitlines()}
    
    print("Part 1:", character_count(apply_insertions(template, rules, 10)))
    print("Part 1:", count_pairs(template, 10, rules))
    print("Part 2:", count_pairs(template, 40, rules))
