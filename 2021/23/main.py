from typing import List
import random

column_index = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

move_cost = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

known_positions=set()
cutoff = None

class Column:
    def __init__(self, name: str, values: List[int], column_length):
        self.name = name
        self.values = values
        self.column_length = column_length

    def move_out(self):
        assert len(self.values)>0, "Moving out not possible on empty column"
        move_out_distance = (self.column_length+1)-len(self.values)
        value = self.values.pop(0)
        return value, move_out_distance

    def move_in(self, value):
        assert len(self.values)<self.column_length, "Moving in not possible on full column"
        move_in_distance = self.column_length-len(self.values)
        self.values.insert(0, value)
        return move_in_distance

    def is_complete(self):
        return self.sorted() and len(self.values) == self.column_length

    def copy(self):
        return Column(self.name, [v for v in self.values], self.column_length)
    
    def to_string(self):
        return "."*(self.column_length - len(self.values)) + "".join(self.values)
    
    def sorted(self):
        return all(v==self.name for v in self.values)

class Env:
    def __init__(self, columns: List[Column], hallway: List[str]=[".", ".", ".", ".", ".",".",".",".",".",".","."], distance=0):
        self.hallway = hallway
        self.columns = columns
        self.total_distance = distance

    def move(self, mode: str, origin_col: str, dest_col: str, hallway_index: int):
        if mode == "ch":
            column = next(c for c in self.columns if c.name == origin_col)
            value, distance = column.move_out()
            self.hallway[hallway_index] = value
            hallway_distance = abs(column_index[column.name]-hallway_index)
            cost = (distance + hallway_distance)*move_cost[value]
        elif mode == "cc":
            column = next(c for c in self.columns if c.name == origin_col)
            dest_column = next(c for c in self.columns if c.name == dest_col)
            value, distance = column.move_out()
            move_in_distance = dest_column.move_in(value)
            hallway_distance = abs(column_index[origin_col]-column_index[dest_col])
            cost = (distance + move_in_distance + hallway_distance)*move_cost[value]
        elif mode == "hc":
            dest_column = next(c for c in self.columns if c.name == dest_col)
            value = self.hallway[hallway_index]
            self.hallway[hallway_index] = "."
            move_in_distance = dest_column.move_in(value)
            hallway_distance = abs(column_index[dest_col]-hallway_index)
            cost = (move_in_distance + hallway_distance)*move_cost[value]
        else:
            assert False, "Unkown movement command: " + mode
        self.total_distance += cost
        return cost

    def available_moves(self):
        available = []
        # Move from col to hallway
        for column in self.columns:
            if not column.is_complete() and not len(column.values)==0 and not column.sorted():
                value = column.values[0]
                start_index = column_index[column.name]
                for i in range(start_index-1, -1, -1):
                    if self.hallway[i] != ".":
                        break
                    else:
                        if i not in column_index.values():
                            available.append(("ch", column.name, None, i))
                for i in range(start_index, len(self.hallway)):
                    if self.hallway[i] != ".":
                        break
                    else:
                        if i not in column_index.values():
                            available.append(("ch", column.name, None, i))
        # Move from col to other col
        for column in self.columns:
            if not column.is_complete() and len(column.values)>0:
                value = column.values[0]
                hallway_index = column_index[column.name]
                for destination_column in self.columns:
                    if column.name != destination_column.name and value == destination_column.name and destination_column.sorted():
                        destination_index = column_index[destination_column.name]
                        step = 1 if hallway_index > destination_index else -1
                        if all(self.hallway[x]=="." for x in range(destination_index, hallway_index, step)):
                            available.append(("cc", column.name, destination_column.name, None))
        # Move from hallway to col
        for i, element in enumerate(self.hallway):
            if element != ".":
                target_index = column_index[element]
                column = next(c for c in self.columns if c.name == element)
                step = 1 if i > target_index else -1
                if all(self.hallway[x]=="." for x in range(target_index, i, step)) and column.sorted():
                    available.append(("hc", None, column.name, i))
        return available

    def copy(self):
        return Env(columns=[c.copy() for c in self.columns], hallway=[v for v in self.hallway], distance=self.total_distance)

    def print(self):
        empty_line = "#"*(len(self.hallway)+2)
        print(empty_line)
        print("#"+"".join(self.hallway)+"#")
        padded_columns = [c.to_string() for c in self.columns]
        for i in range(len(padded_columns[0])):
            line = "###"
            for c in padded_columns:
                line += c[i] + "#"
            line += "##"
            print(line)
        print(empty_line)
        print()

    def to_string(self):
        return "".join(self.hallway + [c.to_string() for c in self.columns])

    def is_complete(self):
        return all(c.is_complete() for c in self.columns)

def iterate(env: Env):
    global cutoff
    if env.is_complete():
        if cutoff is None:
            cutoff = env.total_distance
        else:
            cutoff = min(cutoff, env.total_distance)
        return env.total_distance
    if cutoff and env.total_distance >= cutoff:
        return None
    available_moves = env.available_moves()
    if not len(available_moves):
        return None
    scores = []
    # Immediately move into correct columns to save runtime
    for move in available_moves:
        if move[0] == "cc" or move[0] == "hc":
            env_copy = env.copy()
            env_copy.move(*move)
            return iterate(env_copy)
    for move in available_moves:
        env_copy = env.copy()
        env_copy.move(*move)
        score = iterate(env_copy)
        if score is not None:
            scores.append(score)
    if not len(scores):
        return None
    return min(scores)

if __name__ == "__main__":
    columns = [Column("A", ["D", "B"], 2),
        Column("B", ["D", "A"], 2),
        Column("C", ["C", "A"], 2),
        Column("D", ["B", "C"], 2)]
    hallway = [".", ".", ".", ".", ".",".",".",".",".",".","."]
    env = Env([c.copy() for c in columns], [x for x in hallway])
    cutoff = None
    print("Part 1:", iterate(env))

    columns = [Column("A", ["D", "D", "D", "B"], 4),
        Column("B", ["D", "C", "B", "A"], 4),
        Column("C", ["C", "B", "A", "A"], 4),
        Column("D", ["B", "A", "C", "C"], 4)]
    hallway = [".", ".", ".", ".", ".",".",".",".",".",".","."]
    env = Env([c.copy() for c in columns], [x for x in hallway])
    cutoff = None
    print("Part 2:", iterate(env))