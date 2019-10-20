# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 10:12:29 2019

@author: Timothy
skillshare course excercise
"""

from numpy import random
random.seed(0)

totals = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
purchases = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
totalPurchases = 0
for _ in range(100000):
    ageDecade = random.choice([20, 30, 40, 50, 60, 70])
    purchaseProbability = random.random()
    #float(ageDecade) / 100.0
    totals[ageDecade] += 1
    if (random.random() < purchaseProbability):
        totalPurchases += 1
        purchases[ageDecade] += 1
        
PF = float(totals[30]) / 100000.0
PE = float(totalPurchases) / 100000.0
PEF = float(purchases[30]) / float(totals[30])

print('P(purchase | 30s): ' + str(PEF))
print("P(30's): " +  str(PF))
print("P(Purchase):" + str(PE))