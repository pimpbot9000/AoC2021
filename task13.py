import numpy as np
from utils import load_data
import time

data = load_data('data13.txt')

coordinates = []
instructions = []
read_instructions = False

for row in data:
    if row == '':
        read_instructions = True
        continue
    if not read_instructions:
        coordinates.append(tuple([int(x) for x in row.split(',')]))
    else:
        variable, value = row.split(' ')[2].split('=')
        instructions.append((variable, int(value)))


class Grid:
    # Solution with some numpy 2d array magic!
    def __init__(self, coordinates):
        x_max = max(x[0] for x in coordinates) + 1
        y_max = max(x[1] for x in coordinates) + 1
        self.grid = np.zeros((y_max, x_max), dtype=bool)
        for x, y in coordinates:
            self.grid[y, x] = True

    def fold_up(self, y):
        upper = self.grid[:y, ]
        lower = np.flipud(self.grid[y + 1:, ])

        if upper.shape[0] > lower.shape[0]:
            padding = upper.shape[0] - lower.shape[0]
            lower = np.pad(lower, [(padding, 0), (0, 0)])

        if lower.shape != upper.shape:
            raise Exception('fold up mismatch')

        self.grid = np.logical_or(upper, lower)

    def fold_left(self, x):
        left = self.grid[:, :x]
        right = np.fliplr(self.grid[:, x + 1:])

        if left.shape[1] > right.shape[1]:
            padding = right.shape[1] - left.shape[1]
            right = np.pad(right, [(0, 0), (padding, 0)])

        if left.shape != right.shape:
            raise Exception('fold left mismatch')

        self.grid = np.logical_or(left, right)

    def print(self):
        for i in range(self.grid.shape[0]):
            print(''.join('#' if x else ' ' for x in self.grid[i, ]))


class Grid2:
    # Simpler solution with just a set of coordinates
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def fold_up(self, y_fold):
        self.coordinates = {(x, y) if y <= y_fold else (
            x, y_fold - (y - y_fold)) for x, y in self.coordinates}

    def fold_left(self, x_fold):
        self.coordinates = {(x, y) if x <= x_fold else (
            x_fold - (x - x_fold), y) for x, y in self.coordinates}

    def print(self):
        x_max = max(x[0] for x in self.coordinates) + 1
        y_max = max(x[1] for x in self.coordinates) + 1
        grid = np.zeros((y_max, x_max), dtype=bool)
        for x, y in self.coordinates:
            grid[y, x] = True

        for i in range(grid.shape[0]):
            print(''.join('$' if x else ' ' for x in grid[i, ]))


grid = Grid(coordinates)
grid2 = Grid2(coordinates)
print(" ")

start = time.time()
for variable, value in instructions:
    if variable == 'y':
        grid.fold_up(value)
    if variable == 'x':
        grid.fold_left(value)
end = time.time()
print("folding time", end-start)

start = time.time()
for variable, value in instructions:
    if variable == 'y':
        grid2.fold_up(value)
    if variable == 'x':
        grid2.fold_left(value)
end = time.time()
print("folding time", end-start)
grid2.print()

# Answer
#
# $  $   $$ $$$  $  $ $$$$ $  $ $$$   $$ 
# $ $     $ $  $ $ $  $    $  $ $  $ $  $
# $$      $ $$$  $$   $$$  $  $ $$$  $   
# $ $     $ $  $ $ $  $    $  $ $  $ $ $$
# $ $  $  $ $  $ $ $  $    $  $ $  $ $  $
# $  $  $$  $$$  $  $ $$$$  $$  $$$   $$$