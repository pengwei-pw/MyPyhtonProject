# -*- coding: utf-8 -*-
"""
created on 1/6/2023
@author tengchen CTENG9@ford.com

"""
import sys

def one_level_class(cla,inputfile,outputfile):
    d = {}
    D = {'All':[0,0,0,0,0,0,0]}   #总句数，空白句数，对字数，总字数，关键词正确数，关键词总数，对句数
    cate_list = []
    with open(inputfile,'r',encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            temp = line.strip().split('\t')
            d[temp[0]] = [0,0,0,0,0,0,0] ##错字数，少字数，多字数，总字数，是否为err，关键词正确数，关键词总数
            d[temp[0]][0],d[temp[0]][1],d[temp[0]][2] = int(temp[1]),int(temp[2]),int(temp[3])
            d[temp[0]][3],d[temp[0]][4],d[temp[0]][5] = int(temp[4]),int(temp[5]),int(temp[6])
            d[temp[0]][6] = int(temp[7])
    inputfile2 = inputfile.replace('count_each','input')
    with open(inputfile2,'r',encoding='utf-8') as f:
        lines = f.readlines()
    titles = lines[0].strip().split('\t')
    cla_index = titles.index(cla)
    for line in lines[1:]:
        temp = line.split('\t')
        audio = temp[0]
        cate = temp[cla_index].strip()
        if not cate:
            cate = 'None'
        if cate not in D:
            D[cate] = [0,0,0,0,0,0,0]
            cate_list.append(cate)
        D[cate][0] += 1
        D['All'][0] += 1
        D[cate][1] += d[audio][4]
        D['All'][1] += d[audio][4]
        D[cate][2] += d[audio][3] - d[audio][0] - d[audio][1] - d[audio][2]
        D['All'][2] += d[audio][3] - d[audio][0] - d[audio][1] - d[audio][2]
        D[cate][3] += d[audio][3]
        D['All'][3] += d[audio][3]
        D[cate][4] += d[audio][5]
        D['All'][4] += d[audio][5]
        D[cate][5] += d[audio][6]
        D['All'][5] += d[audio][6]
        if d[audio][0]+d[audio][1]+d[audio][2] == 0:
            D[cate][6] += 1
            D['All'][6] += 1
    cate_list.sort(reverse=False)
    cate_list[0:0] = ['All']
    f0 = open(outputfile,'a',encoding='utf-8')
    f0.write(cla+'\t总句数\t空白句数\t字准率\t关键词准确率\t句准率\n')
    for cate in cate_list:
        word_accurate = D[cate][2]/D[cate][3]*100
        sentence_accurate = D[cate][6]/D[cate][0]*100
        if D[cate][5] == 0:
            keyword_accurate = 'Null'
        else:
            keyword_accurate = '%.2f%%' % (D[cate][4]/D[cate][5]*100)
        f0.write('%s\t%d\t%d\t%.2f%%\t%s\t%.2f%%\n' % (cate,D[cate][0],D[cate][1],word_accurate,keyword_accurate,sentence_accurate))
    f0.write('\n')
    f0.close()
    
def two_level_class(cla1,cla2,inputfile,outputfile):
    cla = cla1 + '_' + cla2
    d = {}
    D = {'All':[0,0,0,0,0,0,0]}  #总句数，空白句数，对字数，总字数，关键词正确数，关键词总数，对句数
    cate_list = []
    with open(inputfile,'r',encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            temp = line.strip().split('\t')
            d[temp[0]] = [0,0,0,0,0,0,0] #错字数，少字数，多字数，总字数，是否为err，关键词正确数，关键词总数
            d[temp[0]][0],d[temp[0]][1],d[temp[0]][2] = int(temp[1]),int(temp[2]),int(temp[3])
            d[temp[0]][3],d[temp[0]][4],d[temp[0]][5] = int(temp[4]),int(temp[5]),int(temp[6])
            d[temp[0]][6] = int(temp[7])
    inputfile2 = inputfile.replace('count_each','input')
    with open(inputfile2,'r',encoding='utf-8') as f:
        lines = f.readlines()
    titles = lines[0].strip().split('\t')
    cla1_index = titles.index(cla1)
    cla2_index = titles.index(cla2)
    for line in lines[1:]:
        temp = line.split('\t')
        audio = temp[0]
        cate1 = temp[cla1_index].strip()
        cate2 = temp[cla2_index].strip()
        cate = cate1 + '_' + cate2
        if 'None' in cate:
            cate = 'None'
        if cate not in D:
            D[cate] = [0,0,0,0,0,0,0]
            cate_list.append(cate)
        D[cate][0] += 1
        D['All'][0] += 1
        D[cate][1] += d[audio][4]
        D['All'][1] += d[audio][4]
        D[cate][2] += d[audio][3] - d[audio][0] - d[audio][1] - d[audio][2]
        D['All'][2] += d[audio][3] - d[audio][0] - d[audio][1] - d[audio][2]
        D[cate][3] += d[audio][3]
        D['All'][3] += d[audio][3]
        D[cate][4] += d[audio][5]
        D['All'][4] += d[audio][5]
        D[cate][5] += d[audio][6]
        D['All'][5] += d[audio][6]
        if d[audio][0]+d[audio][1]+d[audio][2] == 0:
            D[cate][6] += 1
            D['All'][6] += 1
    cate_list.sort(reverse=False)
    cate_list[0:0] = ['All']
    f0 = open(outputfile,'a',encoding='utf-8')
    f0.write(cla+'\t总句数\t空白句数\t字准率\t关键词准确率\t句准率\n')
    for cate in cate_list:
        word_accurate = D[cate][2]/D[cate][3]*100
        sentence_accurate = D[cate][6]/D[cate][0]*100
        if D[cate][5] == 0:
            keyword_accurate = 'Null'
        else:
            keyword_accurate = '%.2f%%' % (D[cate][4]/D[cate][5]*100)
        f0.write('%s\t%d\t%d\t%.2f%%\t%s\t%.2f%%\n' % (cate,D[cate][0],D[cate][1],word_accurate,keyword_accurate,sentence_accurate))
    f0.write('\n')
    f0.close()
    
    
if __name__ == '__main__':
    print('正在汇总结果...')
    
    classify = ['预期垂类','噪声场景','性别','年龄段']
    # classify = ['预期垂类']
    inputfile1 = sys.argv[2]
    inputfile2 = sys.argv[1]
    outputfile = sys.argv[3]
    
    with open(inputfile2,'r',encoding='utf-8') as f:
        lines = f.readlines()
        
    titles = lines[0].strip().split('\t')
    
    for cla in classify:
        one_level_class(cla,inputfile1,outputfile)
        if cla == '性别':
            cla1 = cla
            cla2 = '年龄段'
            two_level_class(cla1,cla2,inputfile1,outputfile)
        if cla == '噪声场景':
            cla1 = cla
            cla2 = '预期垂类'
            two_level_class(cla1,cla2,inputfile1,outputfile)