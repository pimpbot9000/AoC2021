import math

class Number:
    def __init__(self, number):
        self.number = number
        self.exploded = False
        self.splitted = False
        self.explodable = False
        self.splittable = False

    def add(self, other):
        return Number([self.number, other.number])
        
    def print(self):
        print("Numbver", self.number)

    def explode2(self):

        self.exploded = False

        def recurse(n, depth):

            if depth >= 5 and type(n) == list and type(n[0]) == int and type(n[1]) == int and not self.exploded:
                self.exploded = True
                
                return True, n[0], n[1], 0           
                
            elif type(n) == int:
                return False, 0,0, n

            else:
                ex_left, cl_left, cr_left, left = recurse(n[0], depth + 1 )
                ex_right, cl_right, cr_right, right = recurse(n[1], depth + 1 )

                if cl_left != 0 or cr_left != 0:

                    if type(right) == int:
                        return True, cl_left, 0, [left, right + cr_left]
                    elif type(right) == list:
                        suc, res = push_right(right, cr_left)
                        return True, cl_left, 0, [left,res]
                    else:
                        return True, cl_left, cr_right, [left, right]

                elif cl_right != 0 or cr_right != 0:    

                    if type(left) == int:                        
                        return True, 0, cr_right, [left + cl_right, right]
                    elif type(left) == list:
                        success, result = push_left(left, cl_right)
                        return True, 0, cr_right, [result, right]

                else:
                    return False, 0,0, [left, right]

        def push_right(number, push): # push to right side leftmost

            if type(number) == int:
                return True, number + push
            else:
                push1, left = push_right(number[0], push)
                push2, right = push_right(number[1], 0)
                return push1 or push2, [left, right]

        def push_left(number, push): # push to left side rightmost
            if type(number) == int:
                return True, number + push
            else:
                push1, left = push_left(number[0], 0)
                push2, right = push_left(number[1], push)
                return push1 or push2, [left, right]

        a, b, c, d = recurse(self.number,1)
        self.number = d

        return self.exploded
        
    def is_explodable(self):
        
        self.explodable = False

        def recurse(n, depth):
            if depth >= 5:
                self.explodable = True
            else:
                if type(n[0]) == list and not self.explodable:
                    recurse(n[0], depth + 1 )
                if type(n[1]) == list and not self.explodable:
                    recurse(n[1], depth + 1)

        recurse(self.number, 1)
        return self.explodable
    
    def is_splittable(self):
        self.splittable = False
        def recurse(n, depth):
            if type(n) == int and n >= 10:
                self.splittable = True
            else:
                if not self.splittable and type(n) == list:
                    recurse(n[0], depth + 1)
                if not self.splittable and type(n) == list:
                    recurse(n[1], depth +1)

        recurse(self.number, 1)
        return self.splittable
        
    def reduce2(self):

        while True:
            if self.is_explodable():
                self.explode2()
            elif self.is_splittable():
                self.split()
            else:
                break

    def split(self):
        self.splitted = False
        def recurse(n):
            if type(n) == int and n >= 10 and not self.splitted:
                self.splitted = True
                return True, [int(math.floor(n / 2)), int(math.ceil(n / 2))]
            elif type(n) == int:
                return False, n
            else:
                split_left, left = recurse(n[0])
                split_right, right = recurse(n[1])
                return split_left or split_right, [left, right]
        
        splitted, self.number = recurse(self.number)

        return splitted
        
    def magnitude(self):

        def recurse(n):
            if type(n) == int:
                return n
            else:
                left = recurse(n[0])
                right = recurse(n[1])
                return 3 * left + 2 * right
        return recurse(self.number)

from utils import load_data

data = load_data("data/data18.txt")

numbers = []
for row in data:
   numbers.append(eval(row))

def part1():

    summa = Number(numbers[0])
    for i in range(1, len(numbers)):
        summa = summa.add(Number(numbers[i]))
        summa.reduce2()


    print(summa.magnitude())


def part2():
    max_magnitude = 0
    #numbers = [1,2,3,4,5,6]

    for i in range(0, len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            n1 = Number(numbers[i])
            n2 = Number(numbers[j])

            summa1 = n1.add(n2)
            summa1.reduce2()
            magnitude1 = summa1.magnitude()
            max_magnitude = max(max_magnitude, magnitude1)

            summa2 = n2.add(n1)
            summa2.reduce2()
            magnitude2 = summa2.magnitude()
            max_magnitude = max(max_magnitude, magnitude2)

    print(max_magnitude)
part2()