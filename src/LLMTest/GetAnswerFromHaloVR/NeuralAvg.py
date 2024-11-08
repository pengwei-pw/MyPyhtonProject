import torch
import tensorflow as tf
import numpy as np
import time
import re
from sentence_transformers import SentenceTransformer, util
import pandas as ps
from simhash import Simhash
# def remove_punctuation(text):
#     # 匹配常见标点符号
#     pattern = r"[,.，。？！：；、‘’“”（）()《》]"
#     # 去除标点符号
#     cleaned_text = re.sub(pattern, '', text)
#     return cleaned_text
# model = SentenceTransformer('all-MiniLM-L6-v2')
# df = ps.read_excel(r"./语义相似度训练数据.xlsx", sheet_name="Sheet1")
# df["jaccard相似度计算值"] = ""
# # df["SimHash相似度"] = ""
# for index, row in df.iterrows():
#     sentence1 = remove_punctuation(row["text_a"])
#     sentence2 = remove_punctuation(row["text_b"])
    # print(index)
    # # 计算 SimHash 值
    # hash1 = Simhash(sentence1)
    # hash2 = Simhash(sentence2)
    # hamming_distance = hash1.distance(hash2)
    # similarity = (1 - hamming_distance / max(len(bin(hash1.value)), len(bin(hash2.value))))
    # df.at[index, "SimHash相似度"] = similarity
    # # 使用模型编码句子
    # embedding1 = model.encode(sentence1, convert_to_tensor=True)
    # embedding2 = model.encode(sentence2, convert_to_tensor=True)
    # # 计算余弦相似度
    # cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    # df.at[index, "sentence_transformers相似度计算值"] = cosine_similarity.item()
    #
    # df.at[index, "text_a"] = sentence1
    # df.at[index, "text_b"] = sentence2

#     set1 = set(sentence1)
#     set2 = set(sentence2)
#     jaccard_similarity = (len(set1 & set2) / len(set1 | set2))
#     print(f"Jaccard 相似度: {jaccard_similarity:.2f}")
#     df.at[index, "jaccard相似度计算值"] = jaccard_similarity
#
# df.to_excel(r"./语义相似度训练数据new.xlsx", index=False)


# 假设 TF-IDF 和 BERT 模型的输入特征为 1 维数据（实际数据可以更复杂）
# TF-IDF和BERT的特征维度可以根据实际情况调整
def deep_fusion_model(input_dim_tfidf, input_dim_bert):
    input_tfidf = tf.keras.layers.Input(shape=(input_dim_tfidf,))
    input_bert = tf.keras.layers.Input(shape=(input_dim_bert,))

    # 处理 TF-IDF 特征
    x_tfidf = tf.keras.layers.Dense(64, activation='relu')(input_tfidf)
    x_tfidf = tf.keras.layers.Dropout(0.2)(x_tfidf)

    # 处理 BERT 特征
    x_bert = tf.keras.layers.Dense(64, activation='relu')(input_bert)
    x_bert = tf.keras.layers.Dropout(0.2)(x_bert)

    # 融合两种特征
    combined = tf.keras.layers.Concatenate()([x_tfidf, x_bert])

    # 深度融合层
    x = tf.keras.layers.Dense(128, activation='relu')(combined)
    x = tf.keras.layers.Dropout(0.2)(x)

    # 输出层，预测相似度
    output = tf.keras.layers.Dense(1, activation='linear')(x)  # 线性激活，适合回归问题

    # 创建模型
    model = tf.keras.Model(inputs=[input_tfidf, input_bert], outputs=output)

    # 编译模型
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


df_train = ps.read_excel("./语义相似度训练数据.xlsx", sheet_name="Sheet1")
s_li = []
si_li = []
biao_li = []
for index, row in df_train.iterrows():
    s_li.append(row["sentence_transformers相似度计算值"])
    si_li.append(row["jaccard相似度计算值"])
    biao_li.append(row["label"])

s_li = np.array(s_li).reshape(-1, 1)
si_li = np.array(si_li).reshape(-1, 1)
biao_li = np.array(biao_li).reshape(-1, 1)
# # 假设我们有计算出的特征和标签
# # 示例：假设我们有两个输入特征（如 TF-IDF 和 BERT 相似度）以及对应的相似度标签
# X_tfidf = np.array([[0.7], [0.6], [0.8], [0.2], [0.3], [0.1]])  # TF-IDF相似度特征
# X_bert = np.array([[0.9], [0.8], [0.9], [0.71], [0.78], [0.5]])  # BERT相似度特征
# y = np.array([0.85, 0.7, 0.9, 0.1, 0.2, 0])  # 相似度标签
#
# # 训练和评估模型
model = deep_fusion_model(1, 1)  # 输入特征的维度分别为 1（实际特征维度可以更大）
model.fit([s_li, si_li], biao_li, epochs=10, batch_size=4)
#


df2 = ps.read_excel(r"./模型比较&语义相似度.xlsx", sheet_name="不同语义语料")
# # 预测新的句子对相似度
t_s_li = []
t_si_li = []
for index, row in df2.iterrows():
    t_s_li.append(row["sentence_transformers相似度计算值"])
    t_si_li.append(row["Jaccard相似度计算值"])
t_s_li = np.array(t_s_li).reshape(-1, 1)
t_si_li = np.array(t_si_li).reshape(-1, 1)



# X_tfidf_new = np.array([[0.2]])
# X_bert_new = np.array([[0.9]])
#

df2["biaozhu"] = ""

# # 使用训练好的模型进行预测
predicted_similarity = model.predict([t_s_li, t_si_li])
arr_re = np.array(predicted_similarity).ravel()

for i,data in enumerate(arr_re):
    df2.at[i, "biaozhu"] = data

df2.to_excel(r"./AI问答.xlsx", index=False)


# print("Predicted Similarity:", predicted_similarity[0][0])
