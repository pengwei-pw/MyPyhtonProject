#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test_decorator01.py
# @Time      :2024/11/15 15:04:15
# @Author    :PengWei
import sys
import os
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# sys.path.insert(0, project_root)
from src.DecoratorDemo.Decorator_01 import *


@decorator
def test_function():
    print("hello, this is my function")

test_function()
