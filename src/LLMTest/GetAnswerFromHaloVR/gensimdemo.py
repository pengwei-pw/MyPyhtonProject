import numpy as np
import gensim
from gensim.models import KeyedVectors
import jieba
import gensim.downloader as api
# model = api.load("word2vec-google-news-300")

# 加载预训练的 Word2Vec 模型（例如 Google 的模型）
# 请确保你下载了模型并提供正确的路径
# model = KeyedVectors.load_word2vec_format('path/to/GoogleNews-vectors-negative300.bin', binary=True)

# 这里我们用一个示例模型代替，实际应用中请使用真实的模型
model_path = 'cn.cbow.bin'  # 替换为你的模型路径
model = KeyedVectors.load_word2vec_format(model_path, binary=True,encoding="latin1")

import numpy as np

print(model.index_to_key[:10])

# 使用jieba进行分词
def tokenize(sentence):
    return list(jieba.cut(sentence))



# 计算句子向量
def sentence_vector(sentence):
    words = tokenize(sentence)
    vectors = []

    for word in words:
        if word in model:
            vectors.append(model[word])

    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return None


# 计算相似度
def similarity(sentence1, sentence2):
    vec1 = sentence_vector(sentence1)
    vec2 = sentence_vector(sentence2)

    if vec1 is not None and vec2 is not None:
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    else:
        return None


# 示例
sentence1 = "i hat cat"
sentence2 = "i like cat"

sim = similarity(sentence1, sentence2)
print(f"相似度: {sim}")

