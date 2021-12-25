"""
Original code from Reddit for playing around
"""
from utils import load_data

def read(state, n):
    return state[ord(n) - ord("w")] if "w" <= n <= "z" else int(n)


def write(state, n, v):
    state[ord(n) - ord("w")] = v


ins = [line.split() for line in load_data('data/data24.txt')]

cache = {}
arrs = []

def solve(arr, step=0, z=0):
    global cache
    for input in [9,8,7,6,5,4,3,2,1]:
        state = [0, 0, 0, 0]
        write(state, "z", z)
        write(state, ins[step][1], input)
        #print(step)
        i = step + 1

        while True:
            if i == len(ins):
                z = read(state, "z")                
                if z == 0:
                    arrs.append(arr)
                    print(arr)
                return str(input) if z == 0 else None
            n = ins[i]
            if n[0] == "inp":
                z = read(state, "z")
                key = (i, z)

                r = cache.get(key) # even if key exists, value maybe none

                if key not in cache:
                    r = solve(arr + [input], i, z)
                    cache[key] = r                    
                
                #if r is not None:
                #    return str(input) + r
                break
            elif n[0] == "add":
                write(state, n[1], read(state, n[1]) + read(state, n[2]))
            elif n[0] == "mul":
                write(state, n[1], read(state, n[1]) * read(state, n[2]))
            elif n[0] == "div":
                write(state, n[1], read(state, n[1]) // read(state, n[2]))
            elif n[0] == "mod":
                write(state, n[1], read(state, n[1]) % read(state, n[2]))
            elif n[0] == "eql":
                write(state, n[1], int(read(state, n[1]) == read(state, n[2])))
            i += 1


res = solve([])
print("####")
print(res)
print(arrs)
