# %%
with open("input.txt", "r") as f:
    reports = [list(map(int, line.split())) for line in f.readlines()]

# %%
def is_safe(report: list[int], increasing=None) -> bool:
    if len(report) <= 1:
        return True
    if increasing is None:
        increasing = report[0] < report[1]
        return is_safe(report, increasing)
    if increasing and (report[0] < report[1]) and (abs(report[0] - report[1]) >= 1) and (abs(report[0] - report[1]) <= 3):
        return is_safe(report[1:], increasing)  
    elif not increasing and (report[0] > report[1]) and (abs(report[0] - report[1]) >= 1) and (abs(report[0] - report[1]) <= 3):
        return is_safe(report[1:], increasing)
    return False

print(sum(is_safe(report) for report in reports))

# %%
def is_safe_dampened(report: list[int], errors = 0, increasing = None) -> bool:
    if len(report) <= 1:
        return True
    if increasing is None:
        return is_safe_dampened(report, increasing=True) or is_safe_dampened(report[1:], errors=1, increasing=True) or is_safe_dampened(report, increasing=False) or is_safe_dampened(report[1:], errors=1, increasing=False)
    if increasing and (report[0] < report[1]) and (abs(report[0] - report[1]) >= 1) and (abs(report[0] - report[1]) <= 3):
        return is_safe_dampened(report[1:], errors, increasing=True)
    elif not increasing and (report[0] > report[1]) and (abs(report[0] - report[1]) >= 1) and (abs(report[0] - report[1]) <= 3):
        return is_safe_dampened(report[1:], errors, increasing=False)
    elif errors == 0:
        return is_safe_dampened(report[:1] + report[2:], errors=errors+1, increasing=increasing)
    return False

print(sum(is_safe_dampened(report) for report in reports))
