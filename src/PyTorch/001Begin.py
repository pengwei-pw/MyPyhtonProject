#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :001Begin.py
# @Time      :2026/3/31 21:03
# @Author    :pengweiaini123@163.com
import torch

# 检查 CUDA 是否可用
print(torch.cuda.is_available())  # True/False
print(torch.cuda.device_count())  # GPU 数量
print(torch.cuda.get_device_name(0))  # GPU 型号
