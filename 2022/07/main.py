from functools import lru_cache

class Directory:
    def __init__(self, parent, name: str) -> None:
        self.parent = parent
        self.name: str = name
        self.subdirectories: list[Directory] = []
        self.files: list[File] = []
    
    @lru_cache()
    def get_size(self):
        file_size = [file.size for file in self.files]
        dir_size = [dir.get_size() for dir in self.subdirectories]
        return sum(file_size) + sum(dir_size)
    
    def add_subdirectory(self, dir):
        self.subdirectories.append(dir)

    def add_file(self, new_file):
        self.files.append(new_file)

class File:
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size

def add_sizes_threshold(dir: Directory, thr=100000):
    dir_size = dir.get_size()
    subdir_size = sum([add_sizes_threshold(subdir, thr) for subdir in dir.subdirectories])
    if dir_size <= thr:
        return dir_size + subdir_size
    else:
        return subdir_size

def find_smallest_subdir(dir: Directory, thr: int):
    candidates = [dir.get_size()]
    for subdir in dir.subdirectories:
        if subdir.get_size() >= thr:
            candidates.append(find_smallest_subdir(subdir, thr))
    return min(candidates)

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [row for row in f.read().splitlines()]
    
    base_dir = Directory(None, "/")
    current_dir = base_dir
    for cmd in input:
        if cmd.startswith("$ cd"):
            cmd = cmd.split(" ")[-1].strip()
            if cmd == "/":
                current_dir = base_dir
            elif cmd == "..":
                current_dir = current_dir.parent
            else:
                new_dir = Directory(current_dir, cmd)
                current_dir.add_subdirectory(new_dir)
                current_dir = new_dir
        elif cmd.startswith("dir") or cmd.startswith("$ ls"):
            pass
        else: 
            size, name = cmd.split(" ")
            new_file = File(name, int(size))
            current_dir.add_file(new_file)
    
    print("Part 1:", add_sizes_threshold(base_dir))

    needed_space = 30000000 - (70000000 - base_dir.get_size())
    print("Part 2:", find_smallest_subdir(base_dir, needed_space))