# -*- coding: utf-8 -*-
"""
created on 12/23/2022
@author tengchen CTENG9@ford.com

"""

import xlrd
from xlrd import xldate_as_tuple
import datetime
import sys

class ExcelData():
    def __init__(self,data_path,sheetname):
        self.data_path = data_path
        self.sheetname = sheetname
        self.data = xlrd.open_workbook(self.data_path)
        self.table = self.data.sheet_by_name(self.sheetname)
        # self.table = self.data.sheet_by_name(0)
        self.keys = self.table.row_values(0)
        self.rowNum = self.table.nrows
        self.colNum = self.table.ncols

    def readExcel(self):
        datas = []
        for i in range(1,self.rowNum):
            sheet_data = {}
            for j in range(self.colNum):
                c_type = self.table.cell(i,j).ctype
                c_cell = self.table.cell_value(i,j)
                if c_type == 2 and c_cell % 1 == 0:  #如果是整型
                    c_cell = int(c_cell)
                elif c_type == 3:
                    try:
                        date = datetime.datetime(*xldate_as_tuple(c_cell,0))
                        c_cell = date.strftime('%Y/%m/%d')
                    except Exception as e:
                        c_cell = str(c_cell)
                elif c_type == 4:
                    c_cell = True if c_cell == 1 else False
                sheet_data[self.keys[j]] = str(c_cell).replace('\r\n','')
            datas.append(sheet_data)
        # col_titles = self.keys
        return datas

if __name__ == "__main__":
    print('正在读取表格数据...')

    data_path = sys.argv[1]
    sheetname = sys.argv[2]
    outputfile = sys.argv[3]
    get_data = ExcelData(data_path, sheetname)
    datas = get_data.readExcel()
    col_titles = ['音频名称','预期结果','识别结果','NLU预期槽位','预期垂类','噪声场景','性别','年龄段']
    f = open(outputfile,'w',encoding='utf-8')
    f.write('音频名称\t预期结果\t识别结果\tNLU预期槽位\t预期垂类\t噪声场景\t性别\t年龄段\n')
    for i in datas:
        for title in col_titles:
            if title == col_titles[-1]:
                f.write(str(i[title]).strip()+'\n')
            else:
                f.write(str(i[title]).strip()+'\t')
    f.close()