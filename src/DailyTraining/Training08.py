#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training08.py
# @Time      :2025/08/26 16:53:37
# @Author    :PengWei
import os
import pandas as pd
import shutil

def demo():
    path_df_new = pd.read_excel(r'C:\Users\pengw\Desktop\语音识别唤醒结果\R07\CD542HL\CD542MCA_HL_VR性能自动化测试new.xlsx', sheet_name='指令词原始数据整合')
    path_df_old = pd.read_excel(r'C:\Users\pengw\Desktop\语音识别唤醒结果\R06_542H\CD542MCA_H_R06_VR性能自动化测试.xlsx', sheet_name='CD542H内置指令词原始数据整合')

    df_new_fail = path_df_new[(path_df_new['在线结果'] == 'Fail')]
    df_old_fail = path_df_old[(path_df_old['在线结果'] == 'Fail')]
    path_1 = r'C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\mix_5db\command_driver'
    path_2 = r"C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\mix_5db\command_passenger"
    df_1 = pd.DataFrame(columns=["文件名", "音频格式","状态", "录音文本", "主驾分贝", "副驾分贝", "车型", "噪声id"])
    df_2 = pd.DataFrame(columns=["文件名", "音频格式","状态", "录音文本", "主驾分贝", "副驾分贝", "车型", "噪声id"])
    for index, row in df_new_fail.iterrows():
        file_name = row['数据']
        if not df_old_fail['数据'].isin([file_name]).any():
            if row['期望唤醒音区'] == 'Driver':
                src_path = os.path.join(path_1, file_name)
                dst_path = os.path.join(r"C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\asr_fail_new\command_driver", file_name)
                if os.path.exists(src_path):
                    shutil.copy(src_path, dst_path)
                    df_1.at[index, '文件名'] = row['数据']
                    df_1.at[index, '音频格式'] = 1000
                    df_1.at[index, '状态'] = 'mix'
                    df_1.at[index, '录音文本'] = row['期望指令词']
                    df_1.at[index, '主驾分贝'] = ""
                    df_1.at[index, '副驾分贝'] = ""
                    df_1.at[index, '车型'] = "cd542mca_hl"
                    df_1.at[index, '噪声id'] = row['数据'].split('_')[1]
            elif row['期望唤醒音区'] == 'Passenger':
                src_path = os.path.join(path_2, file_name)
                dst_path = os.path.join(r"C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\asr_fail_new\command_passenger", file_name)
                if os.path.exists(src_path):
                    shutil.copy(src_path, dst_path)
                    df_2.at[index, '文件名'] = row['数据']
                    df_2.at[index, '音频格式'] = 1000
                    df_2.at[index, '状态'] = 'mix'
                    df_2.at[index, '录音文本'] = row['期望指令词']
                    df_2.at[index, '主驾分贝'] = ""
                    df_2.at[index, '副驾分贝'] = ""
                    df_2.at[index, '车型'] = "cd542mca_hl"
                    df_2.at[index, '噪声id'] = row['数据'].split('_')[1]
    df_1.to_excel(r"C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\asr_fail_new\command_driver\command_driver_fail_new.xlsx", index=False)
    df_2.to_excel(r"C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\asr_fail_new\command_passenger\command_passenger_fail_new.xlsx", index=False)

if __name__ == "__main__":
    demo()