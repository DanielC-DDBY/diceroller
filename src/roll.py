import random;
import math;


class Dice:
    def __init__(self, size: int, sign: int = 1, group_size: int = 1):
        self.size = size #size of the dice
        self.sign = sign #whether the dice is positive or a negative modifier to a roll
        self.group_size = group_size #the size of the group that the dice is in. E.g 5d8, group_size = 5

    def roll(self):
        return random.randint(1, self.size)

class Roll:
    def __init__(self, inputs=[]):
        self.inputs = inputs #inputs, e.g dice and flat modifiers
        self.result = [] #result of the last roll
        self.sum = 0 #sum of the last roll
        self.out = "" #string to return to console

    def roll(self):
        self.result = []
        
        for v in self.inputs: #add additional modifiers, roll additional dice if necessary
            if v.isinstance(Dice):
                self.result.append(v.roll)
            else:
                self.result.append(v)

        self.result = []
        self.sum = sum(self.result)
        return self.sum

    def form_output(self):
        out = ""
        index = 0
        while index < len(self.inputs):

            term = self.inputs[index]

            #input is dice = add string to out that looks like: + 3d6 (1, 5, 4)
            if isinstance(term, Dice): 
                if not out:
                    sign = "" 
                else:
                    sign = "-" if term.sign == -1 else "+"

                out += f" {sign} {term.group_size}d{term.size} ("
                for temp in range(term.group_size):
                    out += f"{self.result[index + temp]}"
                    if temp < term.group_size - 1:
                        out += ", "
                out += ")"

                index += term.group_size

            #else: add modifier
            else:
                out += f" {'-' if term < 0 else '+'} {abs(term)}"
                index += 1
        out += f" = {self.sum}"

        self.out = out.strip()

            

                







    


