# -*- coding: utf-8 -*-
"""
created on 12/22/2022
@author tengchen CTENG9@ford.com

"""


import re
import sys

def regular(s):
    punc_Chi = re.compile('？ |。 |; |， |: |、|！ |(|) |\* |\@ |# |“ |” |《 |》 |- |· |/')
    punc_Eng = re.compile('\? |\! |,')
    if not s.strip() or s.strip() in ['， ','！ ','？ ','。 ','、 ','； '] or 'errorMsg' in s:
        new_s = 'err'
    else:
        new_s = punc_Chi.sub("",s.strip())
        new_s = punc_Eng.sub("",new_s.strip())
        if new_s[-1] == '.':
            new_s = new_s[:-1]
    return new_s

def deal_keyword(mark,slots):
    pattern = re.compile(':(.*?)\|')
    results = re.findall(pattern,slots+'|')
    keyword_list = []
    if not results:
        return 'none'
    
    for result in results:
        result = regular(result)
        if result and result not in keyword_list and result in mark:
            keyword_list.append(result.strip())
    keyword_list = list(set(keyword_list))
    keywords = '|'.join(keyword_list)
    if not keywords:
        return 'none'
    return keywords

if __name__ == '__main__':
    print('正在对数据进行初始化处理...')
    inputfile = sys.argv[1]
    outputfile1 = sys.argv[2]
    outputfile2 = sys.argv[3]

    with open(inputfile,'r',encoding='utf-8') as f:
        lines = f.readlines()

    f1 = open(outputfile1,'w',encoding='utf-8')
    f2 = open(outputfile2,'w',encoding='utf-8')
    f1.write(lines[0])
    f2.write(lines[0])

    for line in lines[1:]:
        temp = line.split('\t')
        raw_mark = temp[1]
        raw_asr = temp[2]
        raw_slots = temp[3].replace(': ',':')
        deal_mark = regular(raw_mark)
        deal_asr = regular(raw_asr)
        deal_keywords = deal_keyword(raw_mark,raw_slots)

        f1.write(temp[0]+'\t'+deal_mark+'\t'+deal_asr+'\t'+deal_keywords+'\t'+'\t'.join(temp[4:]))
        f2.write(temp[0]+'\t'+deal_mark.lower()+'\t'+deal_asr.lower()+'\t'+deal_keywords.lower()+'\t'+'\t'.join(temp[4:]))

    f1.close()
    f2.close()