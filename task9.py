import numpy as np
import functools


def load_data(filename):
    data = []
    with open(filename, newline='') as file:
        lines = file.readlines()
        for line in lines:
            data.append(line.strip())
    return data


class OceanFloor:
    def __init__(self, A):
        self.A = np.array(A)

    def get_neighbours(self, i, j):
        return [self.A[_i, _j] for _i, _j in self.get_neighbour_coordinates(i, j)]

    def get_neighbour_coordinates(self, i, j):
        shape = self.A.shape
        n = []
        if j - 1 >= 0:
            n.append((i, j - 1))

        if j + 1 < shape[1]:
            n.append((i, j + 1))

        if i - 1 >= 0:
            n.append((i - 1, j))

        if i + 1 < shape[0]:
            n.append((i + 1, j))

        return n

    def is_lowpoint(self, i, j):
        val = self.A[i, j]
        return all(x > val for x in self.get_neighbours(i, j))

    def sum_of_lowpoints(self):
        shape = self.A.shape
        return sum(self.A[i, j] + 1 for i in range(shape[0]) for j in range(shape[1]) if self.is_lowpoint(i, j))

    def get_lowpoints(self):
        shape = self.A.shape
        return [(i, j) for i in range(shape[0]) for j in range(shape[1]) if self.is_lowpoint(i, j)]

    def find_basin(self, i, j):
        """ Returns the nof cells in a basin using DFS"""
        if not self.is_lowpoint(i, j):
            raise Exception("Given coordinate is not a lowpoint")

        visited = np.zeros(self.A.shape, dtype=bool)

        def find(i, j, visited, A):

            N = 1
            visited[i, j] = True
            
            for _i, _j in self.get_neighbour_coordinates(i, j):
                if A[_i, _j] > A[i, j] and A[_i, _j] != 9 and not visited[_i, _j] :
                    N += find(_i, _j, visited, A)

            return N

        return find(i, j, visited, self.A)

    def get_basins(self):
        return [self.find_basin(*x) for x in self.get_lowpoints()]


if __name__ == "__main__":
    data = load_data("data9.txt")
    m = [[int(x) for x in row] for row in data]
    ocean_floor = OceanFloor(m)

    print("Sum of lowpoints:", ocean_floor.sum_of_lowpoints())
    
    basins = sorted(ocean_floor.get_basins())
    
    print("Product of 3 largest basins:", functools.reduce(lambda acc, cur: acc * cur, sorted(basins[-3:])))
