def get_marker_index(package: str, marker_length=4) -> int:
    for i in range(len(package)-marker_length):
        package_sequence = package[i:i+marker_length]
        if len(set(package_sequence)) == marker_length:
            return i+marker_length

if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read().strip()

    package_marker = get_marker_index(input)
    message_marker = package_marker + get_marker_index(input[package_marker:], marker_length=14)
    print("Part 1:", package_marker)
    print("Part 2:", message_marker)