import textwrap
from utils import load_data
import numpy as np


class Message:
    def parse_literal_packet(message, idx, version=0):
        last = False
        segments = []
        while not last:
            if message[idx] == '0':
                last = True
            segments.append(message[idx + 1: idx + 5])
            idx += 5

        return idx, LiteralPacket(int(''.join(segments), 2), version=version)

    def parse_operator_packet(message, idx, type_id, version=0):
        length_type_ID = int(message[idx], 2)
        idx += 1
        sub_packets = []

        if length_type_ID == 1:
            nof_subpackets = int(message[idx: idx + 11], 2)
            idx += 11
            for _ in range(nof_subpackets):
                idx, val = Message.parse(message, idx)
                sub_packets.append(val)

        elif length_type_ID == 0:
            length = int(message[idx: idx + 15], 2)
            idx = idx + 15
            current_idx = idx
            while idx < current_idx + length:
                idx, val = Message.parse(message, idx)
                sub_packets.append(val)

        return idx, OperatorPacket(type_id, sub_packets, version=version)

    def parse(message, index):

        version = int(message[index: index + 3], 2)
        type_ID = int(message[index + 3: index + 6], 2)
        idx = index + 6

        if type_ID == 4:
            return Message.parse_literal_packet(message, idx, version=version)         
        else:
            return Message.parse_operator_packet(message, idx, type_ID, version=version)


class OperatorPacket:
    def __init__(self, type_id, packets, version=0):
        self.type_id = type_id
        self.sub_packets = packets
        self.version = version

        self.operations = {
            0: "+",
            1: "*",
            2: "min",
            3: "max",
            5: ">",
            6: "<",
            7: "=="
        }

    def evaluate(self):
        # recursive evaluation of the packet
        operation = self.operations[self.type_id]
        values = [e.evaluate() for e in self.sub_packets]

        if operation == "min":
            return min(values)
        elif operation == "max":
            return max(values)
        elif operation == "*":
            return np.prod(values)
        elif operation == "==":
            return values[0] == values[1]
        elif operation == "+":
            return sum(values)
        elif operation == "<":
            return values[0] < values[1]
        elif operation == ">":
            return values[0] > values[1]


class LiteralPacket:
    def __init__(self, value, version=0):
        self.value = value
        self.version = version

    def evaluate(self):
        return self.value


data_in_hex = load_data("data/data16.txt")[0]


def int_to_bin(number):
    # integer to 4 bit binary string
    bin_str = format(number, 'b')
    bin_str = (4 - len(bin_str)) * "0" + bin_str
    return bin_str


data_in_bin = ''.join([int_to_bin(int(hex, 16)) for hex in data_in_hex])

idx, packet = Message.parse(data_in_bin, 0)


def version_sum(packet):
    if type(packet) == LiteralPacket:
        return packet.version
    else:
        return sum([version_sum(p) for p in packet.sub_packets]) + packet.version


evaluation = packet.evaluate()
s = version_sum(packet)
print("version sum", s)
print("evaluation", evaluation)
