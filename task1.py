def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(int(line))

        return data

if __name__== "__main__":
    dat = load_data("data/data1.txt")
    import functools
    # task 1
    def nof_consecutive_inc(data):
        return functools.reduce(lambda acc, cur: (cur, acc[1] + 1) if cur > acc[0] else (cur, acc[1]), data, (data[0],0))
    # task 2
    sums = []
    for i in range(len(dat)-2):
        sums.append(dat[i] + dat[i+1] + dat[i+2])
    
    print(nof_consecutive_inc(dat)[0])








    
