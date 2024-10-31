import os
import pandas as pd

if "__main__" == __name__:


    # 读取表格A和表格B
    df_a = pd.read_excel(r"C:\Users\AutoTest_1\Desktop\bug temp\Ford Jira Cloud_new.xlsx")
    df_b = pd.read_excel(r"C:\Users\AutoTest_1\Desktop\bug temp\Ford Jira Cloud (14).xlsx")

    # 在表格A中添加一列用于存储结果，初始值为空字符串
    df_a["结果"] = ""

    # 遍历表格A的每一行
    for index, row in df_a.iterrows():
        # 获取当前行的issue key值
        issue_key = row["Issue key"]
        # print(issue_key)
        # 在表格B中查找匹配的issue key值
        matching_row = df_b[df_b["Issue key"] == issue_key]
        # print(matching_row)
        # 如果找到了匹配的行
        if not matching_row.empty:
            # 将表格B中除issue key以外的所有列的值拼接成一个字符串
            values_str = ' '.join(matching_row.drop("Issue key", axis=1).astype(str).values.flatten())
            # print(values_str)
            # 检查字符串中是否包含611或625
            if values_str.__contains__("611"):
                # 将611或625写入表格A对应行的结果列
                df_a.loc[index, "结果"] = "611"
            elif values_str.__contains__("625"):
                df_a.loc[index, "结果"] = "625"
            elif values_str.__contains__("707"):
                df_a.loc[index, "结果"] = "707"
            elif values_str.__contains__("718"):
                df_a.loc[index, "结果"] = "718"
    # 保存结果到新的Excel文件
    df_a.to_excel(r"C:\Users\AutoTest_1\Desktop\bug temp\jira APIMCIM.xlsx", index=False)

