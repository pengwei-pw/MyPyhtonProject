#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training06.py
# @Time      :2025/08/03 17:26:48
# @Author    :PengWei

import os
import pandas as pd
import string
import re
def ss():
    df = pd.read_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542L\result.xlsx', sheet_name='Sheet1')
    for index, row in df.iterrows():
        df.at[index, 'Query'] = remove_punctuation(row['Query'].strip().replace(' ', ''))
    df.to_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542L\result_cleaned.xlsx', index=False)
    
def analyze_faq_excel():
    path_df = pd.read_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542L\result_cleaned.xlsx', sheet_name='Sheet1')
    dui_df = pd.read_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542L\CD542-M-FAQ.xlsx', sheet_name='Sheet1')
    # print(f"对照表行数: {len(dui_df)}")
    # df_faq = pd.DataFrame(columns=['一级分类', '二级分类', 'query', '参考答案'])
    # ss = 0
    # for index, row in dui_df.iterrows():
    #     query = row['query']
    #     if pd.isna(query):
    #         print(f"第{index}行的query为空，跳过")
    #         continue
    #     query = query.strip().replace(' ', '')
    #     if not query:
    #         print(f"第{index}行的query为空字符串，跳过")
    #         continue
    #     # 查找对应的答案
    #     answer_row = path_df[path_df['Query'] == query]
    #     if answer_row.empty:
    #         new_row = pd.DataFrame([[row['一级分类'], row['二级分类'], query, row['参考答案']]], columns=['一级分类', '二级分类', 'query', '参考答案'])
    #         df_faq = pd.concat([df_faq,new_row], ignore_index=True)
    #     else:
    #         ss += 1
        
    # print(f"未找到答案的FAQ数量: {len(df_faq)}")
    # print(f"找到答案的FAQ数量: {ss}")
    
    # df_faq.to_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542L\faq_not_in_untest.xlsx', index=False)
            

    count = 0
    for index, row in path_df.iterrows():
        query = row['Query']
        if pd.isna(query):
            print(f"第{index}行的query为空，跳过")
            continue
        query = query.strip().replace(' ', '')
        if not query:
            print(f"第{index}行的query为空字符串，跳过")
            continue
        # 查找对应的答案
        
        answer_row = dui_df[dui_df['query'] == query]
        if answer_row.empty:
            # print(f"第{index}行的query在对照表中未找到，跳过")
            continue
        count = count + 1
        answer = answer_row.iloc[0]['参考答案']
        path_df.at[index, '参考答案'] = answer if not pd.isna(answer) else ''
    
    # 保存结果
    print(f"共处理了 {count} 条记录。")
    # path_df.to_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542H\result_updated.xlsx', index=False)
        

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

def analyze_faq_excel_d():
    path_df = pd.read_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542H\result.xlsx', sheet_name='Sheet1')
    dui_df = pd.read_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542H\CD542-H-FAQ.xlsx', sheet_name='Sheet1')
    path_df_list = path_df['Query'].tolist()
    path_df_list = [remove_punctuation(q.strip().replace(' ', '')) for q in path_df_list if isinstance(q, str)]
    print(f"对照表行数: {len(dui_df)}")
    df_faq = pd.DataFrame(columns=['一级分类', '二级分类', 'query', '参考答案'])
    ss = 0
    for index, row in dui_df.iterrows():
        query = row['query']
        if pd.isna(query):
            print(f"第{index}行的query为空，跳过")
            continue
        query = remove_punctuation(query.strip().replace(' ', ''))
        if not query:
            print(f"第{index}行的query为空字符串，跳过")
            continue
        # 查找对应的答案
        
        if query not in path_df_list:
            new_row = pd.DataFrame([[row['一级分类'], row['二级分类'], query, row['参考答案']]], columns=['一级分类', '二级分类', 'query', '参考答案'])
            df_faq = pd.concat([df_faq,new_row], ignore_index=True)
        else:
            ss += 1
    df_faq.to_excel(r'C:\Users\pengw\Desktop\LLM\R07\CD542H\faq__untest.xlsx', index=False)    
    print(f"未找到答案的FAQ数量: {len(df_faq)}")
    print(f"找到答案的FAQ数量: {ss}")

if __name__ == "__main__":
    analyze_faq_excel_d()
    print("FAQ分析完成，结果已保存。")