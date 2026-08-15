#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Training03.py
# @Time      :2025/07/22 09:31:57
# @Author    :PengWei

import soundfile as sf
import numpy as np

def calculate_db(audio_path):
    """
    计算音频文件的分贝值（dB SPL）
    
    参数:
        audio_path: 音频文件路径（支持wav、flac等格式）
    
    返回:
        db_value: 分贝值
    """
    # 读取音频文件
    data, samplerate = sf.read(audio_path)
    
    # 处理多声道（取平均值）
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    
    # 计算RMS（均方根）
    rms = np.sqrt(np.mean(np.square(data)))
    
    # 避免除以零错误（静音情况）
    if rms == 0:
        return -np.inf  # 负无穷大表示静音
    
    # 转换为分贝（参考值为20e-6 Pa，即20μPa）
    # 注意：音频数据通常已归一化到[-1,1]，这里假设满量程对应1Pa
    db_value = 20 * np.log10(rms / 20e-6)
    
    return db_value
import os

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_list_distribution(data_list, title="数据分布可视化"):
    """
    可视化列表数据的分布情况，包括直方图、核密度图和箱线图
    
    参数:
        data_list: 待可视化的列表数据
        title: 图表标题
    """
    # 设置中文字体，确保中文正常显示
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    sns.set(font_scale=1.2)
    
    # 创建画布和子图
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(title, fontsize=16)
    
    # 1. 直方图（显示数据分布频率）
    sns.histplot(data=data_list, kde=True, ax=axes[0], bins=15)
    axes[0].set_title("直方图（带核密度曲线）")
    axes[0].set_xlabel("数值")
    axes[0].set_ylabel("频率")
    
    # 2. 核密度图（更平滑的分布曲线）
    sns.kdeplot(data=data_list, fill=True, ax=axes[1])
    axes[1].set_title("核密度图")
    axes[1].set_xlabel("数值")
    axes[1].set_ylabel("密度")
    
    # 3. 箱线图（显示数据的四分位数、异常值）
    sns.boxplot(data=data_list, ax=axes[2])
    axes[2].set_title("箱线图")
    axes[2].set_xlabel("数据")
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # 调整布局，避免标题重叠
    plt.show()

def min_rms():
    """
    Calculate the minimum RMS value from a set of audio files.
    """
    audio_path = r'C:\Users\pengw\Desktop\Recording\command_5092'
    audio_files = [f for f in os.listdir(audio_path) if f.endswith('.wav')]
    min_rms_value = float('inf')
    list_db = []
    for audio_file in audio_files:
        file_path = os.path.join(audio_path, audio_file)
        rms_value = calculate_db(file_path)
        list_db.append(rms_value)
        if rms_value < min_rms_value:
            min_rms_value = rms_value
            name = audio_file
        list_db.append(min_rms_value)
    plot_list_distribution(list_db, title="RMS值分布可视化")
    print(f"Minimum RMS value: {min_rms_value} from file: {name}")
    
    return min_rms_value

if __name__ == "__main__":
    min_rms()