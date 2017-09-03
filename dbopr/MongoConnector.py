#!/usr/bin/env python
# encoding: utf-8

"""
@summary:Mongodb数据库连接对象,Mongodb数据库的连接初始化参数请在conf的jdbc.properties文件中进行配置
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: MongoConnector.py
@time: 2017/5/31 22:11
"""

import pymongo
from util.Logger import Logger
from util.Properties import Properties

class MongoConnector(object):
    """
    Mongodb数据库对象以及相应的操作方法，里面包含对mongodb中的集合进行增、查以及相应的聚集操作
    该方法还有需要改进的地方,改进的地方为当付mongodb操作完之后，如何将连接进行关闭，以及设置每次连接的时长以及连接池的设定
    """

    __logger = Logger("MongoConnector")

    def __init__(self):
        """
        MongoConnector的初始化方法,里面默认从/conf/jdbc.properties中读取关于mongodb连接的基本信息
        """
        self._mongoClient = None
        self._db = None
        try:
            properties = Properties('/conf/jdbc.properties').getProperties()
            self._mongoClient = MongoConnector.__getMongoClient(properties)
            self._db = self._mongoClient['%s' % (properties['mongodb.database'])]
            self._db.authenticate(properties['mongodb.username'], properties['mongodb.password'], mechanism=properties['mongodb.mechanism'])
        except Exception as ex:
            MongoConnector.__logger.info("数据库连接失败,数据库名/数据库用户名/数据库密码错误")
            MongoConnector.__logger.exception(ex)

    @staticmethod
    def __getMongoClient(properties):
        """
        @summary: 静态方法，获取mongoClient对象
        """
        mongoClient = None
        try:
            mongoClient = pymongo.MongoClient(properties['mongodb.host'],int(properties['mongodb.port']),
                          maxPoolSize=int(properties['mongodb.maxPoolSize']),minPoolSize=int(properties['mongodb.minPoolSize']))
        except Exception as ex:
            MongoConnector.__logger.info('数据库连接失败,数据库的数据库的IP/数据库的端口错误')
            MongoConnector.__logger.error(ex)
        return mongoClient

    def getDB(self):
        """
        @summary: 返回Db对象
        """
        return self._db

    def getMongoClient(self):
        """
        @summary:返回MongoClient对象
        """
        return self._mongoClient


    def insertMany(self,collectionNm,bsonData):
        """
        @summary: 向collection里面插入多条记录
        @param collectionNm:集合名字
        @param bsonData：json数组
        """
        if self.dbNm:
            db = self.getDB()
            if isinstance(bsonData,list):
                result = db.get_collection(collectionNm).insert_many(bsonData)
                return result.inserted_ids
            else:
                return None
        else:
            return None


    def insertOne(self,collectionNm,bsonData):
        """
        @summary: 向collection里面插入一条记录
        @param collectionNm:集合名字
        @param bsonData：json对象
        """
        if self.dbNm:
            db = self.getDB()
            if bsonData:
                result = db.get_collection(collectionNm).insert_one(bsonData)
                return result.inserted_ids
            else:
                return None
        else:
            return None

    def find(self,collectionNm,**kwargs):
        """
        @summary: 根据相应的条件来查询collection里面的数据
        @param  **kwargs   (optional): additional keyword arguments will be passed as options for the find
        this param :
            (1)dataLimit ,限定最多返回多少条
            (2)dataSkip  ,跳过多少条
            (3)dataQuery ,查询限定条件
            (4)dataSortQuery 排序条件
            （5） dataProjection 返回指定的列或者排除指定的列
        """
        if collectionNm is None:
            return False
        else:
            db = self.getDB()

            def findAllDataQuery(self, dataLimit=0, dataSkip=0, dataQuery=None, dataSortQuery=None,
                                 dataProjection=None):
                return db.get_collection(collectionNm).find(filter=dataQuery, projection=dataProjection, skip=dataSkip,
                                                           limit=dataLimit, sort=dataSortQuery)
            return findAllDataQuery(self, **kwargs)

    def aggregation(self, collectionNm,aggreg):
        """
        @summary: 聚集查询
        @param aggreg: 聚集的操作，$max
        """
        if collectionNm:
            db = self.getDB()
            return db.get_collection(collectionNm).aggregate(aggreg)
        else:
            return False

    def count(self, collectionNm,countQuery=None, **kwargs):
        """
         @summary：按照特定的条件查询数据量大小
         @param countQuery:查询条件
        """
        if collectionNm:
            db = self.getDB()
            if countQuery and kwargs:
                return db.get_collection(collectionNm).count(countQuery, kwargs)
            elif countQuery:
                return db.get_collection(collectionNm).count(countQuery)
            elif kwargs:
                return db.get_collection(collectionNm).count(filter=None, **kwargs)
            else:
                return db.get_collection(collectionNm).count()
        else:
            return False

    def distinct(self,collectionNm,column,distinctQuery=None):

        """
        @summary：查询distinct的数据
        """
        if collectionNm:
            db=self.getDB()
            if distinctQuery and column:
                return db.get_collection(collectionNm).find(distinctQuery).distinct(column)
            else:
                if column:
                    return db.get_collection(collectionNm).distinct(column)
                else:
                    return False