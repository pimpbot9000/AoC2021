import time
from utils import load_data
import numpy as np
from queue import PriorityQueue
import heapq

INF = 10**10


class SeaFloor:
    def __init__(self, A, multiplier=1):
        A = np.array(A)

        if multiplier == 1:
            self.A = A
        else:
            I = A.shape[0]
            J = A.shape[1]
            self.A = np.zeros(
                (A.shape[0] * multiplier, A.shape[1] * multiplier), dtype=int)
            for i in range(multiplier):
                for j in range(multiplier):
                    c = i + j
                    padded = np.pad(
                        A + c, [(I * i, I * (multiplier - 1 - i)), (J * j, J * (multiplier-1-j))])
                    padded = np.where(padded > 9, padded % 9, padded)
                    self.A = np.add(self.A, padded)

    def print(self):
        for row in self.A[:, ]:
            print(''.join([str(x) for x in row]))

    def get_adjacent_coordinates(self, i, j):
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

    def get_neighbour_values(selg, i, j):
        pass

    def dijkstra_search(self):
        visited = np.zeros(self.A.shape, dtype=bool)
        distance = np.ones(self.A.shape, dtype=int) * INF
        distance[0, 0] = 0
        previous = {}
        pq = [(0, (0,0))]

        while pq:

            i_current, j_current = heapq.heappop(pq)[1]
            visited[i_current, j_current] = True

            for i, j in self.get_adjacent_coordinates(i_current, j_current):
                if not visited[i, j]:
                    new_distance = distance[i_current, j_current] + self.A[i, j]
                    if new_distance < distance[i, j]:
                        distance[i, j] = new_distance
                        previous[(i, j)] = (i_current, j_current)
                        heapq.heappush(pq, (new_distance, (i,j)))
                        
        print(distance)


data = [[int(x) for x in row] for row in load_data('data/data15.txt')]

seafloor = SeaFloor(data, multiplier=5)
start = time.time()
seafloor.dijkstra_search()
end = time.time()
print("time", end-start, "s")
