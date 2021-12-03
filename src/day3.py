import numpy as np

def column_filter(m, filter):
    for i in range(m.shape[1]):
        mean = m[:,i].mean()
        value = filter if mean >= 0.5 else 1-filter
        m = m[m[:,i]==value, :]
        if len(m) == 1:
            return m.flatten()

def binary_arr_to_int(arr):
    arr_str = "".join([str(x) for x in arr])
    return int(arr_str, 2)

if __name__ == "__main__":
    with open("./data/day3.txt") as f:
        lines = [list(x) for x in f.read().splitlines()]
    m = np.array(lines, dtype=int)

    gamma_arr = np.mean(m, axis=0).round(0).astype(int)
    eps_arr = np.mean(1-m, axis=0).round(0).astype(int)
    gamma = binary_arr_to_int(gamma_arr)
    eps = binary_arr_to_int(eps_arr)
    print(f"Gamma {gamma} * Epsilon {eps} = {gamma*eps}")

    oxygen_arr = column_filter(m, 1)
    co2_arr = column_filter(m, 0)
    oxygen = binary_arr_to_int(oxygen_arr)
    co2 = binary_arr_to_int(co2_arr)
    print(f"Oxygen {oxygen} * CO2 {co2} = {oxygen * co2}")
