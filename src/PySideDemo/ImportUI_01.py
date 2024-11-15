#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ImportUI_01.py
# @Time      :2024/11/15 09:23:59
# @Author    :PengWei

import sys
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

app = QApplication([])

# 加载UI文件
ui_file = QFile("main.ui")
if not ui_file.open(QIODevice.ReadOnly):
    print("无法打开UI文件")
    sys.exit(-1)

# 创建UI加载器
loader = QUiLoader()

# 加载UI文件并实例化为窗口对象
window = loader.load(ui_file)

# 关闭UI文件
ui_file.close()

# 显示窗口
window.show()

# 运行应用程序
app.exec()
