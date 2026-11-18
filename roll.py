import random;
import math;

class Roll:
    def __init__(self, size: int | 0, mod: int | 0):
        self.size = size #base size of the dice
        self.mod = mod #base modifier
        self.inputs = [] #agit additional inputs
        self.base_result = 0 #base roll of the dice
        self.result = [] #result of the last roll

    def roll(self):
        self.result = []
        if not (self.size):
            self.base_result = random.randint(1, self.size) #roll the base dice
        
        for v in self.inputs: #add additional modifiers, roll additional dice if necessary
            if v.isinstance(Roll):
                self.result.append(v.roll)
            else:
                self.result.append(v)

        sum = sum(self.result) + self.base_result + self.mod
        self.base_result = 0
        self.result = []
        return sum



    


