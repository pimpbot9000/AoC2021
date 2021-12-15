import time
from utils import load_data
import numpy as np
import heapq

INF = 10**10


class SeaFloor:
    def __init__(self, A, multiplier=1):
        A = np.array(A)
        self.multiplier = multiplier
        self.original = A

        if multiplier == 1:
            self.A = A            
        else:
            # build a large grid (for speed comparison)
            I = A.shape[0]
            J = A.shape[1]

            padded_list = []
            for i in range(multiplier):
                for j in range(multiplier):
                    c = i + j
                    padded = np.pad(A + c, [(I * i, I * (multiplier - 1 - i)), (J * j, J * (multiplier-1-j))])
                    padded = np.where(padded > 9, padded % 9, padded)
                    padded_list.append(padded)

            self.A = sum(padded_list)

    def get_value(self, coord, use_virtual = True):
        # getting the value from a virtual grid or from a
        # created large grid (for speed comparison)

        if not use_virtual:
            return self.A[coord]       

        if self.multiplier == 1:
            return self.original[coord]
        else:
            i, j = coord
            I, J = self.original.shape
            c = i // I + j // J
            value = self.original[i % I, j % J] + c
            return value if value <= 9 else value % 9

    def get_shape(self):
        return self.multiplier * self.original.shape[0], self.multiplier * self.original.shape[1]

    def print(self):
        for row in self.A[:, ]:
            print(''.join([str(x) for x in row]))
    def print_virtual(self):
        for i in range(self.get_shape()[0]):
            print(''.join([str(self.get_value((i,j))) for j in range(self.get_shape()[1])]))

    def get_adjacent_coordinates(self, coord):
        shape = self.A.shape
        i, j = coord
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

    def dijkstra_search(self, use_virtual=True):
        # A vanilla Dijkstras algorithm for shortest paths.
        # There exists redundancy considering the problem 
        # (See method dijkstra_search2)
        #
        # Does not keep track of the shortest paths.

        visited = np.zeros(self.get_shape(), dtype=bool)
        distance = np.ones(self.get_shape(), dtype=int) * INF
        distance[0, 0] = 0
        pq = [(0, (0, 0))]

        def get_next():
            is_visited = True
            current_distance, (i_current, j_current) = 0, (0, 0)
            while is_visited:
                current_distance, (i_current, j_current) = heapq.heappop(pq)
                is_visited = visited[i_current, j_current]

            return current_distance, (i_current, j_current)

        while pq:

            current_distance, (i_current, j_current) = get_next()
            visited[i_current, j_current] = True

            for i, j in self.get_adjacent_coordinates((i_current, j_current)):
                if not visited[i, j]:
                    new_distance = current_distance + self.get_value((i, j), use_virtual=use_virtual)                    
                    if new_distance < distance[i, j]:
                       distance[i, j] = new_distance
                       heapq.heappush(pq, (new_distance, (i, j)))

        print(distance)
    
    def dijkstra_search2(self, use_virtual=True):
        # Simplified Dijkstras algorithm for shortest paths.
        # After the distance to a cell has been set from infinite to finite value
        # due to the fact how "nodes" are connected and the order of the iteration,
        # the distance is never relaxed twice. Using this fact one can implement 
        # a simplified version of the Dijkstra's algorithm where relaxation is done 
        # only once for each node.
        #
        # Does not keep track of the shortest paths.

        visited = np.zeros(self.get_shape(), dtype=bool)
        distance = -1 * np.ones(self.get_shape(), dtype=int) 
        distance[(0, 0)] = 0
        relaxed = np.zeros(self.get_shape(), dtype=bool)
        pq = [(0, (0, 0))]

        while pq:

            current_distance, coord = heapq.heappop(pq)
            visited[coord] = True

            for coord in self.get_adjacent_coordinates(coord):
                if not relaxed[coord] and not visited[coord]:
                    new_distance = current_distance + self.get_value(coord, use_virtual=use_virtual)
                    distance[coord] = new_distance
                    heapq.heappush(pq, (new_distance, coord))
                    relaxed[coord] = True

        print(distance)

data = [[int(x) for x in row] for row in load_data('data/data15.txt')]

seafloor = SeaFloor(data, multiplier=5)
print("grid build finished")
start = time.time()
seafloor.dijkstra_search(use_virtual=False)
end = time.time()
print("time", end-start, "s")
