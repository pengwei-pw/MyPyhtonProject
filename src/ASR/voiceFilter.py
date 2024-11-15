# -*- coding: utf-8 -*-
"""
created on 1/9/2023
@author tengchen CTENG9@ford.com

"""

import re
import sys

def sentence2word(s):
#####把句子按字分开，中文按字分，英文按单词，数字按空格
    regEx = re.compile(r'[\s]+')##\s匹配任意空白字符
    res = re.compile(r'([\u4e00-\u9fa5])')###[\u4e00-\u9fa5]中文范围
    pl = regEx.split(s)
    str_list = []
    for str in pl:
        if res.split(str) == None:
            str_list.append(str)
        else:
            ret = res.split(str)
            for ch in ret:
                str_list.append(ch)
    list_word = [w for w in str_list if len(w.strip()) > 0]  ##去掉为空的字符
    return list_word
    
    
def levenshtein(u, v):
    prev = None
    curr = [0] + [i for i in range(len(v) + 1)]
    ##Operations:[SUB, DEL, INS]
    prev_ops = None
    curr_ops = [(0, 0 ,i) for i in range(len(v) + 1)]
    for x in range(1, len(v)+1):
        prev, curr = curr, [x] + ([None] * len(v))
        prev_ops, curr_ops = curr_ops, [(0, x, 0)] + ([None] * len(v))
        for y in range(1, len(v) + 1):
            delcost = prev[y] + 1
            addcost = curr[y - 1] + 1
            subcost = prev[y - 1] + int(u[x - 1] != v[y - 1])
            curr[y] = min(subcost, delcost, addcost)
            if curr[y] == subcost:
                (n_s, n_d, n_i) = prev_ops[y - 1]
                curr_ops[y] = (n_s + u[x - 1] != v[y - 1], n_d, n_i)
            elif curr[y] == delcost:
                (n_s, n_d, n_i) = prev_ops[y]
                curr_ops[y] = (n_s, n_d + 1, n_i)
            else:
                (n_s, n_d, n_i) = curr_ops[y - 1]
                curr_ops[y] = (n_s, n_d, n_i + 1)
                
    return curr_ops[len(v)]

if __name__ == "__main__":
    print('正在统计每一条语料的数据...')
    
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    f0 = open(outputfile,'w+',encoding='utf-8')
    f0.write('音频名称\t错字数\t少字数\t多字数\t总字数\t字准率\n')
    with open(inputfile,'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            temp = line.split('\t')
            audioname = temp[0]
            mark = temp[1]
            asr = temp[2]
            mark_list = sentence2word(mark)
            asr_list = sentence2word(asr)
            curr_ops = levenshtein(mark_list,asr_list)
            n = len(mark_list)
            k = 1-((curr_ops[0] + curr_ops[1] + curr_ops[2])/n)
            f0.write(audioname+'\t'+str(str((curr_ops[0]))+'\t'+str(curr_ops[1])+'\t'+str(curr_ops[2])+'\t'+str(n)+'\t'+str(k)+'\n'))
        f0.close()