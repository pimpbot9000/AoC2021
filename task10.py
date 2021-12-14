import functools


def load_data(filename):
    data = []
    with open(filename, newline='') as file:
        lines = file.readlines()
        for line in lines:
            data.append(line.strip())
    return data


strings = load_data("data10.txt")

scores_a = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

corruptions = ["(}", "(]", "(>",
               "{)", "{]", "{>",
               "[)", "[}", "[>",
               "<)", "<}", "<]"]

incomplete = []

total_score_a = 0

for string in strings:

    original = string
    while len(string) > 0:
        before = string
        after = string.replace("()", "").replace(
            "[]", "").replace("<>", "").replace("{}", "")
        if len(before) == len(after):
            break
        string = after

    if len(string) > 0:
        corrupted = False

        for c in corruptions:
            if string.find(c) != -1:
                total_score_a += scores_a[c[1:2]]
                corrupted = True
                break
        if not corrupted:
            incomplete.append((string))

print(total_score_a)

scores_b = {"(": 1, "[": 2, "{": 3, "<": 4}

scores_b = sorted([functools.reduce(lambda acc, cur: 5 * acc + cur,
                                    [scores_b[c] for c in stripped[::-1]], 0) for stripped in incomplete])

print(scores_b[int((1+len(scores_b))/2 - 1)])
