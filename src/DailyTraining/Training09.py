#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training09.py
# @Time      :2025/11/05 10:22:16
# @Author    :PengWei
import shutil
import os

if __name__ == "__main__":
    txt_path = r'C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\483R06\对比\old200.txt'
    new_path = r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\483R06\对比\old200_noise010"
    micin_path = r'D:\Audio_禁止删除\CD542H高配音频\addnoise\command_dirver'
    with open(txt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            # name = line.replace('Mix_noise010', 'Record').strip()
            # print(name)
            name = line.strip()
            shutil.copy(os.path.join(micin_path, name), os.path.join(new_path, name))


    