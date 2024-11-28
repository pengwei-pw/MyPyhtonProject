#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :calculationAf02.py
# @Time      :2024/11/28 09:49:38
# @Author    :PengWei


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



df = pd.read_excel(r"C:\Users\AutoTest_1\Desktop\LLM\LLM.xlsx", sheet_name = "Sheet2")
data_doubao_list = []
data_doubao_list.append(np.array(df["豆包.1"].tolist()))
data_doubao_list.append(np.array(df["豆包.2"].tolist()))
data_doubao_list.append(np.array(df["豆包.3"].tolist()))
data_doubao_list.append(np.array(df["豆包.4"].tolist()))
data_doubao_list.append(np.array(df["豆包"].tolist()))
print(df)
# 假设这三组数据是你要分析的
# data_1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# data_2 = np.array([1.1, 2.1, 3.1, 4.2, 5.1, 6.2, 7.1, 8.3, 9.0, 10.2])
# data_3 = np.array([0.9, 1.9, 2.8, 4.0, 5.0, 6.1, 7.0, 8.2, 8.9, 9.8])

# 将这些数据组合成一个二维数组（每行代表一组数据）
data = np.array(data_doubao_list)

plt.rcParams['font.family'] = 'SimHei'  # 设置为黑体，适用于中文显示
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 可视化：绘制每组数据的折线图
plt.figure(figsize=(10, 6))
for i, d in enumerate(data):
    plt.plot(d, label=f"数据组 {i+1}", marker='o', linestyle='-', markersize=6)

point_dict = dict()
for index, i1, i2, i3, i4, i5 in zip(np.arange(0,28), data_doubao_list[0], data_doubao_list[1], data_doubao_list[2], data_doubao_list[3], data_doubao_list[4]):
    point_dict[(index, i1)] = point_dict.get((index, i1), 0)+1 if point_dict.get((index, i1), 0)!=0 else 1
    point_dict[(index, i2)] = point_dict.get((index, i2), 0)+1 if point_dict.get((index, i2), 0)!=0 else 1
    point_dict[(index, i3)] = point_dict.get((index, i3), 0)+1 if point_dict.get((index, i3), 0)!=0 else 1
    point_dict[(index, i4)] = point_dict.get((index, i4), 0)+1 if point_dict.get((index, i4), 0)!=0 else 1
    point_dict[(index, i5)] = point_dict.get((index, i5), 0)+1 if point_dict.get((index, i5), 0)!=0 else 1
print(point_dict)
for key in point_dict.keys():
    plt.text(key[0], key[1], point_dict[key], fontsize=12, color='green', ha='center', va='bottom')

plt.title("豆包多组数据对比", fontsize=12)
plt.xlabel("数据点编号", fontsize=12)
plt.ylabel("打分值", fontsize=12, rotation = -45)
plt.xticks(np.arange(1, 28, 1))
plt.legend()
plt.grid(True)
plt.show()

# 计算每组数据的相关系数矩阵
correlation_matrix = np.corrcoef(data)
print("数据组之间的相关性矩阵：")
print(correlation_matrix)

# 可视化：绘制相关性热图
# plt.figure(figsize=(8, 6))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', xticklabels=['数据组1', '数据组2', '数据组3'], yticklabels=['数据组1', '数据组2', '数据组3'])
# plt.title("数据组之间的相关性", fontsize=16)
# plt.show()
