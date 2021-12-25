from utils import load_data


class SeaFloor:
    def __init__(self, data):
        self.shape = (len(data), len(data[0]))
        self.points = {(i, j): data[i][j] for i in range(self.shape[0]) for j in range(self.shape[1]) if data[i][j] != '.'}

    def print(self):
        for i in range(self.shape[0]):
            print(''.join(self.points.get((i, j), '.')
                  for j in range(self.shape[1])))

    def move(self, moving_symbol, move_to):
        has_moved = False
        new_points = {}

        for (i, j), symbol in self.points.items():
            if symbol == moving_symbol:

                next_coord = move_to((i, j))

                if not self.points.get(next_coord):
                    has_moved = True
                    new_points[next_coord] = moving_symbol
                else:
                    new_points[(i, j)] = moving_symbol

            elif symbol:
                new_points[(i, j)] = symbol

        self.points = new_points
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
sea_floor = SeaFloor(data)
sea_floor.print()
print("-----------")
has_moved = True
counter = 0
while has_moved:
    counter += 1
    has_moved = sea_floor.move_both_directions()
    if counter % 100 == 0:
        print("...thinking:", (counter // 100) * 100)

print(counter)
