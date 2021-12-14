map = {}
with open('data9.txt') as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            map[(x, y)] = int(char)

def get_neighbours(x, y):
    return {(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)}

def is_low_point(x, y):
    return all(map.get(pos, 9) > map[(x, y)] for pos in get_neighbours(x, y))

def get_low_points():
    return [(x, y) for x, y in map if is_low_point(x, y)]

print("Part 1:")
print(sum(map[pos] + 1 for pos in get_low_points()))

def get_basin(pos):
    basin = {pos}
    follow(pos, basin)
    return basin

def follow(pos, basin):
    x, y = pos
    p1 = map[pos]
    map[pos] = 9 # mark cell visited
    for neighbour in get_neighbours(x, y):
                
        p2 = map.get(neighbour, 0)
        if p2 >= p1 and p2 != 9:            
            basin.add(neighbour)
            print(neighbour)
            
            follow(neighbour, basin)

from math import prod

print("Part 2:")
print(get_basin((2,2)))