#!/usr/bin/env python
# encoding: utf-8

"""
@summary:文件模块，该模块主要是用于操作文件的
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: FileUtil.py
@time: 2017/5/12 17:06
"""

import os,sys
import codecs
from util.Logger import Logger

class FileUtil(object):
    """
    文件工具类
    """
    __logger = Logger("FileUtil")

    def getFileListByExtension(self,dirPath,extension):
        """
        @summary:获取指定目录下的所有指定后缀的文件名
        @param dirPath：指定目录
        @param extension: 文件的后缀名
        """
        extensionFileList = []
        extensionName = '.'+extension #文件的后缀名  例如.log
        fileList = os.listdir(dirPath)
        for file in fileList:
            # os.path.splitext():分离文件名与扩展名
            if os.path.splitext(file)[1] == extensionName:
                extensionFileList.append(file)
        return extensionFileList

    def writeToFile(self,dirPath,content):
        """
        @sumary:向文件中输出内容
        @param dirPath:文件的目录
        @param content:将要输出的内容
        """
        fileWrObj = codecs.open(dirPath,'a',encoding='utf8')
        # fileWrObj = open(dirPath, 'a')
        fileWrObj.write(content)
        fileWrObj.close()

    def readFromFile(self, dirPath):
        """
        @sumary:向文件中输出内容
        @param dirPath:文件的目录
        @param content:将要输出的内容
        """
        # fileWrObj = codecs.open(dirPath, 'a', encoding='utf8')
        content = None
        try:
            fileReadObj = codecs.open(dirPath, 'r', encoding='utf8')
            content = fileReadObj.read()
        except Exception as e:
            errMsg = '读取文件'+dirPath+'失败'
            FileUtil.__logger.error(errMsg)
        return content

    def getFilePath(self,fileName):
        """
        @summary:获取文件的路径，os.path.dirname(sys.path[0])+'/conf/teste.txt'
        @param fileName: 这个存放的是相对于工程的文件路径
        """
        filePath = filename = os.path.dirname(sys.path[0])+fileName
        return filePath

if __name__ == '__main__':
    print('FileUtil.py')
    # filename = '/conf/address.json'
    filename = '/conf/districtDict.txt'
    fileUtil = FileUtil()
    fullfilename = fileUtil.getFilePath(filename)
    content = fileUtil.readFromFile(fullfilename)
    print(content)
    # fullfilename = fileUtil.getFilePath(filename)
    # content = '这个仅仅是一个测试而已！!'
    # print(content)
    # fileUtil.writeToFile(fullfilename,content)
