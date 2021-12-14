import numpy as np
N = 5
def load_data(filename):
        data = []
        with open(filename, newline='') as file:            
            lines = file.readlines()
            for line in lines:
                data.append(line.strip())
        return data

class Board:
    def __init__(self, rows):
        self.board = np.array(rows, np.int32)
        self.marks = np.zeros((N, N), dtype = np.int32)
        self.is_done = False

    def is_win(self):        
        col_sum = np.sum(self.marks, axis=0)
        row_sum = np.sum(self.marks, axis=1)

        if np.isin(5, col_sum) or np.isin(N, row_sum):
            return True
        else:
            return False

    def mark(self, number):        
        arr = np.reshape([number] * N**2, (N,N)) # "mask"
        res = np.isin(self.board, arr) # returns True/False in shape of the mask
        self.marks = np.add(1 * res, self.marks)
        

if __name__== "__main__":
    data = load_data("data/data4.txt")
    bingo_numbers = [int(x) for x in data[0].split(",")]

    def read_boards(data):
        rows = []
        boards = []

        def parse_row(row):
            return [int(x) for x in filter(lambda r: r != '', row.split(" "))]

        for row in data[2:]:
            if row == "":
                boards.append(Board(rows))
                rows = []
            else:
                rows.append(parse_row(row))
        boards.append(Board(rows))
        return boards

    bingo_boards = read_boards(data)

    # Lets play bingo
    def first_win(boards, numbers):
        for n in numbers:            
            for b in boards:
                b.mark(n)
                if b.is_win():                   
                    return b, n
        

    def last_win(boards, numbers):
        nof_boards = len(boards)
        print("nof boards", nof_boards)
        wins = 0
        for n in numbers:
            for b in filter(lambda b: not b.is_done, boards):
                b.mark(n)

                if b.is_win():                    
                    b.is_done = True
                    wins += 1

                if wins == nof_boards:
                    return b, n
            
    winner, last_number = last_win(bingo_boards, bingo_numbers)
    
    inverse_ones = 1 - winner.marks 
    unmarked = np.multiply(winner.board, inverse_ones)
    print(np.sum(unmarked)*last_number)

