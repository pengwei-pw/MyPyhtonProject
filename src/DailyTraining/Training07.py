#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training07.py
# @Time      :2025/08/21 13:52:42
# @Author    :PengWei

import os
import pandas as pd

def excel_compare():
    """
    比较两个Excel文件的内容，控制台打印不同行
    """
    df_H = pd.read_excel(R'C:\Users\pengw\Desktop\LLM\llm测试语料\TEMP\CD542-L-FAQ.xlsx')
    df_L = pd.read_excel(R'C:\Users\pengw\Desktop\LLM\llm测试语料\TEMP\CD542-H-FAQ.xlsx')
    print("CD542-L-FAQ行数:", len(df_L))
    print("CD542-H-FAQ行数:", len(df_H))

    # 找到不同的行
    for index, row in df_L.iterrows():
        query = row['query']
        ex = df_H[df_H['query'] == query]
        if ex.empty:
            print(f"CD542-L-FAQ中有一行在CD542-H-FAQ中未找到: {query}")


if __name__ == "__main__":
    excel_compare()