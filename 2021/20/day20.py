def pad_image(image, n=3, char="0"):
    image = [char*n+row+char*n for row in image]
    empty_row = char*len(image[0])
    for i in range(n):
        image.insert(0, empty_row)
        image.append(empty_row)
    return image

def apply_filter(filter, image):
    new_image = [["0" for _ in range(len(image[0])-2)] for _ in range(len(image)-2)]
    for x in range(1,len(image)-1):
        for y in range(1, len(image[0])-1):
            bin_str = image[x-1][y-1:y+2] + image[x][y-1:y+2] + image[x+1][y-1:y+2]
            index = int(bin_str, 2)
            if filter[index]:
                new_image[x-1][y-1] = "1"
    new_image = ["".join(row) for row in new_image]
    return new_image

if __name__ == "__main__":
    with open("./data/day20.txt") as f:
        filter, image = f.read().split("\n\n")
    
    filter = [1 if element == "#" else 0 for element in filter]
    image = ["".join(["1" if element == "#" else "0" for element in row]) for row in image.splitlines()]

    image = pad_image(image, n=2*50)
    for i in range(2):
        image = apply_filter(filter, image)
    
    lit = lambda img: sum([sum([1 for char in row if char == "1"]) for row in img])
    print("Part 1:", lit(image))

    for i in range(48):
        image = apply_filter(filter, image)
    
    print("Part 2:", lit(image))