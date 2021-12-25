from utils import load_data


class Program:
    def __init__(self, data, inputs):
        self.data = data
        self.inputs = inputs
        self.variables = {
            'x': 0,
            'y': 0,
            'z': 0,
            'y': 0
        }
        self.current_input = 0

    def variable(self, var):
        res = 0
        try:
            res = int(var)
        except:
            res = self.variables[var]
        return res


    def run(self):
        for instruction in data:
            i = instruction.split(" ")
            
            if i[0] == "inp":
                self.variables[i[1]] = inputs[self.current_input]
                self.current_input += 1
            if i[0] == "mul":
                self.variables[i[1]] *= self.variable(i[2])
            if i[0] == "add":
                self.variables[i[1]] += self.variable(i[2])
            if i[0] == "mod":
                self.variables[i[1]] = self.variables[i[1]] % self.variable(i[2])
            if i[0] == "div":
                 self.variables[i[1]] = self.variables[i[1]] // self.variable(i[2])
            if i[0] == "eql":
                res = 1 if self.variables[i[1]] == self.variable(i[2]) else 0
                self.variables[i[1]] = res
        
        print(self.variables['z'], self.inputs)
        

inputs = [int(x) for x in '11911316711811']
data = load_data('data/data24.txt')

p = Program(data, inputs)

p.run()
