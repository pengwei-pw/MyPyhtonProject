#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :AudioStandardAutocorrelation.py
# @Time      :2024/10/18 23:21
# @Author    :pengweiaini123@163.com
import numpy as np
import matplotlib.pyplot as plt
import librosa  # 用于加载音频文件


def autocorrelation(x):
    """
    计算信号 x 的自相关函数

    Args:
        x: 输入信号，numpy 数组

    Returns:
        r: 自相关函数，numpy 数组
    """

    n = len(x)
    r = np.correlate(x, x, mode='full')[-n:]
    return r

# 加载音频文件
y, sr = librosa.load('./AudioPath/pulse_signal.wav')  # 替换为你的音频文件路径

# 计算自相关函数
result = autocorrelation(y)

# 绘制自相关函数图
plt.plot(result)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation Function')
plt.show()

