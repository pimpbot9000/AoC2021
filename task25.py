"""
    Original code from Reddit for playing around and testing stuff
"""

from utils import load_data


class SeaFloor:
    def __init__(self, data):
        self.points = {}
        self.shape = (len(data), len(data[0]))
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if data[i][j] != '.':
                    self.points[(i, j)] = data[i][j]

    def print(self):
        for i in range(self.shape[0]):
            print(''.join(self.points.get((i, j), '.')
                  for j in range(self.shape[1])))

    def move(self, symbol, f):
        has_moved = False
        new_points = {}
        moved = set()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.points.get((i, j)) == symbol:
                    next_coord = f((i, j))

                    if not self.points.get(next_coord):
                        has_moved = True
                        new_points[next_coord] = symbol
                        moved.add((i, j))
                    else:
                        new_points[(i, j)] = symbol

        for point in moved:
            self.points.pop(point)

        self.points.update(new_points)
        return has_moved

    def move_east(self):
        return self.move('>', lambda c: (c[0], (c[1] + 1) % self.shape[1]))

    def move_south(self):
        return self.move('v', lambda c: ((c[0] + 1) % self.shape[0], c[1]))

    def move_both_directions(self):
        has_moved_east = self.move_east()
        has_moved_south = self.move_south()
        return has_moved_east or has_moved_south


data = load_data('data/data25.txt')
s = SeaFloor(data)
s.print()
print("-----------")
has_moved = True
counter = 0
while has_moved:
    counter += 1
    has_moved = s.move_both_directions()
    if counter % 100:
        print("...thinking")

print(counter)
