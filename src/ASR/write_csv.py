# -*- coding: utf-8 -*-
"""
created on 12/23/2022
@author tengchen CTENG9@ford.com

"""

import csv
import sys

print('正在写最终结果...')

inputfile1 = sys.argv[1]
inputfile2 = sys.argv[2]
outputfile = sys.argv[3]

with open(inputfile1,'r',encoding='utf-8') as f:
    L1 = f.readlines()

with open(inputfile2,'r',encoding='utf-8') as f:
    L2 = f.readlines()

f0 = open(outfile,'w',newline='')
writer = csv.writer(f0)

line1 = ['原语料','','','','','','','全小写']
line2 = L1[0].strip().split('\t')+['']+L2[0].strip().split('\t')
writer.writerow(line1)
writer.writerow(line2)

for i,j in zip(L1[1:],L2[1:]):
    line = i.strip().split('\t')+['']+j.strip().split('\t')
    writer.writerow(line)
f0.close()