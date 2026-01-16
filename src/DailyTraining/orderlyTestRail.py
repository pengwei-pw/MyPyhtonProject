#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :orderlyTestRail.py
# @Time      :2026/01/05 17:24:23
# @Author    :PengWei
import win32com.client as win32
import os
import pandas as pd
from pathlib import Path

def orderlyTestRail(Test_case_Folder, Test_run_Folder, automation_sheet, out_path):
    # test rail 导出的xls是缺损文件，代码无法打开，先修复
    fix_xls(Test_case_Folder)
    fix_xls(Test_run_Folder)

    # 规整test run，以test run的模块为准
    test_run_modules = {}
    for file in os.listdir(Test_run_Folder):
        if file.endswith('.xlsx'):
            name_list = file.replace('.xlsx', '').split('_')
            name = ' '.join(name_list).title()
            print(f"Processing test run file: {file} as module name: {name}")
            test_run_path = os.path.join(Test_run_Folder, file)
            test_run_df = pd.read_excel(test_run_path)
            print(len(test_run_df))
            test_run_modules[name] = test_run_df

    # 处理test case
    test_case_modules = {}
    for file in os.listdir(Test_case_Folder):
        if file.endswith('.xlsx'):
            test_case_df = pd.read_excel(os.path.join(Test_case_Folder, file))
            name = test_case_df['Suite'].unique()[0]
            name = name.title()
            print(f"Processing test case file: {file} with {len(test_case_df)} entries")
            test_case_modules[name] = test_case_df

    # 处理自动化维护表格
    automation_sheet_Modules = {}
    xls = pd.ExcelFile(automation_sheet)
    for sheet in xls.sheet_names:
        df = pd.read_excel(automation_sheet, sheet_name=sheet)
        sheet = sheet.title()
        automation_sheet_Modules[sheet] = df


    # 对比test case和test run、自动化维护表格的模块，打印观察是否模块名不能对应
    print(f'Automation Sheet Modules: {list(automation_sheet_Modules.keys())}')
    print(f'Test Run Modules: {list(test_run_modules.keys())}')
    print(f'Test Case Modules: {list(test_case_modules.keys())}')

    # 根据已知模块明统一三表模块名
    module_name_mapping = {
        'Vr&Llm': 'Vr',
        'Vr Llm': 'Vr',
        'Multi Screen Interaction' : 'Multi-Screen Interaction',
        'System Performance': '一键优化'
    }
    test_case_modules = {module_name_mapping.get(k, k): v for k, v in test_case_modules.items()}
    test_run_modules = {module_name_mapping.get(k, k): v for k, v in test_run_modules.items()}
    automation_sheet_Modules = {module_name_mapping.get(k, k): v for k, v in automation_sheet_Modules.items()}
    print('======================================================================================')
    # 打印替换后的模块名对比结果
    print(f'Automation Sheet Modules: {list(automation_sheet_Modules.keys())}')
    print(f'Test Run Modules: {list(test_run_modules.keys())}')
    print(f'Test Case Modules: {list(test_case_modules.keys())}')

    # 若automation_sheet存在模块未匹配，将其添加到最终结果中，方便下次使用更新
    processed_sheets = {}
    for module in automation_sheet_Modules.keys():
        if module not in test_run_modules.keys():
            processed_sheets[module] = automation_sheet_Modules[module]

    # 先合并test case和test run合并后，再将结果和自动化维护表格合并
    test_run_cols =  ['Case ID', 'ID'] 
    automation_cols = ['ID', 'Automation_Y', '分类/依赖', '责任人-483', '责任人-542', 'Comments', 'Script Name', '是否开发', '不能开发原因']
    for module in test_run_modules.keys():
        if module in test_case_modules.keys() and module in automation_sheet_Modules.keys():
            print(f"正在处理模块: {module}")
            test_case_df = test_case_modules[module] 
            test_run_df = test_run_modules[module] 
            automation_df = automation_sheet_Modules[module] 
            # test case保留所有列，test run只保留部分列
            # 读取B表，如果存在所需列
            print(f"Automation DF columns after filtering: {automation_df.columns.tolist()}")
            automation_cols = [col for col in automation_cols if col in automation_df.columns]
            automation_df = automation_df[automation_cols]  # 显式选择所需列
            print(f"Automation DF columns after filtering: {automation_df.columns.tolist()}")

            # 读取C表，如果存在所需列
            test_run_cols = [col for col in test_run_cols if col in test_run_df.columns]
            test_run_df = test_run_df[test_run_cols]  # 显式选择所需列

            if not automation_df.empty:
                test_case_df = test_case_df.merge(automation_df, on='ID', how='left')
                
            if not test_run_df.empty:
                test_run_df = test_run_df.rename(columns={'ID': 'TestRun ID'})
                test_case_df = test_case_df.merge(test_run_df, left_on='ID', right_on='Case ID', how='left')

                        # 将处理后的结果保存到字典中
            test_case_df['自动化是否测试'] = test_case_df.apply(
                lambda row: '是' if pd.notna(row['TestRun ID']) and row['Automation'] == ' Completed' else '',
                axis=1
            )
            test_case_df['Automation_Y'] = test_case_df.apply(
                lambda row: 'Y' if row['Automation'] == ' Completed' else '',
                axis=1
            )
            processed_sheets[module] = test_case_df
        else:
            print(f"模块 {module} 在三张表中未能完全对应，跳过该模块的合并。")
            continue
    # 如果需要保存修改后的Excel文件，可以使用以下代码：
    try:
        with pd.ExcelWriter(out_path) as writer:
            for sheet, df in processed_sheets.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        print(f"处理后的文件已保存为 {out_path}")
    except Exception as e:
        print(f"保存文件时出错: {e}")

            
import time
def fix_xls(path_to_xls):
    excel = win32.Dispatch("Excel.Application")
    excel.DisplayAlerts = False

    xls_dir = Path(path_to_xls)

    for f in xls_dir.glob("*.xls"):
        wb = None
        try:
            print(f"Opening {f}...")
            wb = excel.Workbooks.Open(str(f))
            out_file = xls_dir / f.with_suffix(".xlsx").name
            wb.SaveAs(str(out_file), FileFormat=51)
            print(f"Converted: {f.name} → {out_file.name}")
        except Exception as e:
            print(f"Failed to convert {f.name}: {e}")
        finally:
            # wb 可能为 None 或已断开连接，防止报错
            try:
                if wb is not None:
                    wb.Close()
            except Exception:
                pass
            # 给 COM 一点缓冲
            time.sleep(0.05)

    excel.Quit()

# def fix_xls(path_to_xls):
#     excel = win32.Dispatch("Excel.Application")
#     excel.DisplayAlerts = False

#     xls_dir = Path(path_to_xls)

#     for f in xls_dir.glob("*.xls"):
#         wb = excel.Workbooks.Open(str(f))
#         wb.SaveAs(str(xls_dir / f.with_suffix(".xlsx").name), FileFormat=51)
#         wb.Close()
#     excel.Quit()

if __name__ == "__main__":
    # test case 文件夹
    Test_case_Folder = r'C:\Users\pengw\Desktop\test_py\testcase'
    # test run 文件夹
    Test_run_Folder = r'C:\Users\pengw\Desktop\test_py\testrun'
    # 自动化维护表格
    automation_sheet = r"C:\Users\pengw\Desktop\test_py\save\CX483ICA2_2.0.0_FocusTest_11.21.xlsx"
    # 输出表格
    out_path = r"C:\Users\pengw\Desktop\test_py\orderlyTestRail.xlsx"

    orderlyTestRail(Test_case_Folder, Test_run_Folder, automation_sheet, out_path)