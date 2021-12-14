import numpy as np
from collections import deque
import os
import time
from utils import load_data


def clear():
    os.system('clear')


class SeaFloor:
    def __init__(self, A):
        self.grid = np.array(A)
        self.synchronized = []
        self.time = 0

    def get_neighbour_coordinates(self, i, j):
        shape = self.grid.shape
        coordinates = [(i + _i, j + _j) for _i in range(-1, 2)
                       for _j in range(-1, 2) if not (_i == 0 and _j == 0)]
        return list(filter(lambda x: x[0] >= 0 and x[0] < shape[0] and x[1] >= 0 and x[1] < shape[1], coordinates))

    def get_neighbour_values(selg, i, j):
        pass

    def flash_dfs(self):
        self.time += 1
        shape = self.grid.shape
        flashed = np.zeros(shape, dtype=bool)

        def flash(i, j):
            if flashed[i, j]:
                return

            self.grid[i, j] += 1

            if self.grid[i, j] > 9:
                self.grid[i, j] = 0
                flashed[i, j] = True

                for i, j in self.get_neighbour_coordinates(i, j):
                    flash(i, j)

        for i in range(shape[0]):
            for j in range(shape[1]):
                flash(i, j)

        if np.sum(self.grid) == 0:
            self.synchronized.append(self.time)

    def flash_bfs(self):
        self.time += 1
        shape = self.grid.shape
        flashed = np.zeros(shape, dtype=bool)

        def flash(i_start, j_start):
            q = deque()
            q.append((i_start, j_start))

            while len(q) > 0:
                i, j = q.pop()

                if flashed[i, j]:
                    continue

                self.grid[i, j] += 1

                if self.grid[i, j] > 9:
                    self.grid[i, j] = 0
                    flashed[i, j] = True
                    for _i, _j in self.get_neighbour_coordinates(i, j):
                        q.appendleft((_i, _j))

        for i in range(shape[0]):
            for j in range(shape[1]):
                flash(i, j)

        if np.sum(self.grid) == 0:
            self.synchronized.append(self.time)


data = [[int(x) for x in line] for line in load_data("./data/data11.txt")]


sea_floor = SeaFloor(data)

for i in range(1000):
    sea_floor.flash_bfs()
    clear()
    print(sea_floor.grid)
    time.sleep(0.5)
print(sea_floor.synchronized)
