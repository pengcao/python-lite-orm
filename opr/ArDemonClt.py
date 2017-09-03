#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: ArDemonClt.py
@time: 2017/6/10 14:35
@desc: 测试
'''

from util.XmlParse import SqlXmlParse
from util.Logger import Logger

sqlXmlParse = SqlXmlParse('ArDemonClt')


# 定义对ArDemonClt表进行增删改查的SQL语句
class ArDemonCltSql(object):

    # 1.汇总
    def getSumOrdDataSql(self):
        return sqlXmlParse.getSql('getSumOrdDataSql')



# 对ArDemonClt表进行增删改查的方法
class ArDemonCltOpr(object):
    __logger = Logger('ArDemonCltOpr')

    # 根据查询的结果对象和插入SQL语句向表中插入单条数据
    def insertOneArDemonClt(self, mysqlConnector, obj, sql):
        """
        @summary:向表ArDemonClt中插入单条数据
        """
        try:
            if obj:
                sqlParmList = sqlXmlParse.transInsrtObjBySql(obj, sql)
                if sqlParmList:
                    mysqlConnector.insertOneRowObj(sql, sqlParmList)
        except Exception as ex:
            ArDemonCltOpr.__logger.error(
                "insertOneArDemonCltBySql,向表ArDemonClt中插入单条数据时出错")
            ArDemonCltOpr.__logger.error(ex)
            ArDemonCltOpr.__logger.info(sql)