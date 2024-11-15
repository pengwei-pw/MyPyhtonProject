# -*- coding: utf-8 -*-
"""
created on 12/23/2022
@author tengchen CTENG9@ford.com

"""
import re
import sys

def sentence2word(s):
###把句子按字分开，中文按字分，英文按单词分，数字按空格分
    regEx = re.compile(r'[\s]+')  ##\s匹配任意空白字符
    res = re.compile(r'([\u4e00-\u9fa5])')  ##[\u4e00-\u9fa5]中文范围
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
    curr = [0] + [i for i in range(1, len(v) + 1)]
    # Operations: (SUB, DEL, INS)
    prev_ops = None
    curr_ops = [(0, 0, i) for i in range(len(v) + 1)]
    for x in range(1, len(u) + 1):
        prev, curr = curr, [x] + ([None] * len(v))
        prev_ops, curr_ops = curr_ops, [(0, x, 0)] + ([None] * len(v))
        for y in range(1, len(u) + 1):
            delcost = prev[y] + 1
            addcost = curr[y - 1] + 1
            subcost = prev[y - 1] + int(u[x - 1] != v[y - 1])
            curr[y] = min(subcost, delcost, addcost)
            if curr[y] == subcost:
                (n_s, n_d, n_i) = prev_ops[y - 1]
                curr_ops[y] = (n_s + int(u[x - 1] != v[y - 1]), n_d, n_i)
            elif curr[y] == delcost:
                (n_s, n_d, n_i) = prev_ops[y]
                curr_ops[y] = (n_s, n_d + 1, n_i)
            else:
                (n_s, n_d, n_i) = curr_ops[y - 1]
                curr_ops[y] = (n_s, n_d, n_i + 1)

    return curr_ops[len(v)]


if __name__ == '__main__':
    print('正在统计每一条语料的数据...')


    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    f0 = open(outputfile,'w',encoding='utf-8')
    f0.write('音频名称\t错字数\t少字数\t多字数\t总字数\t是否为err\t关键词正确数\t关键词总数\t错误关键词\t句子对错\t关键词对错\n')
    with open(inputfile,'r',encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines[1:]:
        err_num = 0
        temp = line.split('\t')
        audioname = temp[0]
        mark = temp[1]
        asr = temp[2]
        if asr == 'err':
            err_num = 1
        keyword = temp[3]
        mark_list = sentence2word(mark)
        asr_list = sentence2word(asr)
        (s,d,i) = levenshtein(mark_list,asr_list)
        n = len(mark_list)
        key_right_num = 0
        key_false_list = []
        if keyword == 'none':
            key_list = []
            false_keyword = 'none'
        else:
            key_list = keyword.split('|')
        
            for key in key_list:
                if key in asr and key+key[-1] not in asr:
                    key_right_num += 1
                else:
                    key_false_list.append(key)
            if not key_false_list:
                false_keyword = 'none'
            else:
                false_keyword = '|'.join(key_false_list)
        key_all_num = len(key_list)
        if key_all_num == 0:
            key_flag = 'None'
        elif key_all_num == key_right_num:
            key_flag = 'True'
        else:
            key_flag = 'False'
        sen_flag = 'True' if s+d+i==0 else 'False'
        f0.write(audioname+'\t'+str(s)+'\t'+str(d)+'\t'+str(i)+'\t'+str(n)+'\t'+str(err_num)+ \
                 '\t'+str(key_right_num)+'\t'+str(key_all_num)+'\t'+false_keyword+'\t'+sen_flag+'\t'+key_flag+'\n')
    f0.close()