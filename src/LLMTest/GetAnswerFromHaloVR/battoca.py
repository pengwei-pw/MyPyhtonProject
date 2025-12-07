import time
from sentence_transformersdemo import SentenceTransformer, util
import pandas as ps

# 初始化模型
start_time = time.time()
model = SentenceTransformer('all-MiniLM-L6-v2')
#加载表格
df = ps.read_excel(r"./AI问答-1012-2轮case.xlsx", sheet_name="泛化语义")
# 定义要比较的两个句子
# sentence1 = "我对红瓤西瓜情有独钟，喜欢吃它"
# sentence2 = "我喜欢吃红瓤西瓜"
df["sentence_transformers相似度计算值"] = ""
for index, row in df.iterrows():
    sentence1 = row["泛化语句"]
    sentence2 = row["原语句"]
    # 使用模型编码句子
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    # 计算余弦相似度
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    df.at[index, "sentence_transformers相似度计算值"] = cosine_similarity.item()
    print(f"语义相似度: {cosine_similarity.item():.4f}")
end_time = time.time()
print(f"执行时间：{end_time-start_time}")
df.to_excel(r"./AI问答.xlsx", index=False)