#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: XmlParse.py
@time: 2017/5/23 17:09
@desc:
      对XML文件进行解析
'''

import sys,os
from util.Logger import Logger
import xml.etree.cElementTree as xmlEt
from util.DictUtil import DictUtil

class SqlXmlParse(object):
    # 将存放有sql语句的xml文件进行解析
    __logger = Logger("SqlXmlParse")

    def __init__(self, filename):

        path = sys.path[0]
        self.package = filename
        self.filename = os.path.dirname(path)+'/orm/'+filename+'.xml'

    # 获取对应的SQL语句,将XML中对应的元素解析成SQL语句
    def getSql(self,methnm):
        SqlXmlParse.__logger.info('加载' + self.package + '.' + methnm + '的SQL语句:' + self.filename)
        tree = xmlEt.parse(self.filename)
        root = tree.getroot()
        for child in root:
            if child.attrib['id'] == methnm:
                sql = (child.text).replace('\n', '')
                sql = sql.replace('SQL_LARGER_THAN_EQ','>=')
                sql = sql.replace('SQL_LESS_THAN_EQ', '<=')
                sql = sql.replace('SQL_LARGER_THAN', '>')
                sql = sql.replace('SQL_LESS_THAN','<')
                return sql
        SqlXmlParse.__logger.error('加载'+self.package+'.'+methnm+'的SQL语句失败!')
        return None

    # 获取sql里面的KEY
    @staticmethod
    def parseInsrtTableKeys(sqlText):
        if sqlText:
            sqlText = sqlText.replace(' ', '')
            startIndex = sqlText.index('(')
            endIndex = sqlText.index(')')
            keyStr = sqlText[startIndex + 1:endIndex]
            keyList = keyStr.split(',')
            return keyList
        else:
            return None

    # 根据insert语句获取插入的参数
    def transInsrtObjBySql(self,obj,insrtSql):
        param = []
        if obj is not None and insrtSql is not None:
            keyList = SqlXmlParse.parseInsrtTableKeys(insrtSql)
            if keyList:
                for key in keyList:
                    param.append(DictUtil.getDictValue(obj, key))
                return param
            else:
                return None
        else:
            return None

    # 根据参数集向表中插入数据
    def transInsrtObjByKeys(self,obj,keyList):
        param = []
        if keyList:
            for key in keyList:
                param.append(DictUtil.getDictValue(obj,key))
            return param
        else:
            return None