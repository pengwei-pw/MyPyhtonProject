#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :PySideDemo1.py
# @Time      :2024/11/15 09:16:18
# @Author    :PengWei

# 这一行导入了 QApplication、QWidget 和 QLabel 类，它们是 PySide6 中用于创建应用程序和窗口组件的类。
from PySide6.QtWidgets import QApplication, QWidget,QLabel

# 创建了一个 QApplication 实例，用于管理整个应用程序的事件循环和资源分配。
app = QApplication()

# 创建一个空白的 QWidget 对象，它代表着我们的窗体。
window = QWidget()
# 设置窗体的标题为 "Simple Window"。
window.setWindowTitle("Simple Window")
# 将窗体的大小固定为宽度为 400 像素、高度为 300 像素。
window.setFixedSize(400, 300)

# 创建一个 QLabel 对象，并将其作为子组件添加到窗体上。同时，设置标签的显示文本为 "Hello PySide6!"。
label = QLabel("Hello PySide6!", window)
# 创建一个 QLabel 对象，并将其作为子组件添加到窗体上。同时，设置标签的显示文本为 "Hello PySide6!"。
label.move(150, 125)

# 显示窗体
window.show()

# 启动应用程序的事件循环，等待事件的触发和处理，使窗体保持可响应状态。
app.exec()

