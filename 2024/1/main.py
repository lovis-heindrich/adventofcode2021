# %%


with open("input.txt", "r") as f:
    l1, l2 = map(list, zip(*(map(int, line.split()) for line in f)))

# %%
l1.sort()
l2.sort()

distance = sum([abs(x1 - x2) for x1, x2 in zip(l1, l2)])
print(distance)


# %%
# Part 2

counter = {}
for x in l2:
    counter[x] = counter.get(x, 0) + 1

similarity = sum([x*counter.get(x, 0) for x in l1])
print(similarity)

# %%
