#!/usr/bin/env python
# encoding: utf-8

"""
@summary:该模块是数据处理工程的邮件模块，主要负责将数据处理过程中发生的错误以邮件的形式发送给作者
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: Email.py
@time: 2017/5/20 8:23
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from util.Logger import Logger
from util.Properties import Properties
import smtplib


class Email(object):
    """
    邮件模块,默认从固定的目录下读取邮件的配置
    """
    __logger = Logger("Email")
    def __init__(self,prop_file):
        # self._properties = Properties('/conf/email.properties').getProperties()
        self._properties = Properties(prop_file).getProperties()

    def sendEmail(self,content,subject):
        """
        @summary: 发送邮件
        @param content:邮件的正文
        @param subject: 邮件的主题
        """
        try:
            sender = self._properties["sender"]#发件人
            senderPaswd = self._properties["sender.password"]#发件人的邮箱密码
            receiverInfo = self._properties["receiver"]#收件人
            receiverList = receiverInfo.split(",")
            carbonCopyInfo = self._properties['carbonCopy']  # 抄送
            carbonCopyList = carbonCopyInfo.split(",")
            smtpServer = self._properties["smtp.server"]#SMTP服务器
            smtpPort = int(self._properties["smtp.port"])#SMTP服务器的端口号

            if content is None:
                content = ""
            else:
                content = content

            msg = MIMEText(content)
            msg['From'] = sender
            msg['To'] = receiverInfo
            msg['Cc'] = carbonCopyInfo

            if subject is None:
                msg['Subject'] = ""
            else:
                msg['Subject'] = subject

            #发送邮件
            smtp = smtplib.SMTP_SSL(smtpServer,smtpPort)
            smtp.login(sender, senderPaswd)
            smtp.sendmail(sender, receiverList+carbonCopyList, msg.as_string())
            Email.__logger.info("send email successfully!")
        except Exception as  e:
            Email.__logger.error("send email failure")

    # 从文件路径中获取文件名
    @staticmethod
    def getFileNameInPath(filePath):
        fileName = filePath
        if ('/' in filePath):
            rfixIndex = filePath.rindex('/')
            fileName = filePath[rfixIndex + 1:]
        elif ('\\' in filePath):
            rfixIndex = filePath.rindex('/')
            fileName = filePath[rfixIndex + 1:]
        else:
            fileName = filePath
        return fileName

    def sendEmailWithAttach(self,subject,content,filePath):
        """
        @summary: 发送邮件
        @param content:邮件的正文
        @param subject: 邮件的主题
        @param filePath: 附件

        """
        try:
            sender = self._properties["sender"]#发件人
            senderPaswd = self._properties["sender.password"]#发件人的邮箱密码
            receiverInfo = self._properties["receiver"]#收件人
            carbonCopyInfo = self._properties['carbonCopy']  # 抄送
            carbonCopyList = carbonCopyInfo.split(",")
            receiverList = receiverInfo.split(",")
            smtpServer = self._properties["smtp.server"]#SMTP服务器
            smtpPort = int(self._properties["smtp.port"])#SMTP服务器的端口号

            if content is None:
                content = ""
            else:
                content = content


            msg = MIMEMultipart()
            # 设置主题，内容，收发件人
            if subject is None:
                msg['Subject'] = ""
            else:
                msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = receiverInfo
            msg['Cc'] = carbonCopyInfo
            pureText = MIMEText(content)
            msg.attach(pureText)

            # 添加附件
            attachFile = MIMEApplication(open(filePath,'rb').read())
            attachFile.add_header('Content-Disposition','attachment',filename=Email.getFileNameInPath(filePath))
            msg.attach(attachFile)

            #发送邮件
            smtp = smtplib.SMTP_SSL(smtpServer,smtpPort)
            smtp.login(sender, senderPaswd)
            smtp.sendmail(sender, receiverList+carbonCopyList, msg.as_string())
            Email.__logger.info("send email successfully!")
        except Exception as  e:
            Email.__logger.error("send email failure")