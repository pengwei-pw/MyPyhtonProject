#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :calculationAdf.py
# @Time      :2024/11/27 17:06:54
# @Author    :PengWei

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf

df = pd.read_excel(r"C:\Users\AutoTest_1\Desktop\LLM\LLM.xlsx", sheet_name = "Sheet2")

for index, row in df.iterrows():

    print(row["豆包.1"], row["豆包.2"])

# 设置图形样式
sns.set(style="whitegrid")

# 示例数据：这里你可以换成你的数据
data = {
    "data_1": np.random.randn(100).cumsum(),  # 随机游走数据，非平稳
    "data_2": np.sin(np.linspace(0, 10, 100)) + np.random.randn(100) * 0.5,  # 具有趋势的平稳数据
    "data_3": np.random.randn(100),  # 正态分布数据，平稳
}
print(data)
# ADF检验函数
def adf_test(series):
    result = adfuller(series)
    return result[1]  # 返回p值

# 创建图形
fig, axes = plt.subplots(3, 2, figsize=(10, 12))

for idx, (name, series) in enumerate(data.items()):
    ax1, ax2 = axes[idx]
    
    # 绘制时间序列图
    ax1.plot(series)
    ax1.set_title(f"时间序列图: {name}")
    
    # ADF检验
    p_value = adf_test(series)
    ax1.set_xlabel(f"ADF检验p值: {p_value:.4f}")
    
    # 绘制自相关图
    plot_acf(series, ax=ax2)
    ax2.set_title(f"自相关图: {name}")

# 调整布局
plt.tight_layout()
plt.show()

# 输出各组数据的ADF检验结果
for name, series in data.items():
    p_value = adf_test(series)
    print(f"{name} - ADF检验 p值: {p_value:.4f}")
    if p_value < 0.05:
        print(f"{name} 是平稳的")
    else:
        print(f"{name} 不是平稳的")
