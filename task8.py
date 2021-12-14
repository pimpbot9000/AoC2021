"""
digit	segS	UNIQUE
0	6	6
1	2	        X
2	5   5
3	5   5
4	4	        X
5	5   5
6	6   6
7	3	        X
8	7	        X
9	6   6

Unique length: 1,4,7,8

Segments of 1 -> set A
sefgments of 4 \ segments of 1 -> set B ({b,d} in unscrambled display}

5 segments (2, 3 or 5) and contains A -> 3
5 segments (2, 3 or 5) and not contains A and contains B -> 5
5 segments (2, 3 or 5) and not contains A and not contains B -> 2

6 segments (0, 6 or 9) and not contains A -> 6
6 segments (0, 6 or 9) and contains A and contains B -> 9
6 segments (0, 6 or 9) and contains A and not contains B -> 0
"""

def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(line.strip())
        return data

def split(word):
    return [c for c in word]

data = load_data("data8.test.txt")
#print(signals)

class Digits:
    def __init__(self, row):
        signals, digits = row.split(" | ")
        signals = signals.split(" ")
        digits = digits.split(" ")
        
        self.digits = list(map(lambda d: set(split(d)), digits))
        self.signals = list(map(lambda s: set(split(s)), signals))

        self.digit_map = {}        
        self.digit_map[1] = self.find(lambda s: len(s) == 2)
        self.digit_map[4] = self.find(lambda s: len(s) == 4)
        self.digit_map[7] = self.find(lambda s: len(s) == 3)
        self.digit_map[8] = self.find(lambda s: len(s) == 7)

        a = self.digit_map[1]
        b = self.digit_map[4] - self.digit_map[1]
        
        self.digit_map[3] = self.find(lambda s: len(s) == 5 and a.issubset(s))
        self.digit_map[5] = self.find(lambda s: len(s) == 5 and not a.issubset(s) and b.issubset(s))
        self.digit_map[2] = self.find(lambda s: len(s) == 5 and not a.issubset(s) and not b.issubset(s))


        self.digit_map[6] = self.find(lambda s: len(s) == 6 and not a.issubset(s))
        self.digit_map[9] = self.find(lambda s: len(s) == 6 and a.issubset(s) and b.issubset(s))
        self.digit_map[0] = self.find(lambda s: len(s) == 6 and a.issubset(s) and not b.issubset(s))
        
        self.inverse_digit_map = {}

        for item in self.digit_map.items():
            self.inverse_digit_map[frozenset(item[1])] = item[0]

    def find(self, f):
        return set(list(filter(f, self.signals))[0])

    def get_digits(self):
        return [self.inverse_digit_map[frozenset(d)] for d in self.digits]

    def get_number(self):
        return int("".join(list(map(lambda d: str(d), self.get_digits()))))



print(sum([Digits(d).get_number() for d in data]))
