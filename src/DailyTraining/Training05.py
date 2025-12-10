#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training05.py
# @Time      :2025/07/30 13:44:08
# @Author    :PengWei
import os
import pandas as pd
import numpy as np
import string
import re

def remove_punctuation(text):
    """
    去除字符串中所有中英文标点符号
    """
    # 1. 定义所有需要去除的标点（英文+中文）
    punctuation = string.punctuation  # 英文标点：!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    chinese_punctuation = '，。；：‘’“”！？【】（）《》〈〉『』「」﹑…—～、'
    all_punctuation = punctuation + chinese_punctuation
    
    # 2. 方法一：使用列表推导式过滤（适合简单场景）
    # result = ''.join([char for char in text if char not in all_punctuation])
    
    # 2. 方法二：使用正则表达式（更高效，支持复杂场景）
    # 构建正则模式：匹配所有标点
    pattern = f"[{re.escape(all_punctuation)}]"
    result = re.sub(pattern, '', text)
    return result

def analyze_faq_excel():
    faq_excel_path = r"C:\Users\pengw\Desktop\HALO\LLM\llm测试语料\new0910_PP_003\【Baseline】【CD483-H】【Ford】【Halo】【V2.0】LLM_车知识FAQ_1017.xlsx"
    df_faq = pd.read_excel(faq_excel_path, sheet_name='车知识专家FAQ')
    df_faq_temp = pd.DataFrame(columns=['一级分类', '二级分类', 'Query', '参考答案'])
    index_i = 0
    for index, row in df_faq.iterrows():
        lever_1 = 'FAQ'
        lever_2 = 'FAQ'
        query = ''
        answer = ''
        for key, value in row.items():
            if key == '核心query' and isinstance(value, str):
                query_list = value.split('\n')
                query_list = [remove_punctuation(q.strip().replace(' ', '')) for q in query_list if q.strip()]
                if not query_list:
                    continue
                # print(query_list)
            if key in ['文本答案', '提示', '引导语', '步骤1', '步骤2', '步骤3', '步骤4', '步骤5', '警告']:
                answer += str(value).strip()
            if key == '警告':
                if answer != '' and query_list:
                    for i in query_list:
                        print(i, lever_1, lever_2, answer)
                        df_faq_temp.at[index_i, '一级分类'] = lever_1
                        df_faq_temp.at[index_i, '二级分类'] = lever_2
                        df_faq_temp.at[index_i, 'query'] = i
                        df_faq_temp.at[index_i, '参考答案'] = answer.replace('nan', '')
                        index_i += 1
                    answer = ''
                    query_list = []

    df_faq_temp.to_excel(r'C:\Users\pengw\Desktop\HALO\LLM\llm测试语料\new0910_PP_003\CX483-H-FAQ.xlsx', index=False)
if __name__ == "__main__":
    analyze_faq_excel()