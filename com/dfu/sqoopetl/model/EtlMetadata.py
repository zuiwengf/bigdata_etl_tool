#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 2018年7月19日
@author: zuiweng.df
@summary: 使用sqoop etl工具
'''

'''
'''
class EtlDB:
    def __init__(self,dbName,dbHost,dbPort,userName,password,enable=1,gmt_modify=None,gmt_create=None):
        self.id=id;
        self.dbName=dbName
        self.dbHost=dbHost
        self.dbPort=dbPort
        self.userName=userName
        self.password=password
        self.gmt_modify=gmt_modify
        self.gmt_create=gmt_create
        self.enable=enable
        
    def toConnString(self):
        return "jdbc:mysql://%s:%s/%s" % (self.dbHost,self.dbPort,self.dbName)
    
    def  __str__(self):
        return "dbName->%s # dbHost->%s # dbPort->%s # userName->%s"  % (self.dbName,self.dbHost,self.dbPort,self.userName)
    
    def  __repr__(self):
        return "dbName->%s # dbHost->%s # dbPort->%s # userName->%s"  % (self.dbName,self.dbHost,self.dbPort,self.userName)
    
    
    
class EtlTableTemplate:
    
    def __init__(self,sid,tableName,dbName,isMutTable,mergeCol,incrementCol,createTable,etlAllData,torder,pkeyName,incrementType,etlIncreamData,
                 tableSubName,mapperCount=1,enable=1,gmt_modify=None,gmt_create=None):
        self.sid=sid;
        self.tableName=tableName
        self.dbName=dbName
        self.isMutTable=isMutTable
        self.mergeCol=mergeCol
        self.incrementCol=incrementCol
        self.enable=enable
        self.createTable=createTable
        self.etlAllData=etlAllData
        self.pkeyName=pkeyName
        self.torder=torder
        self.mapperCount=mapperCount
        self.gmt_modify=gmt_modify
        self.gmt_create=gmt_create
        self.incrementType=incrementType
        self.etlIncreamData=etlIncreamData
        self.tableSubName=tableSubName

    
    def  __str__(self):
        return "id->%s  #  tableName->%s # dbId->%s # isMutTable->%s # torder->%s"  % (self.id,self.tableName,self.dbId,self.isMutTable,self.torder)
    
    def  __repr__(self):
        return "id->%s  #  tableName->%s # dbId->%s # isMutTable->%s # torder->%s"  % (self.id,self.tableName,self.dbId,self.isMutTable,self.torder)
    
    
    
    
class AppInfo:
    def __init__(self,sid,etlLogPath,newDataTempDir,namenodeUrl):
        self.sid=sid;
        self.etlLogPath=etlLogPath
        self.newDataTempDir=newDataTempDir
        self.namenodeUrl=namenodeUrl
        
        
class UDFConf:
        def __init__(self,sid,funName,packageName,jarName,hdfsPath,namenodeUrl,hiveDBNames):
            self.sid=sid;
            self.funName=funName
            self.packageName=packageName
            self.jarName=jarName
            self.hdfsPath=hdfsPath
            self.namenodeUrl=namenodeUrl
            self.hiveDBNames=hiveDBNames

    
        