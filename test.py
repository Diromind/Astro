import star_gen
import math
from random import random

"""gen = star_gen.Generator()

lst = [8.5, 10, 12, 14, 16, 18, 20, 30, 50, 75, 100]
logps = [-1.070, -1.342, -1.701, -2.022, -2.279, -2.465, -2.598, -2.962, -3.395, -3.791, -4.104]



Rr = 12
var = (Rr ** 2 - 8.5 ** 2) ** 0.5
p = gen.einasto_distibution(var, 'disk') + gen.einasto_distibution(var, 'flat') + gen.einasto_distibution(var, 'corona')

print('R = ', Rr, ', deviation is ', abs(1 - (math.log(p, 10) / -1.701)) * 100, '%')
print('target p is ', 10**-1.701, -1.701)



print(10**1.4*60*0.25817)"""

s = 0
n = 10**8
a, b = 0.1, 0.45
for i in range(n):
    if a < random() < b:
        s += 1

print(s/n)
print(b - a)
