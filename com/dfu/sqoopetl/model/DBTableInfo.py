#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 2018年7月17日
@author: zuiweng.df
'''


"""
数据库信息
"""
class ConnDBInfo(object):
    def __init__(self,ip,port,dbName,userName,passwd):
        self.ip=ip;
        self.port=port;
        self.dbName=dbName;
        self.userName=userName;
        self.passwd=passwd;
    
    def toConnString(self):
        return "jdbc:mysql://%s:%s/%s" % (self.ip,self.port,self.dbName)
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    
    def __hash__(self):
        return hash(self.dbName)
        
    def __str__(self):
        return "  #### ip-> %s #### port-> %s #### db-> %s #### userName -> %s" % ( self.ip,self.port,self.dbName,self.userName)
    
    def __repr__(self, *args, **kwargs):
        return "  #### ip-> %s #### port-> %s #### db-> %s #### userName -> %s" % ( self.ip,self.port,self.dbName,self.userName)
    








"""
提取的表格信息
"""
class ETLTable(object):
    
    def __init__(self,dbName,realTableName,tableTemplate):
        self.tableTemplateId=tableTemplate.sid
        self.dbName=dbName
        self.realTableName=realTableName
        self.isMutTable=tableTemplate.isMutTable
        self.mergeCol=tableTemplate.mergeCol
        self.incrementCol=tableTemplate.incrementCol
        self.enable=tableTemplate.enable
        self.createTable=tableTemplate.createTable
        self.etlAllData=tableTemplate.etlAllData
        self.torder=tableTemplate.torder
        self.targetTableName=tableTemplate.tableName
        self.mapperCount=tableTemplate.mapperCount
        self.pkeyName=tableTemplate.pkeyName
        self.incrementType=tableTemplate.incrementType
        self.etlIncreamData=tableTemplate.etlIncreamData
        
   
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    
    def __hash__(self):
        return hash(self.dbName)+hash(self.tableName) 
    
    
    def __str__(self):
        return " tableInfo:dbName>%s tableName->%s " % ( self.dbName,self.tableName)
    
    def __repr__(self):
        return " tableInfo:dbName>%s tableName->%s " % ( self.dbName,self.tableName)
    
    





"""
自定义异常
"""
class EtlException(Exception):
    pass