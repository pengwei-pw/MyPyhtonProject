import numpy as np
import matplotlib.pyplot as plt
import pandas as ps


df = ps.read_excel(r"./AI问答-1012-2轮case.xlsx", sheet_name="泛化语义")
sentence_transformers_data = []
spacy_data = []
bert_data = []
for index, row in df.iterrows():
    sentence_transformers_data.append(row["sentence_transformers相似度计算值"])
    spacy_data.append(row["spacy相似度计算值"])
    bert_data.append(row["BERT模型计算值"])
print(sentence_transformers_data)
# 计算每组数据与1的差异（接近度）
distance_sentence_transformers = np.abs(np.array(sentence_transformers_data) - 1)
distance_spacy_data = np.abs(np.array(spacy_data) - 1)
distance_bert_data = np.abs(np.array(bert_data) - 1)

# 计算两组数据的均值和标准差（用于后续比较）
mean_sentence_transformers = np.mean(distance_sentence_transformers)
mean_spacy_data = np.mean(distance_spacy_data)
mean_bert_data = np.mean(distance_bert_data)
print(f"标准差: {np.std(distance_sentence_transformers)}")
print(f"标准差: {np.std(distance_spacy_data)}")
print(f"标准差: {np.std(distance_bert_data)}")
print()
print(f"方差: {np.var(distance_sentence_transformers)}")
print(f"方差: {np.var(distance_spacy_data)}")
print(f"方差: {np.var(distance_bert_data)}")
# 创建一个图形
plt.figure(figsize=(10, 6))

# 绘制两组数据的直方图
plt.hist(distance_sentence_transformers, bins=20, alpha=0.8, label="sentence_transformers", color="red")
plt.hist(distance_spacy_data, bins=20, alpha=0.8, label="spacy_data", color="yellow")
plt.hist(distance_bert_data, bins=20, alpha=0.8, label="bert_data", color="blue")

# 绘制图表标题和标签
plt.title("Comparison of three Data Sets' Proximity to 1")
plt.xlabel("Distance from 1")
plt.ylabel("Frequency")

# 添加均值线
plt.axvline(x=mean_sentence_transformers, color="red", linestyle="dashed", linewidth=2, label=f"Mean Distance Data1: {mean_sentence_transformers:.2f}")
plt.axvline(x=mean_spacy_data, color="yellow", linestyle="dashed", linewidth=2, label=f"Mean Distance Data2: {mean_spacy_data:.2f}")
plt.axvline(x=mean_bert_data, color="blue", linestyle="dashed", linewidth=2, label=f"Mean Distance Data3: {mean_bert_data:.2f}")

# 添加图例
plt.legend()

# 显示图形
plt.show()

# 输出均值比较
# if mean1 < mean2:
#     print("Data1 is closer to 1 on average.")
# else:
#     print("Data2 is closer to 1 on average.")
