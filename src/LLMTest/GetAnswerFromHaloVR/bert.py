from transformers import BertTokenizer, BertModel
import torch
# pip install -u huggingface_hub
# huggingface-cli download bert-base-chinese
#numpy==1.22.0
import pandas as ps
from scipy.spatial.distance import cosine
import time

# 加载BERT模型和分词器
start_time = time.time()
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')
# 假设的句子
df = ps.read_excel(r"./AI问答-1012-2轮case.xlsx", sheet_name="泛化语义")
# 定义要比较的两个句子
# sentence1 = "我对红瓤西瓜情有独钟，喜欢吃它"
# sentence2 = "我喜欢吃红瓤西瓜"
df["BERT模型计算值"] = ""
for index, row in df.iterrows():
    sentence1 = row["泛化语句"]
    sentence2 = row["原语句"]
    # 使用模型编码句子
    inputs1 = tokenizer(sentence1, return_tensors="pt")
    inputs2 = tokenizer(sentence2, return_tensors="pt")
    # 计算余弦相似度
    with torch.no_grad():
        output1 = model(**inputs1)
        output2 = model(**inputs2)
        vector1 = output1.last_hidden_state.mean(dim=1).squeeze()
        vector2 = output2.last_hidden_state.mean(dim=1).squeeze()
    similarity = 1 - cosine(vector1, vector2)
    print("语义相似度:", similarity)
    df.at[index, "BERT模型计算值"] = similarity
end_time = time.time()
print(f"执行时间：{end_time-start_time}")
df.to_excel(r"./AI问答.xlsx", index=False)


sentence1 = "我喜欢读书"
sentence2 = "我热爱阅读"
# 对句子进行编码

# 获取句子的向量表示

# 计算向量相似度（这里使用余弦相似度）

