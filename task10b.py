import functools


def load_data(filename):
    data = []
    with open(filename, newline='') as file:
        lines = file.readlines()
        for line in lines:
            data.append(line.strip())
    return data


rows = load_data("data10.txt")
pairs = {"(": ")", "{": "}", "[": "]", "<": ">"}

scores_a = {")": 3, "]": 57, "}": 1197, ">": 25137}
scores_b = {"(": 1, "[": 2, "{": 3, "<": 4}

total_score_A = 0
total_scores_B = []
for row in rows:

    stack = []
    error = False
    for c in row:
        if c == '(' or c == '{' or c == '[' or c == '<':
            stack.append(c)
        else:
            item = stack.pop()
            if pairs[item] != c:
                total_score_A += scores_a[c]
                error = True
                break
    if error:
        pass  # corrupted

    elif len(stack) > 0:  # incomplete
        total_score_B = 0
        while len(stack) > 0:
            item = stack.pop()
            total_score_B = 5 * total_score_B + scores_b[item]
        total_scores_B.append(total_score_B)

    elif len(stack) == 0:
        pass  # complete

print("result A:", total_score_A)
print("result B:", sorted(total_scores_B)[int((1+len(total_scores_B))/2 - 1)])
