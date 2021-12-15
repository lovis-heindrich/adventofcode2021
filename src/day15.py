import math
import itertools

def dijkstra(grid, start, goal):
    all_nodes = list(itertools.product(list(range(goal[0]+1)), list(range(goal[1]+1))))
    distance = {(x,y):math.inf for x,y in all_nodes}
    distance[start] = 0
    parent = {}
    Q = [(x,y) for x,y in all_nodes]
    while len(Q):
        u = min(Q, key=distance.get)
        if u == goal:
            return distance[goal]
        Q.remove(u)
        for v in [(x,y) for (x,y) in [(u[0]-1, u[1]), (u[0],u[1]-1), (u[0]+1, u[1]), (u[0],u[1]+1)] if x>=0 and y>=0 and x<=goal[0] and y<=goal[1]]:
            if v in Q:
                if distance[u] + grid[v[0]][v[1]] < distance[v]:
                    distance[v] = distance[u] + grid[v[0]][v[1]]
                    parent[v] = u
    return distance[goal]

def manhattan(node1, node2, D=1):
    dx = abs(node1[0] - node2[0])
    dy = abs(node1[1] - node2[1])
    return D * (dx + dy)

def a_star(grid, start, goal):
    open_nodes = {start}
    closed_nodes = set() # More than 10x speedup compared to list
    g = {start: 0}
    f = {start: manhattan(start, goal)}
    parent = {}
    while len(open_nodes):
        u = min(open_nodes, key=lambda node: g[node] + f[node])
        if u == goal:
            return g[goal]
        open_nodes.remove(u)
        closed_nodes.add(u)
        for v in [(x,y) for (x,y) in [(u[0]-1, u[1]), (u[0],u[1]-1), (u[0]+1, u[1]), (u[0],u[1]+1)] if x>=0 and y>=0 and x<=goal[0] and y<=goal[1]]:
            if v not in closed_nodes:
                if v not in open_nodes:
                    open_nodes.add(v)
                    g[v] = g[u] + grid[v[0]][v[1]]
                    f[v] = manhattan(v, goal)
                    parent[v] = u
                elif g[u] + grid[v[0]][v[1]] < g[v]:
                    g[v] = g[u] + grid[v[0]][v[1]]
                    parent[v] = u
    return g[goal]

if __name__ == "__main__":
    with open("./data/day15.txt") as f:
        input = [[int(x) for x in row] for row in f.read().splitlines()]

    start = (0,0)
    goal = (len(input)-1, len(input[0])-1)

    print("Part 1:", a_star(input, start, goal))

    num_rows = len(input)
    num_columns = len(input[0])

    for _ in range(4):
        new_rows=[]
        for row in input[-num_rows:]:
            new_rows.append([x+1 if x<9 else 1 for x in row])
        input.extend(new_rows)
    for row in input:
        for _ in range(4):
            row.extend([x+1 if x<9 else 1 for x in row[-num_columns:]])

    goal = (len(input)-1, len(input[0])-1)
    print("Part 2:", a_star(input, start, goal))
