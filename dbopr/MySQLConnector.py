#!/usr/bin/env python
# encoding: utf-8


"""
@summary:Mysql数据库连接模块,连接Mysql数据的参数请在conf的jdbc.properties文件中进行配置
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: MySQLConnector.py
@time: 2017/5/30 15:04
"""

import pymysql
from pymysql.cursors import DictCursor
from util.PooledDB import PooledDB
from util.Properties import Properties
from util.Logger import Logger

class MysqlConnector(object):

    """
    MYSQL数据库对象，负责产生数据库连接，此类中对应着数据库的连接池以及相应的操作方法,里面包含数据库的连接，
    以及根据sql语句对数据库中的数据进行增、删、改、查等操作方法
    """
    __logger = Logger("MysqlConnector")

    __pool = None
    def __init__(self):
        """
        MysqlConnector的初始化方法,里面默认从/conf/jdbc.properties中读取关于mysql连接的基本信息
        """
        self._conn = None
        self._cursor = None
        try:
            properties = Properties('/conf/jdbc.properties').getProperties()
            self._conn = MysqlConnector.__getConn(properties)
            self._cursor = self._conn.cursor()
        except AttributeError as ex:
            MysqlConnector.__logger.info("数据库连接失败!")
            MysqlConnector.__logger.error("__init__(self)方法报错")
            # MysqlConnector.__logger.exception(ex)

    @staticmethod
    def __getConn(properties):
        """
        @summary: 静态方法，从连接池中取出连接
        """
        pool=None
        try:
            if MysqlConnector.__pool is None:
                __pool = PooledDB(
                    creator=pymysql,mincached=int(properties['mysql.mincached']),maxcached=int(properties['mysql.maxcached']),
                    host=properties["mysql.url"],port=int(properties["mysql.port"]),user=properties["mysql.user"],passwd=properties["mysql.password"],
                    db=properties['mysql.schema'],charset=properties['mysql.charset'],cursorclass=DictCursor
                )
                pool =  __pool.connection()
        except Exception as ex:
            MysqlConnector.__logger.info("数据库连接失败")
            MysqlConnector.__logger.error("__getConn(properties)方法报错")
            # MysqlConnector.__logger.exception(ex)
        return pool

    def getAllRowObj(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询sql，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        result = None
        # print('=== sql  : ',sql)
        try:
            if param is None:
                count = self._cursor.execute(sql)

            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchall()
            else:
                result = False
        except Exception as ex:
            MysqlConnector.__logger.info("获取表中所有结果时，出现异常!")
            MysqlConnector.__logger.error(ex)
            MysqlConnector.__logger.error("getAllRowObj(self, sql, param=None)方法报错")
        return result

    def getOneRowObj(self, sql, param):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询sql，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        result = None
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchone()
            else:
                result = False
        except Exception as ex:
            MysqlConnector.__logger.info("获取表中一条结果时，出现异常!")
            MysqlConnector.__logger.error(ex)
            MysqlConnector.__logger.error("getOneRowObj(self, sql, param)方法报错")
        return result

    def getManyRowObj(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询sql，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        result = None
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchmany(num)
            else:
                result = False
        except Exception as ex:
            MysqlConnector.__logger.info("获取表中多条结果时，出现异常!")
            MysqlConnector.__logger.error("getManyRowObj(self, sql, num, param=None)方法报错")
        return result

    def insertOneRowObj(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的sql格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        count = None
        try:
            self._cursor.execute(sql, value)
            count = self.__getInsertId()
        except Exception as ex:
            MysqlConnector.__logger.info("向表中插入一条数据时,出现异常!")
            MysqlConnector.__logger.error(ex)
            MysqlConnector.__logger.error("insertOneRowObj(self, sql, value)方法报错")
        return count

    def insertManyRowObj(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的sql格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = None
        try:
            count = self._cursor.executemany(sql, values)
        except Exception as ex:
            MysqlConnector.__logger.info("向表中插入多条记录时,出现异常!")
            MysqlConnector.__logger.error("insertManyRowObj(self, sql, values)方法报错")
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        insrtId = None
        try:
            self._cursor.execute("SELECT @@IDENTITY AS id")
            result = self._cursor.fetchall()
            insrtId = result[0]['id']
            print('=== insert id test return : ' ,insrtId)
        except  Exception as ex:
            MysqlConnector.__logger.info("获取当前连接最后一次插入操作生成的id时,出现异常!")
            MysqlConnector.__logger.error("__getInsertId(self)方法报错")
        return insrtId

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: sql格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        count = None
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
        except Exception as ex:
            MysqlConnector.__logger.info("更新数据库中的数据时,出现异常!")
            MysqlConnector.__logger.error("update(self, sql, param=None)方法报错")
        return count

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: sql格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        count = None
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
        except Exception as ex:
            MysqlConnector.__logger.info("删除数据库中的数据时,出现异常!")
            MysqlConnector.__logger.error("delete(self, sql, param=None)方法报错")
        return count

    def commitTrasaction(self):
        """
        @summary: 提交事务
        """
        # self._cursor.close()
        try:
            self._conn.commit()
        except Exception as ex:
            MysqlConnector.__logger.info("提交事物时,出现异常!")

    def rollbackTransaction(self):
        """
        @summary: 事务回滚
        """
        try:
            self._cursor.close()
            self._conn.rollback()
        except Exception as ex:
            MysqlConnector.__logger.info("事务回滚异常!")

    def dispose(self):
        """
        @summary: 释放资源
        """
        try:
            if self._cursor is None :
                print('cursor is closed')
            else:
                self._cursor.close()
                if self._conn is None:
                    print('conn is closed')
                else:
                    self._conn.close()
        except Exception as ex:
            MysqlConnector.__logger.error("资源释放异常!")