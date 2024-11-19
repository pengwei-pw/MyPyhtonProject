#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Decorator_01.py
# @Time      :2024/11/15 09:29:28
# @Author    :PengWei

"""
装饰器本质上是一个函数，它可以接收一个函数作为参数并返回一个新的函数。这个新函数是对原函数的一种包装或增强，可以在不改变原函数代码的前提下，增加额外的功能。
"""

def decorator(fun):
    def wrapper(*args, **kwargs):
        print("before calling the function")
        result = fun(*args, **kwargs)
        print("after calling the function")
        return result
    return wrapper

@decorator
def test_demo(*args, **kwargs):
    print(args)
    print(kwargs)
    print("hello decorator")

test_demo("test1", 1024, "name=kuuleiliya", name="wpeng23")
