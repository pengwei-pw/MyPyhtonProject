import numpy as np
import matplotlib.pyplot as plt
import pandas as ps


df = ps.read_excel(r"./模型比较&语义相似度.xlsx", sheet_name="相同语义语料")
sentence_transformers_data = []
spacy_data = []
bert_data = []
Jaccard_data = []
SimHash_data = []
JaroWinkler_data = []
for index, row in df.iterrows():
    sentence_transformers_data.append(row["sentence_transformers相似度计算值"])
    spacy_data.append(row["spacy相似度计算值"])
    bert_data.append(row["BERT模型计算值"])
    Jaccard_data.append(row["Jaccard相似度计算值"])
    SimHash_data.append(row["SimHash相似度"])
    JaroWinkler_data.append(row["Jaro-Winkler相似度"])

print(sentence_transformers_data)
# 计算每组数据与1的差异（接近度）
distance_sentence_transformers_data = np.abs(np.array(sentence_transformers_data) - 1)
distance_spacy_data = np.abs(np.array(spacy_data) - 1)
distance_bert_data = np.abs(np.array(bert_data) - 1)
distance_Jaccard_data = np.abs(np.array(Jaccard_data) - 1)
distance_SimHash_data = np.abs(np.array(SimHash_data) - 1)
distance_JaroWinkler_data = np.abs(np.array(JaroWinkler_data) - 1)

# 计算两组数据的均值和标准差（用于后续比较）
mean_sentence_transformers = np.mean(distance_sentence_transformers_data)
mean_spacy_data = np.mean(distance_spacy_data)
mean_bert_data = np.mean(distance_bert_data)
mean_Jaccard_data = np.mean(distance_Jaccard_data)
mean_SimHash_data = np.mean(distance_SimHash_data)
mean_JaroWinkler_data = np.mean(distance_JaroWinkler_data)
# 创建一个图形
plt.figure(figsize=(10, 6))

# 绘制两组数据的直方图
plt.hist(distance_sentence_transformers_data, bins=20, alpha=0.8, label="sentence_transformers", color="red")
plt.hist(distance_spacy_data, bins=20, alpha=0.8, label="spacy_data", color="yellow")
plt.hist(distance_bert_data, bins=20, alpha=0.8, label="bert_data", color="blue")
plt.hist(distance_Jaccard_data, bins=20, alpha=0.8, label="Jaccard", color="green")
plt.hist(distance_SimHash_data, bins=20, alpha=0.8, label="SimHash", color="grey")
plt.hist(distance_JaroWinkler_data, bins=20, alpha=0.8, label="JaroWinkler", color="black")

# 绘制图表标题和标签
plt.title("Comparison of all Data Sets' Proximity to 1")
plt.xlabel("Distance from 1")
plt.ylabel("Frequency")

# 添加均值线
plt.axvline(x=mean_sentence_transformers, color="red", linestyle="dashed", linewidth=2, label=f"Mean Distance Data1: {mean_sentence_transformers:.2f}")
plt.axvline(x=mean_spacy_data, color="yellow", linestyle="dashed", linewidth=2, label=f"Mean Distance Data2: {mean_spacy_data:.2f}")
plt.axvline(x=mean_bert_data, color="blue", linestyle="dashed", linewidth=2, label=f"Mean Distance Data3: {mean_bert_data:.2f}")
plt.axvline(x=mean_Jaccard_data, color="green", linestyle="dashed", linewidth=2, label=f"Mean Jaccard Data4: {mean_Jaccard_data:.2f}")
plt.axvline(x=mean_SimHash_data, color="grey", linestyle="dashed", linewidth=2, label=f"Mean SimHash Data5: {mean_SimHash_data:.2f}")
plt.axvline(x=mean_JaroWinkler_data, color="black", linestyle="dashed", linewidth=2, label=f"Mean JaroWinkler Data6: {mean_JaroWinkler_data:.2f}")
# 添加图例
plt.legend()

# 显示图形
plt.show()

# 输出均值比较
# if mean1 < mean2:
#     print("Data1 is closer to 1 on average.")
# else:
#     print("Data2 is closer to 1 on average.")
