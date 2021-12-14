def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(line)
        return data

numbers = [int(x) for x in load_data("data6.test.txt")[0].split(",")]

class Fish:
    def __init__(self, numbers):
        self.fish = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for n in numbers:
            self.fish[n + 1] += 1

    def increment_day(self):
        arr = self.fish[1:]
        nof_new_fish = arr[0]
        arr.append(nof_new_fish)
        arr[7] += nof_new_fish
        self.fish = arr
        self.fish[0] = 0

fishes = Fish(numbers)

for i in range(256):
    print("generation", i)
    numbers = list(map(lambda x: x-1, numbers))
    spawned = 0

    for i, n in enumerate(numbers):
        if n == -1:
            numbers[i] = 6
            spawned += 1
    
    numbers.extend([8]*spawned)
    print(len(numbers))
    
print(numbers)

