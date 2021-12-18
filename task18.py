from utils import load_data
import math


class Number:
    def __init__(self, number):
        self.number = number

    def add(self, other):
        return Number([self.number, other.number])

    def print(self):
        print("Number", self.number)

    def explode(self):

        exploded = False

        def recurse(n, depth):
            nonlocal exploded
            if depth >= 5 and type(n) == list and type(n[0]) == int and type(n[1]) == int and not exploded:
                exploded = True
                return n[0], n[1], 0

            elif type(n) == int:
                return 0, 0, n

            else:
                # cl = "carry left"
                # ct = "carry right"
                cl_left, cr_left, left = recurse(n[0], depth + 1)
                cl_right, cr_right, right = recurse(n[1], depth + 1)

                if cl_left != 0 or cr_left != 0:
                    if type(right) == int:
                        return cl_left, 0, [left, right + cr_left]
                    elif type(right) == list:
                        if cr_left != 0: # don't push zeros
                            right = push_right(right, cr_left)                        
                        return cl_left, 0, [left, right]

                elif cl_right != 0 or cr_right != 0:
                    if type(left) == int:
                        return 0, cr_right, [left + cl_right, right]
                    elif type(left) == list:
                        if cl_right != 0: # don't push zeros
                            left = push_left(left, cl_right)
                        return 0, cr_right, [left, right]
                else:
                    return 0, 0, [left, right]

        def push_right(number, push):  # push to right side leftmost
            if type(number) == int:
                return number + push
            else:
                left = push_right(number[0], push) # push to left
                right = number[1]
                return [left, right]

        def push_left(number, push):  # push to left side rightmost
            if type(number) == int:
                return number + push
            else:                
                right = push_left(number[1], push)
                left = number[0]
                return [left, right]

        _, _, result = recurse(self.number, 1)

        self.number = result

        return exploded

    def is_explodable(self):

        explodable = False

        def recurse(n, depth):
            nonlocal explodable
            if depth >= 5:
                explodable = True
            elif explodable: # already "exploded"
                return n[0], n[1]
            else:
                if not explodable and type(n[0]) == list:
                    recurse(n[0], depth + 1)
                if not explodable and type(n[1]) == list:
                    recurse(n[1], depth + 1)
            
        recurse(self.number, 1)
        return explodable

    def is_splittable(self):

        splittable = False

        def recurse(n):
            nonlocal splittable
            if type(n) == int and n >= 10:
                splittable = True
            else:
                if not splittable and type(n) == list:
                    recurse(n[0])
                if not splittable and type(n) == list:
                    recurse(n[1])

        recurse(self.number)

        return splittable

    def reduce(self):

        while True:
            if self.is_explodable():
                self.explode()
            elif self.is_splittable():
                self.split()
            else:
                break

    def split(self):
        splitted = False

        def recurse(n):
            nonlocal splitted
            if type(n) == int and n >= 10 and not splitted:
                splitted = True
                return [int(math.floor(n / 2)), int(math.ceil(n / 2))]
            elif type(n) == int:
                return n
            else:
                left = recurse(n[0])
                right = recurse(n[1])
                return [left, right]

        self.number = recurse(self.number)

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


data = load_data("data/data18.txt")

numbers = []
for row in data:
    numbers.append(eval(row))


def part1():
    summa = Number(numbers[0])
    for i in range(1, len(numbers)):
        summa = summa.add(Number(numbers[i]))
        summa.reduce()

    print(summa.magnitude())


def part2():
    max_magnitude = 0

    for i in range(0, len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            n1 = Number(numbers[i])
            n2 = Number(numbers[j])

            summa1 = n1.add(n2)
            summa1.reduce()
            magnitude1 = summa1.magnitude()
            max_magnitude = max(max_magnitude, magnitude1)

            summa2 = n2.add(n1)
            summa2.reduce()
            magnitude2 = summa2.magnitude()
            max_magnitude = max(max_magnitude, magnitude2)

    print(max_magnitude)


part1()
part2()
