import re
import tqdm

def get_distance(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def subtract_interval(main_interval, to_subtract):
    if (main_interval[1]<to_subtract[0]) or (main_interval[0]>to_subtract[1]):
        return [main_interval]
    elif (to_subtract[0]<=main_interval[0]) and (to_subtract[1]>=main_interval[1]):
        return []
    elif (to_subtract[0]<=main_interval[0]):
        return [(to_subtract[1]+1, main_interval[1])]
    elif (main_interval[1]<=to_subtract[1]):
        return [(main_interval[0],to_subtract[0]-1)]
    else:
        return [(main_interval[0],to_subtract[0]-1),
            (to_subtract[1]+1,main_interval[1])]

def subtract_from_all(intervals, to_subtract):
    new_intervals = []
    for interval in intervals:
        new_intervals.extend(subtract_interval(interval, to_subtract))
    return new_intervals

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [re.findall("-?\d+", row) for row in f.read().splitlines()]
    
    sensors = []
    distances = []
    beacons = []
    for row in input:
        sensor = (int(row[0]), int(row[1]))
        beacon = (int(row[2]), int(row[3]))
        distance = get_distance(sensor, beacon)
        sensors.append(sensor)
        beacons.append(beacon)
        distances.append(distance)

    min_x, max_x = min(sensors, key=lambda x: x[0])[0], max(sensors, key=lambda x: x[0])[0]
    max_distance = max(distances)

    unavailable = 0
    for x in tqdm.tqdm(range(min_x-max_distance, max_x+max_distance)):
        position = (x, 2000000)
        for sensor, distance, beacon in zip(sensors, distances, beacons):
            if (position != sensor) and (position != beacon) and (get_distance(position, sensor) <= distance):
                unavailable += 1
                break
    print("Part 1:", unavailable)

    dimension = 4000000
    for x in tqdm.tqdm(range(dimension+1)):
        unseen_intervals=[(0, dimension)]
        for sensor, distance, beacon in zip(sensors, distances, beacons):
            if abs(sensor[0]-x)<=distance:
                intersection = distance - abs(sensor[0]-x)
                seen_interval = (sensor[1]-intersection, sensor[1]+intersection)
                unseen_intervals = subtract_from_all(unseen_intervals, seen_interval)
                if len(unseen_intervals) == 0:
                    break
        if len(unseen_intervals) > 0:
            y = unseen_intervals[0][0]
            break
    print("Part 2:", x*4000000+y)
