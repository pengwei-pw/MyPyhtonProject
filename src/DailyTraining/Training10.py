#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training10.py
# @Time      :2025/11/25 13:31:09
# @Author    :PengWei

import re
import os

input_file = r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\U625H-1-1-0\WakeUp"           # 输入日志文件
output_file = r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\U625H-1-1-0\new"   # 输出拆分后的文件

# 匹配时间戳模式，例如 [10:39:11]
timestamp_pattern = r'(\[\d{2}:\d{2}:\d{2}\])'

def split_by_timestamp(text):
    """
    将整个文本按时间戳切分成一条条记录。
    时间戳保持在每条记录开头。
    """

    # 将文本按时间戳拆分，并保留时间戳本身
    parts = re.split(timestamp_pattern, text)

    results = []
    current = ""

    for part in parts:
        if re.fullmatch(timestamp_pattern, part):
            # 遇到新的时间戳，则把前一个日志条目保存
            if current.strip():
                results.append(current.strip())
            # 开始新的日志记录
            current = part
        else:
            current += part

    # 最后一条
    if current.strip():
        results.append(current.strip())

    return results


# =============================
# 主执行逻辑
# =============================

for file in os.listdir(input_file):
    filename = os.path.join(input_file, file)
    print(f"正在处理文件：{filename}")
    

    with open(filename, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 拆分日志
    records = split_by_timestamp(raw_text)
    print(len(records), "条日志")

    # 写出结果
    with open(os.path.join(output_file, file), "w", encoding="utf-8") as f:
        for r in records:
            f.write(r + "\n")

    print(f"处理完成：共拆分 {len(records)} 条日志，输出文件：{output_file}")
