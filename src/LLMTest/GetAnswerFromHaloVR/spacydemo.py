import spacy
import pandas as ps
import time

start_time = time.time()
nlp_zh = spacy.load("zh_core_web_sm")
df = ps.read_excel(r"./AI问答-1012-2轮case.xlsx", sheet_name="泛化语义")
# 定义要比较的两个句子
# sentence1 = "我对红瓤西瓜情有独钟，喜欢吃它"
# sentence2 = "我喜欢吃红瓤西瓜"
df["spacy相似度计算值"] = ""
for index, row in df.iterrows():
    sentence1_zh = row["泛化语句"]
    sentence2_zh = row["原语句"]
    doc1_zh = nlp_zh(sentence1_zh)
    doc2_zh = nlp_zh(sentence2_zh)
    similarity_score_zh = doc1_zh.similarity(doc2_zh)
    # 计算余弦相似度
    print(f"中文语义相似度为: {similarity_score_zh}")
    df.at[index, "spacy相似度计算值"] = similarity_score_zh
end_time = time.time()
print(f"执行时间：{end_time-start_time}")
df.to_excel(r"./AI问答.xlsx", index=False)








