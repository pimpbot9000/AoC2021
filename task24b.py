"""
    Original code from Reddit for playing around and testing stuff
"""
import functools
from utils import load_data

def read(state, n):
    return state[ord(n) - ord("w")] if "w" <= n <= "z" else int(n)


def write(state, n, v):
    state[ord(n) - ord("w")] = v


ins = [line.split() for line in load_data('data/data24.txt')]


@functools.lru_cache(maxsize=None)
def solve(step=0, z=0):
    for input in (9,8,7,6,5,4,3,2,1):
        state = [0, 0, 0, 0]
        write(state, "z", z)
        write(state, ins[step][1], input)
        
        i = step + 1

        while True:
            if i == len(ins):
                z = read(state, "z")
                if z == "0":
                    print("solution")
                return str(input) if read(state, "z") == 0 else None
            n = ins[i]
            if n[0] == "inp":
                r = solve(i, read(state, "z"))
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


res = solve()
print("####")
print(res)
# 
1191131671181,