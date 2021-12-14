import timeit

def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(line)
        return data

data = [int(x) for x in load_data("data7.txt")[0].split(",")]

max_val = max(data)

lookup = {}
def fuel(x):
    val = lookup.get(x)
    if not val:
        val = int((x**2+x)/2)
        lookup[x] = val
        return val
    else:
        return val

def fuel2(x):
    return x

start = timeit.timeit()
minimum = min([sum([fuel2(abs(position-x)) for x in data]) for position in range(max_val)])
end = timeit.timeit()
print(minimum)
print(end - start)