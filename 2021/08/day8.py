def count_occurences(signals, digit_lengths):
    occurrences = 0
    for signal in signals:
        output_readings = signal[-4:]
        occurrences += sum([1 if len(pattern) in digit_lengths else 0 for pattern in output_readings])
    return occurrences

def parse_signal(signal):
    mapping={}
    unique_signals = list(set(signal))
    for pattern in unique_signals:
        if len(pattern) == 2:
            mapping[1] = pattern
        elif len(pattern) == 3:
            mapping[7] = pattern
        elif len(pattern) == 4:
            mapping[4] = pattern
        elif len(pattern) == 7:
            mapping[8] = pattern
    for pattern in unique_signals:
        if len(pattern) == 6: # 0, 6, 9
            if all(digit in pattern for digit in mapping[4]):
                mapping[9] = pattern
            elif all(digit in pattern for digit in mapping[1]):
                mapping[0] = pattern
            else:
                mapping[6] = pattern
    for pattern in unique_signals:
        if len(pattern) == 5: # 2, 3, 5
            if all(digit in mapping[6] for digit in pattern):
                mapping[5] = pattern
            elif all(digit in mapping[9] for digit in pattern):
                mapping[3] = pattern
            else:
                mapping[2] = pattern
    output = 0
    for output_pattern, multiplier in zip(signal[-4:], [1000, 100, 10, 1]):
        for key, value in mapping.items():
            if value == output_pattern:
                output += key * multiplier
    return output

if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.read().splitlines()

    signals = [x.strip().split("|") for x in lines]
    signals = [x[0].strip().split(" ") + x[1].strip().split(" ") for x in signals]
    signals = [["".join(sorted(pattern)) for pattern in signal] for signal in signals]

    print("Part 1:", count_occurences(signals, [2, 3, 4, 7]))
    print("Part 2:", sum([parse_signal(signal) for signal in signals]))

