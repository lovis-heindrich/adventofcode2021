import tqdm
class Cave:
    def __init__(self, commands, width=7) -> None:
        self.width = width
        self.lowest = 0
        self.trimmed_height = 0
        self.num_dropped = 0
        self.num_steps = 0
        self.next_command = "push"
        self.commands = command_gen(commands)
        self.grid = [[2]*7]
        self.next_shape = shapes_gen()
        self.new_shape = True

    def __repr__(self) -> str:
        str_rep = "\n"
        for row in self.grid:
            str_rep += str(row)+"\n"
        return str_rep
    
    def step(self):
        self.num_steps += 1
        if self.new_shape:
            self.num_dropped += 1
            self.make_empty_rows()
            self.grid = get_shape(next(self.next_shape)) + self.grid
            self.next_cmd = "push"
            self.new_shape = False
        if self.next_cmd == "push":
            self.next_cmd = "fall"
            first, last = self.get_moving_row_indices()
            next_command, next_command_index = next(self.commands)
            left = (next_command == "<")
            #print("push", left, self.is_side_blocked(left, first, last))
            if not self.is_side_blocked(left, first, last):
                for row_i, row in zip(range(first,last+1), self.grid[first:last+1]):
                    if left:
                        for col_i, element in enumerate(row):
                            if (col_i<len(row)-1) and (self.grid[row_i][col_i+1]==1):
                                self.grid[row_i][col_i]=1
                            elif (element==1):
                                self.grid[row_i][col_i]=0
                    else:
                        for col_i, element in reversed(list(enumerate(row))):
                            if (col_i>=1) and (self.grid[row_i][col_i-1]==1):
                                self.grid[row_i][col_i]=1
                            elif (element==1):
                                self.grid[row_i][col_i]=0
        elif self.next_cmd == "fall":
            self.next_cmd = "push"
            first, last = self.get_moving_row_indices()
            if self.is_blocked(first, last):
                for row_i, row in zip(range(first,last+1), self.grid[first:last+1]):
                    self.grid[row_i] = [x if (x!=1) else 2 for x in row]
                self.new_shape=True
            else:
                for row_i, row in reversed(list(zip(range(first, last+2), self.grid[first:last+2]))):
                    new_row = []
                    for col_i, element in enumerate(row):
                        if self.grid[row_i-1][col_i]==1:
                            new_row.append(1)
                        elif element == 1:
                            new_row.append(0)
                        else:
                            new_row.append(element)
                    self.grid[row_i] = new_row
    
    def process_shape(self):
        if self.new_shape:
            self.step()
            while not self.new_shape:
                self.step()
        
    def get_moving_row_indices(self):
        first, last = None, None
        for row_i, row in enumerate(self.grid):
            if (1 in row) and (first==None):
                first = row_i
            if (1 not in row) and (first!=None):
                last = row_i - 1
                return first, last

    def is_side_blocked(self, left=True, first=None, last=None):
        for row_i, row in zip(range(first,last+1), self.grid[first:last+1]):
            for col_i, element in enumerate(row):
                if (element==1) and left:
                    if (col_i==0) or (self.grid[row_i][col_i-1]==2):
                        return True
                elif (element==1) and (not left):
                    if (col_i==len(row)-1) or (self.grid[row_i][col_i+1]==2):
                        return True
        return False

    def height(self):
        empty = 0
        for row in self.grid:
            if sum(row) == 0:
                empty += 1
            else:
                break
        floor = 1 if self.trimmed_height==0 else 1
        return len(self.grid)-empty-floor+self.trimmed_height
    
    def trim_floor(self):
        indices = []
        for col_i in range(len(self.grid[0])):
            for row_i in range(len(self.grid)):
                if self.grid[row_i][col_i] == 2:
                    indices.append(row_i)
                    break
        assert len(indices)==len(self.grid[0])
        highest = max(indices)
        trimmed = len(self.grid) - highest - 1
        self.trimmed_height += trimmed
        self.grid = self.grid[:highest+1]

    def is_blocked(self, first=None, last=None):
        if (first==None) or (last==None):
            first = 0
            last = len(self.grid)
        for row_i, row in zip(range(first, last+1), self.grid[first:last+1]):
            for col_i, element in enumerate(row):
                if (element == 1) and (self.grid[row_i+1][col_i] == 2):
                    return True
        return False

    def make_empty_rows(self, n=3):
        count = 0
        for row in self.grid:
            if sum(row)==0:
                count += 1
            else:
                break
        if count > n:
            self.grid = self.grid[(count-n):]
        elif n > count:
            for row in range(n - count):
                self.grid.insert(0, [0]*self.width)

def command_gen(commands):
    index = 0
    while True:
        yield commands[index], index
        index = (index+1)%len(commands)

def shapes_gen():
    shapes = ["-", "+", "L", "I", "o"]
    index = 0
    length = len(shapes)
    while True:
        yield shapes[index]
        index = (index+1)%length

def get_shape(shape, width=7, left_distance=2):
    match shape:
        case "-":
            row_1 = [0]*left_distance + [1, 1, 1, 1] + [0]*(width-left_distance-4)
            return [row_1]
        case "+":
            row_1 = [0]*left_distance + [0, 1, 0] + [0]*(width-left_distance-3)
            row_2 = [0]*left_distance + [1, 1, 1] + [0]*(width-left_distance-3)
            row_3 = [0]*left_distance + [0, 1, 0] + [0]*(width-left_distance-3)
            return [row_1, row_2, row_3]
        case "L":
            row_1 = [0]*left_distance + [0, 0, 1] + [0]*(width-left_distance-3)
            row_2 = [0]*left_distance + [0, 0, 1] + [0]*(width-left_distance-3)
            row_3 = [0]*left_distance + [1, 1, 1] + [0]*(width-left_distance-3)
            return [row_1, row_2, row_3]
        case "I":
            row_1 = [0]*left_distance + [1] + [0]*(width-left_distance-1)
            row_2 = [0]*left_distance + [1] + [0]*(width-left_distance-1)
            row_3 = [0]*left_distance + [1] + [0]*(width-left_distance-1)
            row_4 = [0]*left_distance + [1] + [0]*(width-left_distance-1)
            return [row_1, row_2, row_3, row_4]
        case "o":
            row_1 = [0]*left_distance + [1, 1] + [0]*(width-left_distance-2)
            row_2 = [0]*left_distance + [1, 1] + [0]*(width-left_distance-2)
            return [row_1, row_2]
        case _:
            assert False, f"Unsupported shape {shape}"

if __name__ == "__main__":
    with open("input.txt") as f:
        commands = [cmd for cmd in f.read().strip()]
    
    #commands = [cmd for cmd in ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]
    cave = Cave(commands)

    for i in range(2022):
        cave.process_shape()
    print("Part 1:", cave.height())

    cave = Cave(commands)
    last_height = 0
    for i in range(10):
        for _ in range(len(commands)):
            cave.process_shape()
        print(i, cave.height()-last_height)
        last_height = cave.height()
    # command_length = len(commands)
    # cave = Cave(commands)
    # for i in range(command_length):
    #     cave.process_shape()
    # first_height = cave.height()
    # for i in range(command_length):
    #     cave.process_shape()
    # second_height = cave.height() - first_height
    # remaining_steps = 1000000000000%command_length
    # for i in range(remaining_steps):
    #     cave.process_shape()
    # remaining_height = cave.height() - first_height - second_height
    # print("Part 2:", first_height + ((1000000000000)//command_length)*second_height + remaining_height)