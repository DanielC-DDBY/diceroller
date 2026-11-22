import random;
import math;


class Dice:
    def __init__(self, size: int):
        self.size = size #size of the dice

    def roll(self):
        return random.randint(1, self.size)

class Roll:
    def __init__(self, size: int | 0, mod: int | 0):
        self.inputs = [] #inputs, e.g dice and flat modifiers
        self.result = [] #result of the last roll

    def roll(self):
        self.result = []
        
        for v in self.inputs: #add additional modifiers, roll additional dice if necessary
            if v.isinstance(Dice):
                self.result.append(v.roll)
            else:
                self.result.append(v)

        sum = sum(self.result) + self.base_result + self.mod
        self.base_result = 0
        self.result = []
        return sum



    


