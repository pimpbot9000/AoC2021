from utils import load_data

rots = [lambda x, y, z: (x, y, z),
        lambda x, y, z: (y, z, x),
        lambda x, y, z: (z, x, y),
        lambda x, y, z: (-x, z, y),
        lambda x, y, z: (z, y, -x),
        lambda x, y, z: (y, -x, z),
        lambda x, y, z: (x, z, -y),
        lambda x, y, z: (z, -y, x),
        lambda x, y, z: (-y, x, z),
        lambda x, y, z: (x, -z, y),
        lambda x, y, z: (-z, y, x),
        lambda x, y, z: (y, x, -z),
        lambda x, y, z: (-x, -y, z),
        lambda x, y, z: (-y, z, -x),
        lambda x, y, z: (z, -x, -y),
        lambda x, y, z: (-x, y, -z),
        lambda x, y, z: (y, -z, -x),
        lambda x, y, z: (-z, -x, y),
        lambda x, y, z: (x, -y, -z),
        lambda x, y, z: (-y, -z, x),
        lambda x, y, z: (-z, x, -y),
        lambda x, y, z: (-x, -z, -y),
        lambda x, y, z: (-z, -y, -x),
        lambda x, y, z: (-y, -x, -z),
        ]

def parse_data():
    data = load_data("data/data19.txt")
    scanners = []
    coordinates = []

    for row in data:
        if row == "" or row == "end":
            coordinates.append((0, 0, 0, 1)) # append scanners to probe list
            scanners.append(coordinates)
            coordinates = []
        elif row[0:2] == "--":
            pass
        else:
            coordinates.append([int(x) for x in row.split(",")])
    return scanners

scanners = parse_data()

def zero(point, coordinates):
    # Shift coordinates that param point becomes the new zero
    x, y, z = point[0], point[1], point[2]
    new_coordinates = [(X[0] - x, X[1] - y, X[2] - z, X[3]) if len(X) == 4 else (X[0] - x, X[1] - y, X[2] - z) for X in coordinates]
    return new_coordinates


def match(scanner1, scanner2):
    max_union = set()
    for rot in rots:
        rotated_coordinates = [rot(x[0], x[1], x[2]) if len(x) == 3 else rot(x[0], x[1], x[2]) + tuple((1,)) for x in scanner2]
        for coord in rotated_coordinates:
            sc2_coordinates = zero(coord, rotated_coordinates)  # new zero for scanner2
            sc1 = set(scanner1)
            sc2 = set(sc2_coordinates)
            intersection = sc1.intersection(sc2)
            if len(intersection) > 11:
                print("match!!")
                return sc1.union(sc2)

    return max_union


def manhattan(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

def calculate_distances(coords):
    coords = list(filter(lambda x: len(x) == 3, coords))
    distances = set() 
    for i in range(0, len(coords) - 1):
        for j in range(i + 1, len(coords)):
            distances.add(manhattan(coords[i], coords[j]))
    return distances

def match_pairwise(scanners):
    unions = []
    # match scanners pairwise
    for i in range(0, len(scanners) - 1):
        for j in range(i + 1, len(scanners)):
            print("match", i, j)
            scanner1 = scanners[i]
            scanner2 = scanners[j]
            # Check if contains same distances
            # If not, does not overlap
            distances1 = calculate_distances(scanner1)
            distances2 = calculate_distances(scanner2)
            if len(distances1.intersection(distances2)) < 70:
                continue
            for s in scanner1:
                scanner1_zeroed = zero(s, scanner1)
                # scanner 2 coordinates are permutated.
                m = match(scanner1_zeroed, scanner2)
                if len(m) > 0:
                    unions.append((set((i, j)), m))
                    break
    return unions

def match2(union1, union2):

    for point in union1:
        scanner1_zero = zero(point, union1)
        # scanner 2 coordinates are permutated.
        m = match(scanner1_zero, union2)
        if len(m) > 0:
            return m

unions = match_pairwise(scanners)

used = set((0,))
total_union = unions[0][1]
contains = unions[0][0]

while len(contains) != len(scanners):
    for i in range(len(unions)):
        if i not in used:
            if len(contains.intersection(unions[i][0])) > 0:
                print("Union:", contains.union(unions[i][0]))
                used.add(i)
                total_union = match2(total_union, unions[i][1])
                contains = contains.union(unions[i][0])

                
print("result")
print(len(total_union) - len(scanners))

probes = list(filter(lambda x: len(x) == 4, total_union))
print(probes)

max_manhattan = 0
for i in range(0, len(probes) - 1):
    for j in range(i+1, len(probes)):
        max_manhattan = max(manhattan(probes[i], probes[j]), max_manhattan)
print(max_manhattan)
