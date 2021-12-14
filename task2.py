def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(line)

        return data

if __name__== "__main__":
    data = load_data("data/data2.txt")
    import functools
    # task 1

    def nof_consecutive_inc(arr):
        return functools.reduce(lambda acc, cur: (cur, acc[1] + 1) if cur > acc[0] else (cur, acc[1]), arr, (arr[0],0))

    def elementwise_sum(list1, list2):
        return [sum(x) for x in zip(list1, list2)]

    def parse_command(cmd):
        direction, val = cmd.split(" ")
        val = int(val)
        if direction == "down":
            return [0, val]
        elif direction == "up":
            return [0, -val]
        elif direction == "forward":
            return [val, 0]
        else:
            raise Exception("Unknown direction")
    
    commands = map(lambda command: parse_command(command), data)

    position = functools.reduce(lambda acc, cur: elementwise_sum(acc, cur), commands, [0,0])
    print(position[0]*position[1])