from fractions import Fraction as F
from itertools import product,combinations
from collections import defaultdict,Counter
from pathlib import Path
import re
q1=defaultdict(F)
for orders in product([0,1],repeat=3):
 n=sum(orders);q1[5*n-4]+=F(3,5)**n*F(2,5)**(3-n)
assert q1=={-4:F(8,125),1:F(36,125),6:F(54,125),11:F(27,125)}
q2=defaultdict(F)
for (x,p),(y,q) in product(zip([0,3,8],[F(1,5),F(1,2),F(3,10)]),zip([0,3,8],[F(2,5),F(2,5),F(1,5)])):q2[x+y]+=p*q
assert q2[11]==F(11,50) and sum(q2.values())==1
for vals,nums,den,low,high,answers in [([0,2,4,7,11,16,23],[4,3,4,3,2,2,2],20,7,16,[F(11,20),F(1,5)]),([0,2,4,6,10,15,25],[4,2,3,3,2,4,2],20,6,15,[F(9,20),F(3,10)]),([0,2,5,9,14,20],[1,2,3,6,3,5],20,9,14,[F(3,10),F(2,5)])]:
 assert sum(nums)==den
 assert [sum(F(n,den) for v,n in zip(vals,nums) if v<low),sum(F(n,den) for v,n in zip(vals,nums) if v>=high)]==answers
print('PASS: all PMF normalizations, independently grouped Q1/Q2 masses, and Q3–Q6 requested probabilities.')
