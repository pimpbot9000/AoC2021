from utils import load_data


def load_and_parse():
    # Loads and maps # -> 1 and . -> 0
    data = load_data("data/data20.txt")
    algorithm = [1 if x == "#" else 0 for x in data[0]]

    rows = []
    for i in range(2, len(data)):
        r = [1 if x == "#" else 0 for x in data[i]]
        rows.append(r)
    return algorithm, rows


algorithm, rows = load_and_parse()


class Image:
    def __init__(self, algorithm, rows):
        self.algorithm = algorithm
        self.points = set()
        self.padding = 2
        self.points = {(i, j) for i in range(len(rows))
                       for j in range(len(rows[0])) if rows[i][j] == 1}

        self.min_i = self.get_min_i()
        self.max_i = self.get_max_i()
        self.min_j = self.get_min_j()
        self.max_j = self.get_max_j()

        self.rim = False

    def get_value(self, coord, p=0):
        i, j = coord
        if self.rim and (i < self.min_i - p or i > self.max_i + p or j < self.min_j - p or j > self.max_j + p):
            return 1
        else:
            return 1 if coord in self.points else 0

    def get_min_i(self):
        return min(self.points, key=lambda p: p[0])[0]

    def get_max_i(self):
        return max(self.points, key=lambda p: p[0])[0]

    def get_min_j(self):
        return min(self.points, key=lambda p: p[1])[1]

    def get_max_j(self):
        return max(self.points, key=lambda p: p[1])[1]

    def get_grid_value(self, coord, p=0):
        # get binary value for 3x3 grid
        bin_str = ''.join([str(self.get_value((coord[0] + i, coord[1] + j), p))
                          for i in range(-1, 2) for j in range(-1, 2)])
        return int(bin_str, 2)

    def get_algorithm_value(self, number):
        return self.algorithm[number]

    def print(self):
        for i in range(self.min_i, self.max_i + 1):
            row = ""
            for j in range(self.min_j, self.max_j + 1):
                row += "#" if self.get_value((i, j)) == 1 else "."
            print(row)

    def enhance(self):
        enhanced = set()

        counter = 0

        self.min_i -= self.padding
        self.max_i += self.padding
        self.min_j -= self.padding
        self.max_j += self.padding

        for i in range(self.min_i, self.max_i + 1):
            for j in range(self.min_j, self.max_j + 1):
                grid_value = self.get_grid_value((i, j), -self.padding)
                pixel_value = self.get_algorithm_value(grid_value)
                if pixel_value == 1:
                    enhanced.add((i, j))
                # check the edges
                if i == self.min_i or i == self.max_i or j == self.min_j or j == self.max_j:
                    if pixel_value == 1:
                        counter += 1

        height = abs(self.max_i - self.min_i + 1)
        width = abs(self.max_j - self.min_j + 1)

        if counter == 2 * height + 2 * width - 4:
            self.rim = True
            self.padding = 1
        else:
            self.rim = False
        self.points = enhanced


image = Image(algorithm, rows)

for i in range(3):
    image.enhance()
    print("round", i)

image.print()
print(len(image.points))
