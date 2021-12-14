import time
from collections import defaultdict
from utils import load_data


edges = defaultdict(list)

for row in load_data("data/data12.txt"):
    start, end = row.split("-")
    if end != 'start':
        edges[start].append(end)
    if start != 'start':
        edges[end].append(start)


def search(allow_visit_twice=False):

    def visit(v, route, visited, visited_twice):
        visits = 0
        
        if v == 'end':
            return 1

        if visited.get(v, False) and v.islower():
            visited_twice = True

        visited[v] = True

        for next_vertice in edges.get(v):
            is_upper = next_vertice.isupper()
            if (not is_upper and not visited.get(next_vertice, False)) \
                    or is_upper \
                    or not visited_twice:

                visits += visit(next_vertice, route + [next_vertice],
                                visited.copy(), visited_twice)
        return visits

    return visit('start', [], {}, visited_twice=not allow_visit_twice)


start = time.time()
for i in range(10):
    routes = search(allow_visit_twice=False)
    routes = search(allow_visit_twice=True)
end = time.time()
print((end - start)/10)
print(routes)
