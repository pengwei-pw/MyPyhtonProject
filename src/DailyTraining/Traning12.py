#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Traning12.py
# @Time      :2025/12/26 14:18:39
# @Author    :PengWei
import pandas as pd

if __name__ == "__main__":
    # a_path和A 是test case 表格,B表是test run，c是自动化自己维护的表，保证3张表sheet名字一样
    a_path = r'C:\Users\pengw\Desktop\test_py\Test_case_1225.xlsx'
    b_path = r'C:\Users\pengw\Desktop\test_py\CX483ICA2_2.0.0_FocusTest_11.21.xlsx'
    c_path = r'C:\Users\pengw\Desktop\test_py\483testrun.xlsx'

    # 使用ExcelFile对象读取Excel文件，这样可以查看所有sheet的名字
    xls = pd.ExcelFile(a_path)

    # 获取所有sheet的名称
    sheet_names = xls.sheet_names
    print(f"所有sheet页名称: {sheet_names}")

    # 初始化一个字典，用来保存每个sheet处理后的数据
    processed_sheets = {}

    # 遍历每个sheet页进行处理
    for sheet in sheet_names:
        try:
            # 读取A表：保留所有列
            A = pd.read_excel(a_path, sheet_name=sheet)
            B = pd.read_excel(b_path, sheet_name=sheet)
            C = pd.read_excel(c_path, sheet_name=sheet)

            # 清理列名，去除空格，并统一列名大小写
            A.columns = A.columns.str.strip()
            B.columns = B.columns.str.strip()
            C.columns = C.columns.str.strip()

            # 确保 ID 列存在
            if 'ID' not in A.columns:
                raise ValueError(f"A表 {sheet} 中没有 'ID' 列")
            if 'ID' not in B.columns:
                raise ValueError(f"B表 {sheet} 中没有 'ID' 列")
            if 'Case ID' not in C.columns:
                raise ValueError(f"C表 {sheet} 中没有 'Case ID' 列")

            # 打印 A 和 B 表的 ID 列，帮助调试
            print(f"A表 {sheet} 的 ID 列: \n", A['ID'].head())
            print(f"B表 {sheet} 的 ID 列: \n", B['ID'].head())
            print(f"C表 {sheet} 的列名：", C.columns)
            print(C['Case ID'])
            if 'Case ID' not in C.columns:
                raise ValueError(f"C表 {sheet} 中没有 'Case ID' 列")

            # 确保 ID 列的数据类型一致，转换为字符串类型
            A['ID'] = A['ID'].astype(str)
            B['ID'] = B['ID'].astype(str)
            C['Case ID'] = C['Case ID'].astype(str)
            C['ID'] = C['ID'].astype(str)

            # 获取B表和C表的列名称，判断是否存在需要的列
            B_columns_needed = ['Automation_Y', '分类/依赖', '责任人-483', '责任人-542', 'Comments', 'Script Name', '是否开发', '不能开发原因']
            C_columns_needed = ['Case ID', 'ID']  # 只需要C表中的ID列

            # 读取B表，如果存在所需列
            B_cols = [col for col in B_columns_needed if col in B.columns]
            B = B[B_cols + ['ID']]  # 显式选择所需列，并保留 'ID' 列

            # 读取C表，如果存在所需列
            C_cols = [col for col in C_columns_needed if col in C.columns]
            # C = C[C_cols + ['ID']]  # 显式选择所需列，并保留 'ID' 列
            C = C[C_cols]  # 显式选择所需列，并保留 'ID' 列

            # 读取C表，如果存在所需列
            # C_cols = [col for col in C_columns_needed if col in C.columns]
            # C = C[C_cols] if not C.empty else pd.DataFrame()

            # 通过ID列将A表和B表合并，A表保留所有数据，B表合并指定的列
            if not B.empty:
                A = A.merge(B, on='ID', how='left')  # 合并时保留 A 表所有列

            # 通过ID列将A表和C表合并，A表保留所有数据，C表合并指定的列
            if not C.empty:
                C = C.rename(columns={'ID': 'TestRun ID'})  # 重命名 C 表中的 ID 列
                A = A.merge(C, left_on='ID', right_on='Case ID', how='left')

            # 将处理后的结果保存到字典中
            A['自动化是否测试'] = A.apply(
                lambda row: '是' if pd.notna(row['TestRun ID']) and row['Automation'] == ' Completed' else '',
                axis=1
            )
            A['Automation_Y'] = A.apply(
                lambda row: 'Y' if row['Automation'] == ' Completed' else '',
                axis=1
            )
            processed_sheets[sheet] = A

            print(f"处理后的sheet页 {sheet}:\n", A.head())

        except Exception as e:
            print(f"处理sheet {sheet} 时出现错误: {e}")

    # 如果需要保存修改后的Excel文件，可以使用以下代码：
    try:
        with pd.ExcelWriter(r'C:\Users\pengw\Desktop\test_py\processed_file.xlsx') as writer:
            for sheet, df in processed_sheets.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        print("处理后的文件已保存为 'processed_file.xlsx'")
    except Exception as e:
        print(f"保存文件时出错: {e}")
