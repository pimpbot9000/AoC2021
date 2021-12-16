import textwrap
from utils import load_data
import numpy as np


class Message:
    def __init__(self, message):
        self.message = message
        self.total_version = 0
        self.operations = {
            0: "+",
            1: "*",
            2: "min",
            3: "max",
            5: ">",
            6: "<",
            7: "=="
        }

    def parse_literal_value(bits, idx):
        last = False
        segments = []
        while not last:
            if bits[idx] == '0':
                last = True
            segments.append(bits[idx + 1: idx + 5])
            idx += 5

        return idx, int(''.join(segments), 2)

    def calculate(self, elements, type_id):
        operation = self.operations[type_id]

        if operation == "min":
            return min(elements)
        elif operation == "max":
            return max(elements)
        elif operation == "*":
            return np.prod(elements)
        elif operation == "==":
            return elements[0] == elements[1]
        elif operation == "+":
            return sum(elements)
        elif operation == "<":
            return elements[0] < elements[1]
        elif operation == ">":
            return elements[0] > elements[1]

    def parse(self, index):

        version = int(self.message[index: index + 3], 2)
        self.total_version += version
        type_ID = int(self.message[index + 3: index + 6], 2)
        idx = index + 6

        if type_ID == 4:
            # literal packet
            return Message.parse_literal_value(self.message, idx)

        else:
            # operator packet
            length_type_ID = int(self.message[idx], 2)
            idx += 1
            elements = []

            if length_type_ID == 1:
                nof_subpackets = int(self.message[idx: idx + 11], 2)
                idx += 11
                for _ in range(nof_subpackets):
                    idx, val = self.parse(idx)
                    elements.append(val)

            elif length_type_ID == 0:
                length = int(self.message[idx: idx + 15], 2)
                idx = idx + 15
                current_idx = idx
                while idx < current_idx + length:
                    idx, val = self.parse(idx)
                    elements.append(val)

            return idx, self.calculate(elements, type_ID)


data_in_hex = load_data("data/data16.txt")[0]


def int_to_bin(number):
    # integer to 4 bit binary string
    bin_str = format(number, 'b')
    bin_str = (4 - len(bin_str)) * "0" + bin_str
    return bin_str


data_in_bin = ''.join([int_to_bin(int(hex, 16))
                      for hex in textwrap.wrap(data_in_hex, 1)])

m = Message(data_in_bin)
print(m.parse(0))
