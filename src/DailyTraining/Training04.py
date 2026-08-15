#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training04.py
# @Time      :2025/07/23 15:45:52
# @Author    :PengWei

import pandas as pd
import shutil
import os

def demo():
    df = pd.read_excel(r'C:\Users\pengw\Desktop\asrtemp\CD542MCA_H_R06_VR性能自动化测试.xlsx', sheet_name='CD542H中配指令词原始数据整合')
    micin_path = r"C:\Users\pengw\Desktop\MixNoise\CD542HL\micin\command_driver"
    df_1 = pd.DataFrame(columns=["文件名", "音频格式","状态", "录音文本", "主驾分贝", "副驾分贝", "车型", "噪声id"])
    out_noise011_path = r"C:\Users\pengw\Desktop\asrtemp\noise011"
    df = df[(df['在线结果'] == 'Fail') & (df['期望唤醒音区'] == 'Driver')]
    set_name = set()
    for index, row in df.iterrows():
        name = row['数据']
        name_list = name.split('_')
        name_list = name_list[7:]
        set_name.add('_'.join(name_list))
        print('_'.join(name_list))
    print(len(set_name))
    for name in set_name:
        for audo_name in os.listdir(micin_path):
            if name in audo_name:
                shutil.copy(os.path.join(micin_path, audo_name), out_noise011_path)
                

def demo1():
    df = pd.read_excel(r'C:\Users\pengw\Desktop\asrtemp\CD542MCA_H_R06_VR性能自动化测试.xlsx', sheet_name='CD542H中配指令词原始数据整合')
    df_1 = pd.DataFrame(columns=["文件名", "音频格式","状态", "录音文本", "主驾分贝", "副驾分贝", "车型", "噪声id"])
    df = df[df['噪声场景'] == 'noise011']
    for idnex, name in enumerate(os.listdir(r"C:\Users\pengw\Desktop\asrtemp\noise011")):
        if df['文件名'].isin([name]).any():
            row = df[df['文件名'] == name].iloc[0]
            df_1.at[idnex, '文件名'] = row['文件名']
            df_1.at[idnex, '音频格式'] = row['音频格式']
            df_1.at[idnex, '状态'] = row['状态']
            df_1.at[idnex, '录音文本'] = row['录音文本']
            df_1.at[idnex, '主驾分贝'] = row['主驾分贝']
            df_1.at[idnex, '副驾分贝'] = row['副驾分贝']
            df_1.at[idnex, '车型'] = row['车型']
    df_1.to_excel(r"C:\Users\pengw\Desktop\asrtemp\noise011标注.xlsx", index=False)


import soundfile as sf
import numpy as np

def process_pcm_to_pcm(input_path, output_path, db_increase=5, samplerate=16000, 
                       channels=8, subtype='PCM_16'):
    """
    处理PCM文件（8通道，16000Hz），提高音量后仍输出为PCM格式
    
    参数:
        input_path: 输入PCM文件路径
        output_path: 输出PCM文件路径
        db_increase: 提高的分贝数
        samplerate: 采样率（固定为16000Hz）
        channels: 通道数（8通道）
        subtype: PCM位深格式（如'PCM_16'）
    """
    # 读取原始PCM文件
    data, _ = sf.read(
        input_path,
        samplerate=samplerate,
        channels=channels,
        subtype=subtype,
        format='RAW'  # 读取原始PCM
    )
    
    print(f"读取信息 - 采样率: {samplerate}Hz, 通道数: {channels}, "
          f"样本数: {data.shape[0]}, 位深: {subtype}")
    
    # 计算音量调整比例
    amplitude_ratio = 10 **(db_increase / 20)
    adjusted_data = data * amplitude_ratio
    
    # 防止削波（超过[-1,1]范围会导致失真）
    max_amp = np.max(np.abs(adjusted_data))
    if max_amp > 1.0:
        adjusted_data /= max_amp
        print(f"警告：音量调整导致过载，已归一化（原最大振幅: {max_amp:.2f}）")
    
    # 保存为PCM格式（无头部信息）
    sf.write(
        output_path,
        adjusted_data,
        samplerate=samplerate,
        subtype=subtype,
        format='RAW'
    )
    
    print(f"处理完成，PCM文件已保存到: {output_path}")

def demo2():
    for name in os.listdir(r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\483R06\对比\new200_micin"):
        if name.endswith('.pcm'):
            path = os.path.join(r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\483R06\对比\new200_micin", name)
            output_pcm = os.path.join(r"C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\483R06\对比\new200_micin_8db",name)
            process_pcm_to_pcm(
                input_path=path,
                output_path=output_pcm,
                db_increase=8,
                samplerate=16000,
                channels=8,
                subtype='PCM_16'  # 确保与输入PCM的位深一致
            )

def demo5():
    df = pd.read_excel(r'C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\CD542MCA_HL_VR性能自动化测试.xlsx', sheet_name='指令词原始数据整合')
    micin_path = r"C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\mix_5db\command_passenger"
    df_1 = pd.DataFrame(columns=["文件名", "音频格式","状态", "录音文本", "主驾分贝", "副驾分贝", "车型", "噪声id"])
    out_noise011_path = r"C:\Users\pengw\Desktop\MixNoise\CD542HL_5DB\asr_fail\command_passenger"
    df = df[(df['在线结果'] == 'Fail') & (df['期望唤醒音区'] == 'Passenger')]
    print(len(df))
    for index, row in df.iterrows():
        shutil.copy(os.path.join(micin_path, row['数据']), out_noise011_path)
        df_1.at[index, '文件名'] = row['数据']
        df_1.at[index, '音频格式'] = 1000
        df_1.at[index, '状态'] = 'mix'
        df_1.at[index, '录音文本'] = row['期望指令词']
        df_1.at[index, '主驾分贝'] = ""
        df_1.at[index, '副驾分贝'] = ""
        df_1.at[index, '车型'] = "cd542mca_hl"
        df_1.at[index, '噪声id'] = row['数据'].split('_')[1]
    df_1.to_excel(os.path.join(out_noise011_path, 'cd542hh_command_passenger_fail.xlsx'), index=False)

def demo6():
    df = pd.read_excel(r'C:\Users\pengw\Desktop\MixNoise\CD542HH_5DB\CD542MCA_HH_VR性能自动化测试.xlsx', sheet_name='唤醒词原始数据整合')
    micin_path = r"C:\Users\pengw\Desktop\MixNoise\CD542HH_5DB\mix_5db\wakeup_passenger"
    df_1 = pd.DataFrame(columns=["文件名", "音频格式","状态", "录音文本", "主驾分贝", "副驾分贝", "车型", "噪声id"])
    out_noise011_path = r"C:\Users\pengw\Desktop\MixNoise\CD542HH_5DB\asr_fail\wakeup_passenger"
    df = df[(df['期望唤醒音区'] == 'Passenger') & (df['唤醒成功'] <= 18)]
    print(len(df))
    for index, row in df.iterrows():
        shutil.copy(os.path.join(micin_path, row['数据']), out_noise011_path)
        df_1.at[index, '文件名'] = row['数据']
        df_1.at[index, '音频格式'] = 1000
        df_1.at[index, '状态'] = 'mix'
        df_1.at[index, '录音文本'] = '你好福特'
        df_1.at[index, '主驾分贝'] = ""
        df_1.at[index, '副驾分贝'] = ""
        df_1.at[index, '车型'] = "cd542mca_hh"
        df_1.at[index, '噪声id'] = row['数据'].split('_')[1]
    df_1.to_excel(os.path.join(out_noise011_path, 'cd542hl_command_passenger_fail.xlsx'), index=False)

def replace_data_by_name(df1, df2, name_col='name'):
    """
    根据name列匹配两个DataFrame，用df2的数据替换df1中匹配到的数据
    
    参数:
        df1: 被替换的主DataFrame
        df2: 提供替换数据的DataFrame
        name_col: 用于匹配的列名（默认'name'）
    
    返回:
        替换后的DataFrame
    """
    # 创建df1的副本，避免修改原数据
    result = df1.copy()
    
    # 获取两个DataFrame共有的列（排除name列）
    common_cols = [col for col in df1.columns if col in df2.columns and col != name_col]
    
    if not common_cols:
        print("警告：两个DataFrame没有除name列外的共同列，无需替换")
        return result
    
    # 用df2的数据替换df1中匹配的行
    # 1. 先将df1和df2按name列合并
    merged = result.merge(df2[[name_col] + common_cols], on=name_col, how='left', suffixes=('', '_df2'))
    
    # 2. 对每列进行替换：如果df2中有值则用df2的值，否则保留df1原值
    for col in common_cols:
        result[col] = merged[f'{col}_df2'].fillna(merged[col])
    
    return result

def demo7():
    path_df_all = pd.read_excel(r'C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\U625L-1-1-0-R05\result_test.xlsx', sheet_name='指令词原始数据整合')
    path_df_fail = pd.read_excel(r'C:\pw\625lfail_driver\u625_VR性能自动化测试.xlsx', sheet_name='指令词原始数据整合')
    df = replace_data_by_name(path_df_all, path_df_fail, name_col='数据')
    df.to_excel(r'C:\Users\pengw\Desktop\HALO\语音识别唤醒结果\U625L-1-1-0-R05\sss.xlsx', index=False)

def move_audio_by_excel():
    df = pd.read_excel(r'C:\Users\pengw\Desktop\MixNoise\CD542HL_8DB\wakeup_fail\wakeup_passenger\cd542hl_command_passenger_fail.xlsx')
    for index,row in df.iterrows():
        name = row['文件名']
        src_path = os.path.join(r"C:\Users\pengw\Desktop\MixNoise\CD542HL_8DB\mix\command_passenger", name)
        dst_path = os.path.join(r"C:\Users\pengw\Desktop\MixNoise\CD542HL_8DB\wakeup_fail\wakeup_passenger", name)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            print(f"已复制: {name}")
        else:
            print(f"未找到文件: {name}")

if __name__ == "__main__":
    demo7()