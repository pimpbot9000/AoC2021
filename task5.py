import numpy as np

def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(line)
        return data
        
N = 1000
data = load_data("data5.txt")
X = []

for d in data:
    x1, x2 = d.split(" -> ")
    x1 = [int(x) for x in x1.split(",")]
    x2 = [int(x) for x in x2.split(",")]
    X.append([x1, x2])

class Segment:
    def __init__(self, x1, x2):
        self.x1 = np.array(x1)
        self.x2 = np.array(x2)
        self.vector = np.add(self.x2,  -1 * self.x1)
        self.max = np.max(np.absolute(self.vector))
        self.unit_vector = np.divide(self.vector, self.max).astype(np.int32)

    def get_points(self):
        return [np.add(segment.x1, i * segment.unit_vector) for i in range(segment.max + 1)]
        
    def is_horizontal(self):
        return self.unit_vector[1] == 0

    def is_vertical(self):
        return self.unit_vector[0] == 0

class Space:
    def __init__(self, N):
        self.space = np.zeros((N,N), dtype=np.int32)

    def add_segment(self, segment, i):
        for x in segment.get_points():
            self.space[x[1], x[0]] +=1
       
    def count(self):
        arr = self.space.flatten()
        return len(list(filter(lambda x: x >= 2, arr)))

# part a
space = Space(N)

for i, x in enumerate(X):    
    segment = Segment(*x)
    if segment.is_vertical() or segment.is_horizontal():    
        space.add_segment(segment, i)

print(space.space)
print(space.count())

# part b
space2 = Space(N)

for i, x in enumerate(X):    
    segment = Segment(*x)  
    space2.add_segment(segment, i)

print(space2.space)
print(space2.count())
# part b




