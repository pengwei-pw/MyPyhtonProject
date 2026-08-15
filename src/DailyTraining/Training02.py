#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training02.py
# @Time      :2025/07/17 16:26:13
# @Author    :PengWei

import pandas as pd
import os
import shutil

def demo1():
    r05_path = r'C:\Users\pengw\Desktop\语音识别唤醒结果\CD542H\R05_063\MediumMatching\report\CD542MCA_H&L_VR性能自动化测试.xlsx'
    r06_path = r'C:\Users\pengw\Desktop\语音识别唤醒结果\CD542H\R06_071\CD542H_HL\report\CD542MCA_HL_VR性能自动化测试.xlsx'

    r05_df = pd.read_excel(r05_path, sheet_name='CD542H中配指令词原始数据整合')
    r06_df = pd.read_excel(r06_path, sheet_name='指令词原始数据整合')

    cun_path = r'C:\Users\pengw\Desktop\语音识别唤醒结果\r05_r06_check_noise'
    R06_dirver = r"C:\Users\pengw\Desktop\MixNoise\CD542HL\addnoise\command_driver"
    R06_passenger = r"C:\Users\pengw\Desktop\MixNoise\CD542HL\addnoise\command_passenger"

    df = pd.DataFrame(columns=['噪声场景', '期望唤醒音区', 'RO5在线FAIL条数', 'RO6在线FAIL条数', '在线Fail重复条数'])
    noise_list = ['noise001', 'noise008', 'noise009', 'noise010', 'noise011', 'noise012', 'noise013', 'noise014', 'noise015', 'noise016', 'dacheganrao', 'gongzhenzaosheng']
    noise_columns = ['音频名', '期望识别结果','r05在线识别结果','r06在线识别结果','期望唤醒音区']
    index_count = -1
    with pd.ExcelWriter(r'C:\Users\pengw\Desktop\语音识别唤醒结果\r05_r06_check_noise\output.xlsx', engine='openpyxl') as writer:
        for noise in noise_list:
            noise_fail_r05_dirver = r05_df[(r05_df['噪声场景'] == noise) & (r05_df['期望唤醒音区'] == 'driver') & (r05_df['在线结果'] == 'Fail')]
            noise_fail_r05_passenger = r05_df[(r05_df['噪声场景'] == noise) & (r05_df['期望唤醒音区'] == 'passenger') & (r05_df['在线结果'] == 'Fail')]
            noise_fail_r06_dirver = r06_df[(r06_df['噪声场景'] == noise) & (r06_df['期望唤醒音区'] == 'Driver') & (r06_df['在线结果'] == 'Fail')]
            noise_fail_r06_passenger = r06_df[(r06_df['噪声场景'] == noise) & (r06_df['期望唤醒音区'] == 'Passenger') & (r06_df['在线结果'] == 'Fail')]
            df_noise = pd.DataFrame(columns=noise_columns)
            count_driver = 0
            for index, row in noise_fail_r06_dirver.iterrows():
                query = row['期望指令词']
                r05_row = noise_fail_r05_dirver[noise_fail_r05_dirver['期望指令词'] == query]
                if noise_fail_r05_dirver['期望指令词'].isin([query]).any():
                    count_driver += 1
                    os.makedirs(os.path.join(cun_path, noise, 'driver'), exist_ok=True)
                    if not os.path.exists(os.path.join(cun_path, noise, row['数据'])):
                        shutil.copy(os.path.join(R06_dirver, row['数据']), os.path.join(cun_path, noise,'driver' ,row['数据']))
                    df_noise.at[index, '音频名'] = row['数据']
                    df_noise.at[index, '期望识别结果'] = row['期望指令词']
                    df_noise.at[index, 'r05在线识别结果'] = r05_row['在线识别结果'].values[0] if not r05_row.empty else ''
                    df_noise.at[index, 'r06在线识别结果'] = row['在线识别结果']
                    df_noise.at[index, '期望唤醒音区'] = 'driver'
            count_passenger = 0
            for index, row in noise_fail_r06_passenger.iterrows():
                query = row['期望指令词']
                r05_row = noise_fail_r05_passenger[noise_fail_r05_passenger['期望指令词'] == query]
                if noise_fail_r05_passenger['期望指令词'].isin([query]).any():
                    count_passenger += 1
                    os.makedirs(os.path.join(cun_path, noise, 'passenger'), exist_ok=True)
                    if not os.path.exists(os.path.join(cun_path, noise, row['数据'])):
                        shutil.copy(os.path.join(R06_passenger, row['数据']), os.path.join(cun_path, noise,'passenger', row['数据']))
                    df_noise.at[index+count_driver, '音频名'] = row['数据']
                    df_noise.at[index+count_driver, '期望识别结果'] = row['期望指令词']
                    df_noise.at[index+count_driver, 'r05在线识别结果'] = r05_row['在线识别结果'].values[0] if not r05_row.empty else ''
                    df_noise.at[index+count_driver, 'r06在线识别结果'] = row['在线识别结果']
                    df_noise.at[index+count_driver, '期望唤醒音区'] = 'passenger'
                    
            df_noise.to_excel(writer, sheet_name=noise, index=False)
            print('driver',len(noise_fail_r05_dirver), len(noise_fail_r06_dirver), count_driver)
            print('passenger',len(noise_fail_r05_passenger), len(noise_fail_r06_passenger), count_passenger)
            index_count += 1
            df.at[index_count, '噪声场景'] = noise
            df.at[index_count, '期望唤醒音区'] = 'driver'
            df.at[index_count, 'RO5在线FAIL条数'] = len(noise_fail_r05_dirver)
            df.at[index_count, 'RO6在线FAIL条数'] = len(noise_fail_r06_dirver)
            df.at[index_count, '在线Fail重复条数'] = count_driver
            index_count += 1
            df.at[index_count, '噪声场景'] = noise
            df.at[index_count, '期望唤醒音区'] = 'passenger'
            df.at[index_count, 'RO5在线FAIL条数'] = len(noise_fail_r05_passenger)
            df.at[index_count, 'RO6在线FAIL条数'] = len(noise_fail_r06_passenger)
            df.at[index_count, '在线Fail重复条数'] = count_passenger
        df.to_excel(writer, sheet_name='all', index=False)
if __name__ == "__main__":
    demo1()
    print("This is a placeholder for demo1 function in Training02.py.")
    # You can add more functionality or calls to other functions as needed.