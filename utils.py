def load_data(filename):
    with open(filename) as f:
        lines = f.readlines()
        data = [line.strip() for line in lines]
        return data
