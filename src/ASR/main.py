# -*- coding: utf-8 -*-
"""
created on 1/9/2023
@author tengchen CTENG9@ford.com

"""

import os
import shutil
import time
import subprocess
import io
import xlrd
# import sys

def main_deal(sheetname):
    file1 = 'temp/'+sheetname+'_raw_data.txt'
    file2 = 'temp/'+sheetname+'_input_raw.txt'
    file3 = 'temp/'+sheetname+'_input_lower.txt'
    file4 = 'temp/'+sheetname+'_count_each_raw.txt'
    file5 = 'temp/'+sheetname+'_count_each_lower.txt'
    file6 = 'result/'+sheetname+'_result_raw.txt'
    file7 = 'result/'+sheetname+'_result_lower.txt'
    file8 = 'final_result/'+sheetname+'_result.csv'
    
    command1 = 'python read_excel.py '+data_path+' '+sheetname+' '+file1
    command2 = 'python advance_deal.py '+file1+' '+file2+' '+file3
    command3 = 'python count_each.py '+file2+' '+file4
    command4 = 'python count_each.py '+file3+' '+file5
    command5 = 'python gather_result.py '+file2+' '+file4+' '+file6
    command6 = 'python gather_result.py '+file3+' '+file5+' '+file7
    command7 = 'python write_csv.py '+file6+' '+file7+' '+file8
    cmd = [command1,command2,command3,command4,command5,command6,command7]
    
    for command in cmd:
        proc = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        stream_stdout = io.TextIOWrapper(proc.stdout, encoding='gbk')
        stream_stderr = io.TextIOWrapper(proc.stderr, encoding='gbk')
        
        str_stdout = str(stream_stdout.read())
        str_stderr = str(stream_stderr.read())
        
        if str_stdout:
            print(str_stdout)
        if str_stderr:
            print('errorMag: '+str_stderr)

if __name__ == '__main__':
    t1 = time.time()
    
    for folder in ['temp','result','final_result']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            time.sleep(0.1)
            os.mkdir(folder)
    data_path = 'test.xlsx'
    # classes = '垂类/噪音环境/年龄段/性别_年龄段/噪音环境_垂类'
    ff = xlrd.open_workbook(data_path)
    sheets = ff.sheet_names()
    
    for sheet in sheets:
        main_deal(sheet)
        
    t2 = time.time()
    
    print('执行完毕，用时： %ds' % (t2-t1))