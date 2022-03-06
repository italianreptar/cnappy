# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 11:59:15 2020

@author: Connor
"""

import random
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl

mpl.style.use("seaborn")

def pca():
    plt.close("all")

class Dice():
    def __init__(self, sides, count=1):
        self.sides = sides
        self.count = count
    def __repr__(self):
        return f"<object Dice: sides = {self.sides}; count = {self.count}>"
    
    def __str__(self):
        return f"{self.count}d{self.sides}"
        
    def roll(self):
        return random.randint(1, self.sides)
        
    def roll_sum(self):
        output = 0
        for die in range(self.count):
            output += self.roll()
        return output
    
    def roll_max(self, modifier):
        output = 0
        for die in range(self.count):
            this_roll = self.roll()+modifier
            if output < this_roll:
                output = this_roll
        return output
    
    def roll_min(self, modifier):
        output = self.sides+modifier
        for die in range(self.count):
            this_roll = self.roll()+modifier
            if output > this_roll:
                output = this_roll
        return output
    
    def roll_drop_min(self):
        output = np.array([self.roll() for die in range(self.count)])
        output.sort()
        return np.sum(output[1:])
        

def gen_sum_hist(sides, count, num_rolls=100000):
    die = Dice(sides,count)
    roll_set = np.array([die.roll_sum() for i in range(num_rolls)])
    vals, bins, patches = plt.hist(roll_set, bins=np.arange(count, count*sides+2), density=True, alpha=0.8)
    plt.title(f"Plot of Sum(rolls) for {die}")
    return vals, bins

def gen_drop_min_hist(sides, count, num_rolls=100000):
    die = Dice(sides,count)
    roll_set = np.array([die.roll_drop_min() for i in range(num_rolls)])
    vals, bins, patches = plt.hist(roll_set, bins=np.arange(count-1, (count-1)*sides+2), density=True, alpha=0.8)
    plt.title(f"Plot of dropping the lowest of {die}")
    return vals, bins

def gen_max_hist(sides, count, num_rolls=100000, modifier=0):
    """
    Generates a hist of the max of all rolls.
    """
    die = Dice(sides, count)
    roll_set = np.array([die.roll_max(modifier) for i in range(num_rolls)])
    vals, bins, patches = plt.hist(roll_set, bins=np.arange(1+modifier, sides+modifier+2), density=True, alpha=0.8)
    plt.title(f"Plot of Max(rolls) for {die}+{modifier}")
    
    return vals, bins

def gen_min_hist(sides, count, num_rolls=100000, modifier=0):
    """
    Generates a hist of the max of all rolls.
    """
    die = Dice(sides, count)
    roll_set = np.array([die.roll_min(modifier) for i in range(num_rolls)])
    vals, bins, patches = plt.hist(roll_set, bins=np.arange(1+modifier, sides+modifier+2), density=True, alpha=0.8)
    plt.title(f"Plot of Min(rolls) for {die}+{modifier}")
    
    return vals, bins

def odds_of(min_val, max_val, vals, bins):
    if min_val > max_val:
        temp = min_val
        min_val = max_val
        max_val = temp
        
    bins = bins[:-1]
    mask = (bins >= min_val) & (bins <= max_val)
    return sum(vals[mask])
    
pca()
# makes a hist with 2d8, 3d8, and 4d8 odds on it.
fig1 = plt.figure()
sides = 6

for sides, count in ((8,4), (12,3)):
# for count in range(4, 1, -1):
    sum_vals, sum_bins = gen_sum_hist(sides, count)

# # makes a hist of rolling 2d20+3 with advantage
# fig2 = plt.figure()
# max_vals, max_bins = gen_max_hist(20, 2, modifier=3)

# # makes a hist of rolling 2d20+3 with disadvantage
# fig3 = plt.figure()
# min_vals, min_bins = gen_min_hist(20, 2, modifier=3)


# four = odds_of(4,4, max_vals, max_bins)
# print(f"Odds of hitting a nat 1 with advantage is about: {four*100}%")

# ac_18 = odds_of(18, 30, max_vals, max_bins)
# print(f"Odds of hitting someone with an AC:18 with advantage, with +3 modifier: {ac_18*100}%")

# ac_18 = odds_of(18, 30, min_vals, min_bins)
# print(f"Odds of hitting someone with an AC:18 with disadvantage, with +3 modifier: {ac_18*100}%")