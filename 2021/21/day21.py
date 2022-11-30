from collections import Counter

def quantum_die(p1, p2, s1, s2, p1_active):
    if s1 >= 21:
        return 1, 0
    elif s2 >= 21:
        return 0, 1
    else:
        p1_wins, p2_wins = 0, 0
        for roll, occurrences in counter.items():
            if p1_active:
                p1_new = (p1+roll)%10
                p1_win, p2_win = quantum_die(p1_new, p2, s1+p1_new+1, s2, not p1_active)
            else:
                p2_new = (p2+roll)%10
                p1_win, p2_win = quantum_die(p1, p2_new, s1, s2+p2_new+1, not p1_active)
            p1_wins+=p1_win*occurrences
            p2_wins+=p2_win*occurrences
        return p1_wins, p2_wins
        
if __name__ == "__main__":
    with open("input.txt") as f:
        p1_init, p2_init = [int(input[-1])-1 for input in f.read().splitlines()]
    
    p1, p2 = p1_init, p2_init
    s1, s2 = 0, 0
    p1_active = True
    roll = 0
    total_rolls = 0
    while s1 < 1000 and s2 < 1000:
        total_rolls += 3
        sum_of_rolls = roll%100+1 + (roll+1)%100+1 + (roll+2)%100+1
        roll = (roll+3) % 100
        if p1_active:
            p1 = (p1 + sum_of_rolls) % 10
            s1 += p1+1
        else:
            p2 = (p2 + sum_of_rolls) % 10
            s2 += p2+1
        p1_active = not p1_active
    
    print("Part 1:", min(s1,s2)*total_rolls)

    counter = Counter()
    for roll1 in range(1,4):
            for roll2 in range(1,4):
                for roll3 in range(1,4):
                    counter[roll1 + roll2 + roll3] += 1
    
    print("Part 2:", max(quantum_die(p1_init, p2_init, 0, 0, True)))