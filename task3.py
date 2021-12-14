def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(line)

        return data

if __name__== "__main__":
    import functools

    data = load_data("data3.txt")
    numbers=list(map(lambda s: int(s, base=2), data))
    
    def get_bit(number, position):
        return ((2**position) & number) >> position
    
    nof_numbers = len(numbers)
    
    gamma = 0
    epsilon = 0

    for i in range(12):
        val = functools.reduce(lambda acc, cur: acc + get_bit(cur, i), numbers, 0)
        if val > nof_numbers / 2:
            gamma += 2**i            
        else:            
            epsilon += 2**i

    print("3a answer", gamma*epsilon)

    """
    3b consider only first bit. Keep only numbers with bit criteria

    """   

    def filter_numbers(number_list, number_length, bit_value, verbose=False):
        """bitvalue == most common bit"""
        numbers = number_list.copy()

        def rec(numbers_left, i):
            if len(numbers_left) == 1 or i == -1:
                return numbers_left

            val = functools.reduce(lambda acc, cur: acc + get_bit(cur, i), numbers_left, 0)
            most_common_bit = 0 if bit_value == 1 else 1

            if val >= len(numbers_left) / 2: 
                most_common_bit = 1 if bit_value == 1 else 0

            numbers_left = list(filter(lambda x: get_bit(x, i) == most_common_bit, numbers_left))

            if verbose:
                print("bit: ", i, list(map(lambda x: bin(x), numbers_left)))

            return rec(numbers_left, i-1)
        
        res = rec(numbers, number_length - 1)
        
        return res[0]

    oxygen = filter_numbers(numbers, 12, 1)
    co2 = filter_numbers(numbers, 12, 0)

    print(oxygen)
    print(co2)
    print(oxygen * co2)
    