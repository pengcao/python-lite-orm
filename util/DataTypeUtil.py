#!/usr/bin/env python
# encoding: utf-8

"""
@summary:该模块主要是关于对从数据库中查询出来的数据进行数据类型转换
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com.
@software: garner
@file: DataTypeUtil.py
@time: 2017/5/24 16:51
"""

class MysqlDataTypeUtil(object):

    @staticmethod
    def transDecimalData(data):
        """
        @summary:数据类型转换程序，将获取得到的数据类型转换成decimal
        @param data: mysql查询出来的数据
        """
        if data is None:
            return 0
        else:
            return data