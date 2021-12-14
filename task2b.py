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
        if direction == "down": #adds to aim
            return {"forward": 0, "aim": val}
        elif direction == "up":
            return {"forward": 0, "aim": -val}
        elif direction == "forward":
            return {"forward": val, "aim": 0}
        else:
            raise Exception("Unknown direction")
    
    commands = map(lambda command: parse_command(command), data)

    def calculate_new_position(position, command):       
        horizontal = position[0] + command["forward"]
        aim = position[2] + command["aim"]
        depth = position[1] + aim * command["forward"] 
        return (horizontal, depth, aim)
        

    #position = functools.reduce(lambda acc, cur: elementwise_sum(acc, cur), commands, [0,0])
    #(horizontal, depth, angle)
    position = functools.reduce(calculate_new_position, commands, (0, 0, 0))

    print(position[0]*position[1])