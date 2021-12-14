from utils import load_data
from collections import Counter, defaultdict

data = load_data('./data/data14.txt')

template = data[0]
rules = {}
for row in data[2:]:
    a, b = row.split(' -> ')
    rules[a] = b


class Polymer:
    def __init__(self, template, rules): 
        self.pairs = defaultdict(int)
        self.occurrences = defaultdict(int)
        self.rules = rules

        for pair in [template[i:i+2] for i in range(len(template)-1)]:
            self.pairs[pair] += 1

        for letter in template:
            self.occurrences[letter] += 1

    def replace(self):
        pairs = defaultdict(int)

        for pair, occurrence in self.pairs.items():
            inserted = self.rules.get(pair)

            if inserted is not None:
                pairs[pair[0] + inserted] += occurrence                
                pairs[inserted + pair[1]] += occurrence
                self.occurrences[inserted] += occurrence
            else:
                pairs[pair] += occurrence

        self.pairs = pairs

polymer = Polymer(template, rules)

import time
start = time.time()
for i in range(40):
    polymer.replace()
end = time.time()
print("time", end-start, "s")
min_occurence = min(polymer.occurrences.values())
max_occurence = max(polymer.occurrences.values())
print(max_occurence - min_occurence)
