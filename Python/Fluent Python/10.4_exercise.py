# def logger(func):
#     def wrapper(*args, **kw):
#         print('我准备开始计算：{} 函数了:'.format(func.__name__))
#
#         # 真正执行的是这行。
#         func(*args, **kw)
#
#         print('啊哈，我计算完啦。给自己加个鸡腿！！')
#     return wrapper
#
#
# @logger
# def add(x, y):
#     print('{} + {} = {}'.format(x, y, x+y))
#
#
# def decorate1(fun):
#     print("I am do something before running fun().")
#     fun("me")
#     print("I need do some other things.")
#
#
# def decorate(func):
#     def wrapper(arg1,arg2):
#         print("I get some parameters:{},{}".format(arg1,arg2),)
#         func(arg1,arg2)
#         print("I need do some other things.")
#     return wrapper
#
#
# @decorate
# def func(m1,m2):
#     print("I luff {} and {}.".format(m1,m2))
#
#
# func("qqq", "thomas")
import time
from time_decorator import clock
import functools
@clock
def fibo(n):
    if n < 2:
        return n
    return fibo(n-2)+fibo(n-1)
@functools.lru_cache()
@clock
def fibo2(n):
    if n < 2:
        return n
    return fibo(n-2)+fibo(n-1)

