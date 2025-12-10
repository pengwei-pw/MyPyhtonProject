#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training11.py
# @Time      :2025/11/25 13:56:52
# @Author    :PengWei

import os
import re

# 输入输出文件夹
input_folder = r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\U625H-1-1-0\Wakeup"
output_folder = r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\U625H-1-1-0\new"

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 正则匹配关键内容
RE_PCM = re.compile(r'WAKEUP fileName--->\s*(.+?\.pcm)')
RE_OUTPUT = re.compile(r'唤醒成功(\d+)次,主驾唤醒(\d+)次,副驾唤醒(\d+)次')

# 遍历文件夹
for filename in os.listdir(input_folder):
    # if not filename.lower().endswith(".txt"):
    #     continue  # 忽略非 txt 文件

    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, filename)  # 保留原文件名

    seen_pcm = set()
    current_record = []
    current_pcm = None

    # 清空输出文件
    open(output_file, "w", encoding="utf-8").close()

    with open(input_file, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip()

            pcm_match = RE_PCM.search(line)
            if pcm_match:
                pcm_in_line = pcm_match.group(1)
                # 内部去重，防止同条记录重复 PCM
                if any(pcm_in_line in l for l in current_record):
                    continue
                current_pcm = pcm_in_line

            current_record.append(line)

            if RE_OUTPUT.search(line):
                if current_pcm and current_pcm not in seen_pcm:
                    seen_pcm.add(current_pcm)
                    # 添加分隔线（仅在末尾没有）
                    if not current_record[-1].strip() == "-------------------------------------------":
                        current_record.append("-------------------------------------------")
                    # 写入输出文件
                    with open(output_file, "a", encoding="utf-8") as out_f:
                        for rec_line in current_record:
                            out_f.write(rec_line + "\n")
                # 重置临时记录
                current_record = []
                current_pcm = None

    print(f"{filename} 去重完成，共 {len(seen_pcm)} 条唯一 PCM，输出文件：{output_file}")

print("\n所有文件处理完成。")
