# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import re

# def replace_numbers(text, replacement="*"):
#     # 匹配中文数字和阿拉伯数字
#     pattern = r"[零一二三四五六七八九十百千万0-9]+"
#     # 替换数字为指定字符
#     replaced_text = re.sub(pattern, replacement, text)
#     return replaced_text

# def remove_punctuation(text):
#     # 匹配常见标点符号
#     pattern = r"[,.，。？！：；、‘’“”（）()《》]"
#     # 去除标点符号
#     cleaned_text = re.sub(pattern, '', text)
#     return cleaned_text
#
# def text_replace(text, replacement="*"):
#     replaced_text = replace_numbers(text)
#     txt = remove_punctuation(replaced_text)
#     return txt

# text1 = "全程十一公里大约需要一万五千零十七分钟，三百二十一米后右转"
# text2 = '全程12公里，大约需要28分钟,100米后右转'

# text1 = "当前网络异常，请先为我联网吧，我先退下了！"
# text2 = "当前网络异常请先问我联网吧我先退下了"

# text1 = text_replace(text1)
# text2 = text_replace(text2)
# print(text1)
# print(text2)

# text1 = '我热爱学习'
# text2 = '我喜欢学习'

import textdistance
from simhash import Simhash
import pandas as ps
# 将每个文本的词汇放入集合中
df = ps.read_excel(r"./模型比较&语义相似度.xlsx", sheet_name="相同语义泛化语料")
# 定义要比较的两个句子
# sentence1 = "我对红瓤西瓜情有独钟，喜欢吃它"
# sentence2 = "我喜欢吃红瓤西瓜"
df["Jaccard相似度计算值"] = ""
df["SimHash相似度"] = ""
df["Jaro-Winkler相似度"] = ""
for index, row in df.iterrows():
    sentence1_zh = row["泛化语句"]
    sentence2_zh = row["原语句"]
    set1 = set(sentence1_zh)
    set2 = set(sentence2_zh)
    jaccard_similarity = (len(set1 & set2) / len(set1 | set2))
    print(f"Jaccard 相似度: {jaccard_similarity:.2f}")
    df.at[index, "Jaccard相似度计算值"] = jaccard_similarity

    # 计算 SimHash 值
    hash1 = Simhash(sentence1_zh)
    hash2 = Simhash(sentence2_zh)
    hamming_distance = hash1.distance(hash2)
    similarity = (1 - hamming_distance / max(len(bin(hash1.value)), len(bin(hash2.value))))
    df.at[index, "SimHash相似度"] = similarity
    print(f"SimHash 相似度: {similarity:.2f}")


    # 计算 Jaro-Winkler 相似度
    def jaro_winkler_similarity(sentence1_zh, sentence2_zh):
        return textdistance.jaro_winkler(sentence1_zh, sentence2_zh)
    # 计算相似度
    similarity_score = jaro_winkler_similarity(sentence1_zh, sentence2_zh)
    df.at[index, "Jaro-Winkler相似度"] = similarity_score
    print(f"Jaro-Winkler相似度: {similarity_score:.2f}")

df.to_excel(r"./AI问答.xlsx", index=False)



# 计算 Jaccard 相似度
# jaccard_similarity = (len(set1 & set2) / len(set1 | set2)) * 100
# print(f"Jaccard 相似度: {jaccard_similarity:.2f}")


# from simhash import Simhash


# 计算汉明距离并转换为相似度
# hamming_distance = hash1.distance(hash2)
# similarity = (1 - hamming_distance / max(len(bin(hash1.value)), len(bin(hash2.value)))) * 100
# print(f"SimHash 相似度: {similarity:.2f}")
#
#
# import Levenshtein
# # 计算编辑距离
# edit_distance = Levenshtein.distance(text1, text2)
#
# # 将编辑距离转换为相似度得分
# # 相似度 = 1 - (编辑距离 / 两个文本中较长的文本长度)
# similarity = (1 - (edit_distance / max(len(text1), len(text2)))) * 100
# print(f"编辑距离 相似度: {similarity:.2f}")
#
#
# from sklearn.feature_extraction.text import CountVectorizer
#
#
# # 定义 N-gram 参数
# N = 2  # 使用 2-gram，即每两个字符组成一个子序列
#
# # 使用 CountVectorizer 生成 N-gram 序列
# vectorizer = CountVectorizer(analyzer='char', ngram_range=(N, N))
# ngrams = vectorizer.fit_transform([text1, text2])
#
# # 计算两个文本 N-gram 的重叠比例
# intersection = (ngrams[0].toarray() & ngrams[1].toarray()).sum()
# union = (ngrams[0].toarray() | ngrams[1].toarray()).sum()
# similarity = (intersection / union if union != 0 else 0) * 100
#
# print(f"重叠比例 相似度: {similarity:.2f}")
#
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import jieba
#
#
#
# # 使用 TF-IDF 向量化
# def compute_tfidf_similarity(text1, text2):
#     # 分词
#     documents = [" ".join(jieba.cut(text1)), " ".join(jieba.cut(text2))]
#
#     # 创建 TF-IDF 向量化器
#     vectorizer = TfidfVectorizer()
#
#     # 计算 TF-IDF 矩阵
#     tfidf_matrix = vectorizer.fit_transform(documents)
#
#     # 计算余弦相似度
#     similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
#     return similarity[0][0]
#
#
# # 计算相似度
# similarity_score = compute_tfidf_similarity(text1, text2) * 100
# print(f"TF-IDF 向量化 相似度: {similarity_score:.2f}")
#
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import pairwise_distances
# import numpy as np
# import jieba
#
#
# # 使用 TF-IDF 向量化
# def compute_tfidf(text1, text2):
#     documents = [" ".join(jieba.cut(text1)), " ".join(jieba.cut(text2))]
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(documents)
#     return tfidf_matrix
#
#
# # 汉明距离计算
# def hamming_distance(str1, str2):
#     # 确保长度相同
#     if len(str1) != len(str2):
#         max_len = max(len(str1), len(str2))
#         str1 = str1.ljust(max_len)  # 用空格填充
#         str2 = str2.ljust(max_len)
#
#     distance = sum(el1 != el2 for el1, el2 in zip(str1, str2))
#     return distance
#
#
# # 综合相似度计算
# def combined_similarity(text1, text2):
#     tfidf_matrix = compute_tfidf(text1, text2)
#
#     # 计算余弦相似度
#     cosine_sim = 1 - pairwise_distances(tfidf_matrix, metric='cosine')[0][1]
#
#     # 计算汉明距离相似度
#     distance = hamming_distance(text1, text2)
#     hamming_sim = 1 - (distance / max(len(text1), len(text2)))  # 归一化
#
#     # 计算综合相似度
#     combined_sim = (cosine_sim + hamming_sim) / 2
#     return combined_sim
#
#
# # 计算相似度
# similarity_score = combined_similarity(text1, text2) * 100
# print(f"余弦+汉明距离 综合相似度: {similarity_score:.2f}")
#
#
# import jieba
# import numpy as np
# from nltk.metrics import edit_distance
#
#
# # Jaccard相似度计算
# def jaccard_similarity(text1, text2):
#     # 分词并创建集合
#     set1 = set(jieba.cut(text1))
#     set2 = set(jieba.cut(text2))
#
#     intersection = len(set1.intersection(set2))
#     union = len(set1.union(set2))
#
#     return intersection / union if union != 0 else 0
#
#
# # 编辑距离相似度计算
# def levenshtein_similarity(text1, text2):
#     distance = edit_distance(text1, text2)
#     max_len = max(len(text1), len(text2))
#     return 1 - distance / max_len if max_len != 0 else 0
#
#
# # 综合相似度计算
# def combined_similarity(text1, text2):
#     jaccard_sim = jaccard_similarity(text1, text2)
#     levenshtein_sim = levenshtein_similarity(text1, text2)
#
#     # 取平均
#     return (jaccard_sim + levenshtein_sim) / 2
#
#
# # 计算相似度
# similarity_score = combined_similarity(text1, text2) * 100
# print(f"Jaccard+编辑距离 综合相似度: {similarity_score:.2f}")
#
#
#
#
# import jieba
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
#
# # 分词并创建 TF-IDF 向量
# def compute_tfidf(text1, text2):
#     # 分词
#     documents = [" ".join(jieba.cut(text1)), " ".join(jieba.cut(text2))]
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(documents)
#     return tfidf_matrix
#
# # 计算相似度
# def calculate_similarity(text1, text2):
#     tfidf_matrix = compute_tfidf(text1, text2)
#     sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
#     return sim[0][0]
#
# # 计算相似度
# similarity_score = calculate_similarity(text1, text2) * 100
# print(f"TF-IDF + 余弦 相似度: {similarity_score:.2f}")
#
#
# from difflib import SequenceMatcher
# similarity_score = (SequenceMatcher(None, text1, text2).ratio()) * 100
# print(f'difflib 文本相似度: {similarity_score:.2f}')
#
#
# import jieba
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
#
# # 计算 Bag of Words 向量
# def compute_bow(text1, text2):
#     # 分词
#     documents = [" ".join(jieba.cut(text1)), " ".join(jieba.cut(text2))]
#     vectorizer = CountVectorizer()
#     bow_matrix = vectorizer.fit_transform(documents)
#     return bow_matrix
#
# # 计算相似度
# def calculate_similarity(text1, text2):
#     bow_matrix = compute_bow(text1, text2)
#     sim = cosine_similarity(bow_matrix[0:1], bow_matrix[1:2])
#     return sim[0][0]
#
# # 计算相似度
# similarity_score = calculate_similarity(text1, text2) * 100
# print(f"Bag of Words + 余弦  相似度: {similarity_score:.2f}")
#
#
# import jieba
# import numpy as np
# from gensim.models import Word2Vec
# from sklearn.metrics.pairwise import cosine_similarity
#
# # 分词
# def tokenize(text):
#     return list(jieba.cut(text))
#
# # 准备语料库
# corpus = [tokenize(text1), tokenize(text2)]
#
# # 训练 Word2Vec 模型
# model = Word2Vec(corpus, vector_size=100, window=5, min_count=1, sg=0)
#
# # 计算文本向量
# def get_text_vector(text):
#     words = tokenize(text)
#     # 获取每个词的向量并取平均
#     word_vectors = [model.wv[word] for word in words if word in model.wv]
#     return np.mean(word_vectors, axis=0) if word_vectors else np.zeros(model.vector_size)
#
# # 计算相似度
# def calculate_similarity(text1, text2):
#     vec1 = get_text_vector(text1)
#     vec2 = get_text_vector(text2)
#     return cosine_similarity([vec1], [vec2])[0][0]
#
# # 计算相似度
# similarity_score = calculate_similarity(text1, text2) * 100
# print(f"Word2Vec + 余弦  相似度: {similarity_score:.2f}")
#
# import jieba
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
#
# # Jaccard相似度计算
# def jaccard_similarity(text1, text2):
#     # 分词并创建集合
#     set1 = set(jieba.cut(text1))
#     set2 = set(jieba.cut(text2))
#
#     intersection = len(set1.intersection(set2))
#     union = len(set1.union(set2))
#
#     return intersection / union if union != 0 else 0
#
#
# # TF-IDF 向量计算
# def compute_tfidf(text1, text2):
#     documents = [" ".join(jieba.cut(text1)), " ".join(jieba.cut(text2))]
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(documents)
#     return tfidf_matrix.toarray()
#
#
# # 计算综合相似度
# def combined_similarity(text1, text2):
#     jaccard_sim = jaccard_similarity(text1, text2)
#
#     tfidf_matrix = compute_tfidf(text1, text2)
#     tfidf_sim = np.dot(tfidf_matrix[0], tfidf_matrix[1]) / (
#                 np.linalg.norm(tfidf_matrix[0]) * np.linalg.norm(tfidf_matrix[1]))
#
#     # 取平均
#     return (jaccard_sim + tfidf_sim) / 2
#
# # 计算相似度
# similarity_score = combined_similarity(text1, text2) * 100
# print(f"TF-IDF + Jaccard  综合相似度: {similarity_score:.2f}")
#
# import jieba
# import Levenshtein as lev
#
# # 计算编辑距离
# def levenshtein_similarity(text1, text2):
#     # 使用 jieba 分词
#     words1 = list(jieba.cut(text1))
#     words2 = list(jieba.cut(text2))
#
#     # 将分词后的结果拼接成字符串
#     str1 = ''.join(words1)
#     str2 = ''.join(words2)
#
#     # 计算编辑距离
#     distance = lev.distance(str1, str2)
#     max_len = max(len(str1), len(str2))
#
#     # 计算相似度
#     similarity = 1 - (distance / max_len) if max_len > 0 else 0
#     return similarity
#
# # 计算相似度
# similarity_score = levenshtein_similarity(text1, text2) * 100
# print(f"Levenshtein Distance 相似度: {similarity_score:.2f}")
#
# import jieba
# import numpy as np
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# # N-grams 向量计算
# def ngrams_vectorize(text1, text2, n=2):
#     # 使用 jieba 分词
#     words1 = ' '.join(jieba.cut(text1))
#     words2 = ' '.join(jieba.cut(text2))
#
#     documents = [words1, words2]
#
#     # 创建 N-grams 向量
#     vectorizer = CountVectorizer(ngram_range=(n, n))
#     ngrams_matrix = vectorizer.fit_transform(documents)
#     return ngrams_matrix.toarray()
#
#
# # 计算相似度
# def calculate_similarity(text1, text2):
#     ngrams_matrix = ngrams_vectorize(text1, text2)
#     return cosine_similarity(ngrams_matrix)[0][1]  # 返回两个文本的相似度
#
# # 计算相似度
# similarity_score = calculate_similarity(text1, text2) * 100
# print(f"N-grams + 余弦  相似度: {similarity_score:.2f}")
#
#
# import textdistance
# #
# #
# # 计算 Jaro-Winkler 相似度
# def jaro_winkler_similarity(text1, text2):
#     return textdistance.jaro_winkler(text1, text2)
#
#
# # 计算相似度
# similarity_score = jaro_winkler_similarity(text1, text2) * 100
# print(f"Jaro-Winkler 相似度: {similarity_score:.2f}")

# from collections import Counter
# from sklearn.metrics import jaccard_score
# import jieba
#
# # 定义 n-gram 切分函数
# def ngrams(text, n=3):
#     text = ''.join(jieba.cut(text))  # 使用 jieba 进行分词后连接
#     return [text[i:i + n] for i in range(len(text) - n + 1)]
#
#
# # 计算 n-gram 重叠相似度
# def ngram_similarity(text1, text2, n=3):
#     ngrams1 = Counter(ngrams(text1, n))
#     ngrams2 = Counter(ngrams(text2, n))
#
#     # 取交集
#     intersection = sum((ngrams1 & ngrams2).values())
#     union = sum((ngrams1 | ngrams2).values())
#
#     # 相似度
#     return intersection / union if union > 0 else 0
#
# # 计算相似度
# similarity_score = ngram_similarity(text1, text2) * 100
# print(f"n-gram 重叠相似度: {similarity_score:.2f}")
#
# from simhash import Simhash
#
# # 计算 SimHash 哈希值
# def calculate_simhash(text):
#     return Simhash(text)
#
# # 计算汉明距离
# def hamming_distance(hash1, hash2):
#     return hash1.distance(hash2)
#
#
# # 计算 SimHash 和汉明距离
# hash1 = calculate_simhash(text1)
# hash2 = calculate_simhash(text2)
# distance = hamming_distance(hash1, hash2)
#
# # 将汉明距离转换为相似度（0 到 1）
# similarity_score = (1 - distance / 64) * 100  # SimHash 的默认长度为 64 位
# print(f"SimHash+汉明 相似度: {similarity_score:.2f}")






