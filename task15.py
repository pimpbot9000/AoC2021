import time
from utils import load_data
import numpy as np
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

    def dijkstra_search(self):
        # A vanilla Dijkstra's algorithm to shortest paths.

        visited = np.zeros(self.A.shape, dtype=bool)
        distance = np.ones(self.A.shape, dtype=int) * INF
        distance[0, 0] = 0
        seen = np.zeros(self.A.shape, dtype=bool)
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
                if not visited[i, j] and not seen[i,j]:
                    new_distance = current_distance + self.A[i, j]                    
                    if new_distance < distance[i, j]:
                       distance[i, j] = new_distance
                       heapq.heappush(pq, (new_distance, (i, j)))
        print(distance)

    def dijkstra_search2(self):
        # Modifier Dijkstra's algorithm to shortest paths.
        # After the distance to a cell has been set from infinite to finite value
        # due to the fact how "nodes" are connected and the order of the iteration,
        # the distance is never relaxed. Using this fact one can implement a simplified
        # version of the Dijkstra's algorithm.

        visited = np.zeros(self.A.shape, dtype=bool)
        distance = np.ones(self.A.shape, dtype=int) * INF
        distance[(0, 0)] = 0
        seen = np.zeros(self.A.shape, dtype=bool)
        pq = [(0, (0, 0))]

        while pq:

            current_distance, coord = heapq.heappop(pq)
            visited[coord] = True

            for coord in self.get_adjacent_coordinates(coord):
                if not visited[coord] and not seen[coord]:
                    new_distance = current_distance + self.A[coord]  
                    distance[coord] = new_distance
                    heapq.heappush(pq, (new_distance, coord))
                    seen[coord] = True

        print(distance)

data = [[int(x) for x in row] for row in load_data('data/data15.txt')]

seafloor = SeaFloor(data, multiplier=5)
start = time.time()
seafloor.dijkstra_search2()
end = time.time()
print("time", end-start, "s")
