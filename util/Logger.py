#!/usr/bin/env python
# encoding: utf-8

"""
@summary:日志对象模块,主要将脚本在运行过程中的错误以及运行情况输出到log的etl.log文件里
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: Logger.py
@time: 2016/5/21 8:17
"""
import logging
import sys,os

class Logger(object):
    """
    日志类，在这里面默人了日志输出的文件
    """
    def __init__(self,name):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        fullfilename = os.path.dirname(sys.path[0])+'/log/etl.log'
        fileHandl = logging.FileHandler(fullfilename,'a',encoding='utf8')
        fileHandl.setLevel(logging.INFO)

        strmHandl = logging.StreamHandler()
        strmHandl.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandl.setFormatter(formatter)
        strmHandl.setFormatter(formatter)

        self._logger.addHandler(fileHandl)
        self._logger.addHandler(strmHandl)

    def info(self,message):
        """
        @summary:在该logger上以INFO级别记录一条信息
        """
        self._logger.info(message)

    def debug(self,message):
        """
        @summary:在该logger上以DEBUG级别记录一条信息
        """
        self._logger.debug(message)

    def error(self,message):
        """
        @summary:在该logger上以ERROR级别记录一条信息
        """
        self._logger.error(message)

    def warring(self,message):
        """
        @summary:在该logger上以WARRING级别记录一条信息
        """
        self._logger.warning(message)

    def exception(self,message):
        """
        @summary:在该logger上输出异常信息
        """
        self._logger.exception(message)