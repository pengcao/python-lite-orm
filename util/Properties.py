#!/usr/bin/env python
# encoding: utf-8

"""
@summary:该模块主要是读取properties文件里面的配置信息
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: Properties.py
@time: 2016/5/30 16:14
"""
import sys,os
from util.Logger import Logger

class Properties(object):
    """
    读取配置文件  定义读取配置文件的类
    """
    __logger = Logger("Properties")
    def __init__(self, fileName):
        path = sys.path[0]
        self.fileName = os.path.dirname(path)+fileName
        self.properties = {} #该属性为一个字典对象


    def getProperties(self):
        """
        @summary: 获取 Properties里面的文件信息
        """
        try:
            pro_file = open(self.fileName, 'Ur')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#")!=-1:
                    line=line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1]= line[len(strs[0])+1:]
                    self.properties[strs[0].strip()]=strs[1].strip()
            try:
                pro_file.close()
            except Exception as ex:
                Properties.__logger.error("关闭配置文件关闭时,出现错误")
        except Exception as e:
            raise Properties.__logger.error("读取配置文件时,出现错误")
        return self.properties

    def getCurrentPath(self):
        """
        @summary: 获取当前文件所处的目录
        """
        path = sys.path[0]
        return os.path.dirname(path)

    def getParentPath(self):
        """
        @summary: 获取当前文件所处的目录
        """
        path = sys.path[0]
        return os.path.abspath(os.path.join(os.path.dirname(path), os.path.pardir))


