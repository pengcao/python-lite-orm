#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: DictUtil.py
@time: 2017/5/21 18:11
@desc:
'''

class DictUtil(object):

    # 获取字典中某个key的值
    @staticmethod
    def getDictValue(Dict,keyName):
        if keyName in Dict:
            return Dict[keyName]
        else:
            return None

    # 获取字典中某个key的String类型的值,空值的情况下默认值为''
    @staticmethod
    def getDictStrValue(Dict,keyName):
        if keyName in Dict:
            if Dict[keyName]:
                return Dict[keyName]
            else:
                return ''
        else:
            return ' '
