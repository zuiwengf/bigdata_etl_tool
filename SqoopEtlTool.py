#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 2018年7月17日
@author: zuiweng
@summary: 使用sqoop etl工具
'''
import ConfigParser
import datetime
import logging
from optparse import OptionParser
import os
import random
import re
import subprocess
import sys
import time
import traceback

from com.xcom.dfupetl.model.DBTableInfo import ETLTable
from com.xcom.dfupetl.model.EtlMetadata import EtlDB, EtlTableTemplate, AppInfo, \
    UDFConf
from com.xcom.dfupetl.utils.DBHelper import DBHelper




'''
sqoop表导入hive的工具
'''
class SqoopEtlTool(object):
    
    '''
       开始从mysql导入hive
    '''
    def startEtl(self):
        #创建日志路径
        today=datetime.date.today()
        formattedToday=today.strftime('%y%m%d')
        self.currPath=self.appInfo.etlLogPath+"/"+formattedToday+"/"+str(self.batchNumIn)
        os.system("rm -rf "+self.currPath)
        os.system("mkdir -p  "+self.currPath)
        
        self.realEtlTableList.sort(lambda a,b:b.torder-a.torder)
        self.splitTableDict={}
        
        if SqoopEtlTool.str2Bool(self.dropAllTable) :
            #AppInfo
            namenodeUrl=self.appInfo.namenodeUrl;
            for k,tableTemplate in self.tableTemplateDict.items():
                ##EtlTableTemplate
                dbName=tableTemplate.dbName
                baseTableName="ods_"+dbName+"."+tableTemplate.tableName
                
        
                tempTableNameList=[baseTableName,baseTableName+"_daily_incr"]
                for tableName in tempTableNameList:
                    self.system(r''' hive -e  "  drop table IF  EXISTS  %s  " ''' % tableName,None,0)
               
                tempDNName="ods_"+dbName+".db"
                tempTableNameList=[tableTemplate.tableName,tableTemplate.tableName+"_daily_incr"]
                for tableName in tempTableNameList:
                    dict={
                        "namenodeUrl":namenodeUrl,
                        "tempDNName":tempDNName,
                        "tableName":tableName
                        }
                    tablePath=r''' hadoop fs -rm -r  {0[namenodeUrl]}/user/hive/warehouse/{0[tempDNName]}/{0[tableName]}'''.format(dict)
                    self.system(tablePath,None,0)
                    tablePath=r''' hadoop fs -rmdir   {0[namenodeUrl]}/user/hive/warehouse/{0[tempDNName]}/{0[tableName]}'''.format(dict)
                    self.system(tablePath,None,0)   
            
        
        #遍历循环所有的表
        ####  EtlTableTemplate
        for k,tableTemplate in self.tableTemplateDict.items():
                #如果是全量导入则创建表 EtlTableTemplate
                if  tableTemplate.createTable==1 :
                    try:
                        self.exeCreateTable(tableTemplate)
                    except Exception as e:
                        logging.error(r"exeCreateTable 出现问题: %s     %s " % (tableTemplate.tableName,str(e)))
                        traceback.print_exc()
                        
                    currentPath=os.path.abspath(os.path.join(os.getcwd(), "."))
                    os.system("rm -rf  %s/*.java" % currentPath)
                        
        #全量导入数据    ETLTable              
        for tableInfo in self.realEtlTableList:
            #如果需要全部导入
            if  tableInfo.etlAllData==1 :
                #如果是多个分表
                if  tableInfo.isMutTable==1:
                    rr=re.match(r"(.*?)_(\d+)",tableInfo.realTableName, re.M|re.I)
                    try:
                        self.extractAllData(tableInfo,False)
                    except Exception as e:
                        logging.error(r'extractAllData 出现问题: '+str(e))
                        traceback.print_exc()
                else:
                    try:
                        self.extractAllData(tableInfo,True)
                    except Exception as e:
                        logging.error(r'extractAllData 出现问题: '+str(e))
                        traceback.print_exc()
                
                currentPath=os.path.abspath(os.path.join(os.getcwd(), "."))
                os.system("rm -rf  %s/*.java" % currentPath) 
                    

        #增量导入             ETLTable  
        for tableInfo in self.realEtlTableList:
            if tableInfo.etlIncreamData==1:
                if tableInfo.isMutTable==1 and tableInfo.incrementType==1:
                    try:
                        self.extractIncrementData(tableInfo)
                    except Exception as e:
                        logging.error(r'extractIncrementData  出现问题: '+str(e))
                        traceback.print_exc()
                else :
                    try:
                        self.extractAllData(tableInfo,True)
                    except Exception as e:
                        logging.error(r'extractAllData 出现问题: '+str(e))
                        traceback.print_exc()
                    
                
                
                currentPath=os.path.abspath(os.path.join(os.getcwd(), "."))
                os.system("rm -rf  %s/*.java" % currentPath) 

        #从临时表导入到总表   ，不能和上一段合并代码  EtlTableTemplate。因为他等待所有分表执行完以后才开始
        for  k,tableTemplate in self.tableTemplateDict.items():
            if   tableTemplate.etlIncreamData==1 and tableInfo.isMutTable==1  and tableTemplate.incrementType==1:
                try:
                    self.mergeTempData2RealTable(tableTemplate)
                except Exception as e:
                    logging.error(r' mergeTempData2RealTable 出现问题:   ==》 '+tableTemplate.tableName+"    "+str(e))
                    traceback.print_exc()

            currentPath=os.path.abspath(os.path.join(os.getcwd(), "."))
            os.system("rm -rf  %s/*.java" % currentPath)              
                
                
                
        currentPath=os.path.abspath(os.path.join(os.getcwd(), "."))
        os.system("rm -rf  %s/*.java" % currentPath)      
                   
                    

    def system(self,cmd,tableInfo,sleepTime=1,recLog=1):
#         time.sleep(1)
        logging.warn(r"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 执行如下命令： ")
        logging.info(cmd)
        if sleepTime >0:
            time.sleep(sleepTime)
            
        startTime=datetime.datetime.now() 
        os.system(cmd)
        endTime=datetime.datetime.now()
        
        if  recLog==1 and  tableInfo  is not None:
            self.insertEtlRes(tableInfo,0,0,startTime,endTime,cmd) 
#         cmdOut = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         while True:
#             line = cmdOut.stdout.readline()
#             print(line)
#             if subprocess.Popen.poll(cmdOut)==0:
#                 break 
                
    '''
    从临时表到总表合并
    '''            
    def mergeTempData2RealTable(self,tableInfo):
        ####EtlTableTemplate
        targetDBName="ods_"+tableInfo.dbName+"."
        allDataTable=targetDBName+tableInfo.tableName
        pkeyName=tableInfo.pkeyName
        
        increaseDataTable=targetDBName+tableInfo.tableName+"_daily_incr"
        hiveTableDict={
           "allDataTable":allDataTable,
           "increaseDataTable":increaseDataTable,
           "pkeyName":pkeyName
        }
        hiveCmd=r'''hive -e " insert overwrite    table {0[allDataTable]}    select * from ( select a.* from {0[allDataTable]} as a where a.{0[pkeyName]}  not in ( select  {0[pkeyName]} from {0[increaseDataTable]} ) union all select b.* from {0[increaseDataTable]} as b  ) tmp " '''.format(hiveTableDict)
        logging.info( r" mergeTempData2RealTable: hiveCmd %s" %  hiveCmd)
        self.system(hiveCmd,tableInfo)
        
        
        
    
    '''
         向数据库中插入每一个etl table的记录
    '''
    def insertEtlRes(self,tableInfo,type,status,startTime,endTime,cmd):
        if isinstance(tableInfo, ETLTable):
            sourceTableName=tableInfo.realTableName
            targetTableName=tableInfo.targetTableName
            
        else :
            sourceTableName=tableInfo.tableName
            targetTableName=tableInfo.tableName
        
        
        sourceDBName=tableInfo.dbName
        targetDBName="ods_"+tableInfo.dbName
        useTime=(endTime-startTime).seconds
        
        dataDict={
            "sourceTableName":sourceTableName,
            "targetTableName":targetTableName,
            "sourceDBName":sourceDBName,
            "targetDBName":targetDBName,
            "type":type,
            "batchNum":self.batchNumIn,
            "status":status,
            "startTime":startTime,
            "endTime":endTime,
            "useTime":useTime,
            "cmd":cmd
            }
        
        DBHelper.insert(self.configDBInfo,"table_exe_info",dataDict);
                    
    '''
    创建hive表
    '''
    def exeCreateTable(self,etlTableTemplate):
        ####EtlTableTemplate
        dbName=etlTableTemplate.dbName
        dbInfo=self.dbDict.get(dbName)
        if etlTableTemplate.isMutTable==1:
            sql="desc %s%s" % (etlTableTemplate.tableName,etlTableTemplate.tableSubName)
        else:
            sql="desc %s " % etlTableTemplate.tableName
        
        fetchResult=DBHelper.query(dbInfo,sql);
        rowcount=fetchResult[0]
        queryResult=fetchResult[1]
        baseTableName="ods_"+dbName+"."+etlTableTemplate.tableName

        tempTableNameList=[baseTableName,baseTableName+"_daily_incr"]

              
        if (queryResult is not None) and rowcount>0 :
            for tableName in tempTableNameList:
                createTableStr=r''' hive -e  " create  table  IF NOT EXISTS  ''' +tableName+''' ( '''
                index=0
                maxSize=len(queryResult)
                for columnInfo in queryResult:
                    columnName=columnInfo[0]
                    columnType=columnInfo[1]
                    createTableStr=createTableStr+" "+columnName+" "
                    
                    #判断数据类型
                    if "int" in columnType:
                        columnType=" int "
                    elif "long" in columnType:
                        columnType=" bigint "
                    elif "varchar" in columnType:
                        columnType=" string "
                    elif "float" in columnType:
                        columnType=" float "
                    elif "double" in columnType:
                        columnType=" double "
                    elif "datetime" in columnType:
                        columnType=" timestamp "
                    elif "timestamp" in columnType:
                        columnType=" timestamp "
                    elif "text" in columnType:
                        columnType=" string "
                    elif "decimal" in columnType:
                        #使用数据库的原有配置旧ok
                        pass
                    
                    #是否是最后一行
                    if index < maxSize-1:
                        createTableStr=createTableStr+" "+columnType+" , "
                    else :
                        createTableStr=createTableStr+" "+columnType
                    index=index+1
                    
                   
                createTableStr=createTableStr+r''' ) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'  STORED AS TEXTFILE "   '''
                logging.info( r"exeCreateTable: %s" % createTableStr)
                self.system(createTableStr,etlTableTemplate)
        
        
        
        
    '''
            全量导入数据
    '''
    def extractAllData(self,tableInfo,isOverWrite):
        dbName=tableInfo.dbName
        dbInfo=self.dbDict.get(dbName)
        connStr=dbInfo.toConnString()
        targetDir=self.appInfo.namenodeUrl+"/user/hive/tmp/warehouse/ods_"+dbName+".db/"+tableInfo.realTableName
        hadoopDbDict={
               "targetDir":targetDir
        }
        
        hdfsCmd=r'''hadoop  dfs -rm -r {0[targetDir]}  '''.format(hadoopDbDict)
        logging.info( r"extractAllData: hdfsCmd %s" %  hdfsCmd)
        self.system(hdfsCmd,tableInfo)
        
        
        sqoopDbDict={
               "mysqlConn":connStr,
               "username":dbInfo.userName,
               "password":dbInfo.password,
               "tableName":tableInfo.realTableName,
               "mapperCount":tableInfo.mapperCount,
               "targetDir":targetDir,
               "pkeyName":tableInfo.pkeyName
        }
        
        sqoopCmd=r''' sqoop import    --connect {0[mysqlConn]}      --table {0[tableName]}    --username {0[username]}     --password {0[password]}  --split-by {0[pkeyName]}  --hive-drop-import-delims --null-string '\\N'     --null-non-string '\\N'   --target-dir {0[targetDir]}    --fields-terminated-by  '\t'     --lines-terminated-by '\n'  '''.format(sqoopDbDict)
        logging.info( r"extractAllData: sqoopCmd %s" %  sqoopCmd)
        self.system(sqoopCmd,tableInfo)
        
        tableName="ods_"+dbName+"."+tableInfo.targetTableName
        targetDir=self.appInfo.namenodeUrl+"/user/hive/tmp/warehouse/ods_"+dbName+".db/"+tableInfo.realTableName

        
        overWriteStr=" "
        if tableInfo.isMutTable==1:
            overWriteStr="  "
        else:
            overWriteStr=" overwrite "
        hiveDBDict={
               "tableName":tableName,
               "targetDir":targetDir,
               "overWriteStr":overWriteStr
        }
            
        
        loadDataCmd=r''' hive -e "load data inpath '{0[targetDir]}' {0[overWriteStr]} into table {0[tableName]}  "   '''.format(hiveDBDict)
        logging.info( r"所有表第一次初始化所有数据  extractAllData: loadDataCmd %s" %  loadDataCmd)
        self.system(loadDataCmd,tableInfo)
          

    
    '''
          增量导入数据到临时表
    '''
    def extractIncrementData(self,tableInfo):
        dbName=tableInfo.dbName
        dbInfo=self.dbDict.get(dbName)
        connStr=dbInfo.toConnString()
        incrementTableName=tableInfo.realTableName+"_daily_incr"
        
        targetDir=self.appInfo.namenodeUrl+"/user/hive/tmp/warehouse/ods_"+dbName+".db/"+incrementTableName
        hadoopDbDict={
               "targetDir":targetDir
        }
        
        hdfsCmd=r'''hadoop  dfs -rm -r {0[targetDir]}  '''.format(hadoopDbDict)
        logging.info( r"extractIncrementData: hdfsCmd %s" %  hdfsCmd)
        self.system(hdfsCmd,tableInfo)
        
        
        now = datetime.datetime.now()
        zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
        
        dayHours=24*1
        lastToday = zeroToday - datetime.timedelta(hours=dayHours, minutes=0, seconds=0)
        
        
        strEndTime  = zeroToday.strftime("%Y-%m-%d %H:%M:%S") 
        strBeginTime = lastToday.strftime("%Y-%m-%d %H:%M:%S") 
        
        ####ETLTable
        whereSQL=" "
        
        #只支持时间啊，其他必错无疑  导入到临时表
        if tableInfo.incrementType==1 :
            whereDict={
                   "incrementCol":tableInfo.incrementCol,
                   "strEndTime":strEndTime,
                   "strBeginTime":strBeginTime,
                }
            whereSQL='''  where {0[incrementCol]} > "{0[strBeginTime]}" and {0[incrementCol]} <  "{0[strEndTime]}"  and $CONDITIONS '''.format(whereDict)
        
        sqoopDbDict={
               "mysqlConn":connStr,
               "username":dbInfo.userName,
               "password":dbInfo.password,
               "tableName":tableInfo.realTableName,
               "mapperCount":tableInfo.mapperCount,
               "targetDir":targetDir,
               "pkeyName":tableInfo.pkeyName,
               "whereSQL":whereSQL
            }
        
        sqoopImportCmd=r''' sqoop import --connect {0[mysqlConn]} --username  {0[username]} --password {0[password]} --split-by {0[pkeyName]} --query 'select * from {0[tableName]}    {0[whereSQL]}'  --hive-drop-import-delims --null-string '\\N' --null-non-string '\\N' --target-dir {0[targetDir]}    --fields-terminated-by  '\t'     --lines-terminated-by '\n'  '''.format(sqoopDbDict)
        logging.info( r"extractIncrementData: sqoopImportCmd %s" %  sqoopImportCmd)
        self.system(sqoopImportCmd,tableInfo)
        
        incrementTableName="ods_"+dbName+"."+tableInfo.targetTableName+"_daily_incr"
        hiveDBDict={
               "incrementTableName":incrementTableName,
               "targetDir":targetDir
        }
        
        loadDataHiveCmd=r''' hive -e " load data inpath '{0[targetDir]}'   into table {0[incrementTableName]}  "   '''.format(hiveDBDict)
        logging.info( r"extractIncrementData: loadDataHiveCmd %s" %  loadDataHiveCmd)
        self.system(loadDataHiveCmd,tableInfo)
        
          
        
        
    
    def startFetchTables(self):
        logging.info( r"startFetch etl ......")
#         tablesStr=','.join(self.tableTemplateNameList);
        for dbName,dbInfo in self.dbDict.items():
            sql=" show tables "
            fetchResult=DBHelper.query(dbInfo,sql);
            if fetchResult  is  not None:
                rowcount=fetchResult[0]
                queryResult=fetchResult[1]
                
              
                if (queryResult is not None) and rowcount>0 :
                    queryResult=sorted(queryResult)
                    #遍历所有一个数据库中所有的表，查看表名是否符合我们所配置的表
                    for tinfo in queryResult:
                        realTableName=tinfo[0].lower()
                        isConfigTable=False
                        shortTableName=realTableName
                        #如果表明不是以数字结尾的
                        tableTemplate1=  self.tableTemplateDict.get(shortTableName) 
                        if (realTableName in self.tableTemplateNameList) and (tableTemplate1 is not None) and (tableTemplate1.isMutTable==0) :
                            isConfigTable=True
                        else :
                            rr=re.match(r"(.*?)_(\d+)",realTableName, re.M|re.I)
                            #如果表明不是以数字结尾的
                            if rr is not  None:
                                shortTableName=rr.group(1)
                                if shortTableName in self.tableTemplateNameList:
                                    isConfigTable=True
                                    
                        
                        #如果符合正则，说明是我们想要配置的表
                        if isConfigTable:
                            tableTemplate=  self.tableTemplateDict.get(shortTableName)  
                            try:
                                mytable=ETLTable(dbName,realTableName,tableTemplate)
                            except Exception as e:
                                traceback.print_exc()
                            self.realEtlTableList.append(mytable)
                
    @staticmethod            
    def str2Bool(str):
        return True if str.lower() == 'true' else False    

####{0[dbName]}.
    def registUDF(self,udfConfigList):
        funSQL=r'''hive -e    " CREATE FUNCTION {0[funName]} as '{0[packageName]}'  USING JAR '{0[namenodeUrl]}{0[hdfsPath]}/{0[jarName]}'   "   '''
        while(len(udfConfigList)>0):
            udfConfig=udfConfigList.pop()
            if udfConfig is not None:
                #UDFConf   {0[targetDir]}
                ##CREATE FUNCTION default.userLivingInfo AS 'com.xinniu.recommenation.hive.udf.UserLivingInfoUDF' USING JAR 'hdfs://global-sevice-daily-4:8020/user/hive/userjars/hive-UDF-1.0-SNAPSHOT.jar'; 
                dbscom.dfu.hiveDBNames.split(",")
                dict={
                        ##"dbName":dbName,
                        "funName":udfConfig.funName,
                        "packageName":udfConfig.packageName,
                        "jarName":udfConfig.jarName,
                        "hdfsPath":udfConfig.hdfsPath,
                        "namenodeUrl":udfConfig.namenodeUrl
                    }
                cmd2=r'''hive -e " DROP FUNCTION IF EXISTS  default.%s  "  '''  %(udfConfig.funName)
                print (cmd2)
                cmd=funSQL.format(dict)
                print (cmd)
                for dbName in dbs:
                    dict={
                        "dbName":dbName,
                        "funName":udfConfig.funName,
                        "packageName":udfConfig.packageName,
                        "jarName":udfConfig.jarName,
                        "hdfsPath":udfConfig.hdfsPath,
                        "namenodeUrl":udfConfig.namenodeUrl
                    }
#                     cmd=funSQL.format(dict)
#                     cmd2=r'''hive -e " DROP FUNCTION IF EXISTS  %s.%s  "  '''  %(dbName,udfConfig.funName)
#                     cmd2=r'''DROP FUNCTION IF EXISTS  %s.%s   ;'''  %(dbName,udfConfig.funName)
#                     print (cmd2)
#                     print (cmd2)
#                     self.system(cmd, None, 0,0)
                
    
    
    
    def init(self,conf,envName):
        '''
                     初始化配置参数
        '''
        logging.info( r"init etl ......")
        
        self.envName=envName
        
        #放置数据库信息
        self.dbDict={}
        self.tableTemplateList=[]
        self.tableTemplateNameList=[]
        self.tableTemplateDict={}
        self.realEtlTableList=[]
        
        #存放所有的表字符串
        self.dbTableStrList={}
        
        self.dropAllTable=conf.get("default", "dropAllTable")
        
        registUDFOnHive=conf.get("default", "registUDFOnHive")
        
        connInfo=conf.get("default", "db.connInfo")
        infoList=connInfo.strip().split(":")
        configDBInfo=EtlDB(infoList[0],infoList[1],infoList[2],infoList[3],infoList[4])
        

        
        sql="select dbName,dbHost,dbPort,userName,password,enable  from etl_db where enable=1 "
        fetchResult=DBHelper.query(configDBInfo,sql);
        self.configDBInfo=configDBInfo
        
        
        
        if fetchResult is not None:
            rowncount=fetchResult[0]
            dbNameList=fetchResult[1]
            
            if rowncount>0 and dbNameList is not None:
                for dbrow in dbNameList:
                    dbName=dbrow[0]
                    dbHost=dbrow[1]
                    dbPort=dbrow[2]
                    userName=dbrow[3]
                    password=dbrow[4]
                    enable=dbrow[5]
                    dbInfo=EtlDB(dbName,dbHost,dbPort,userName,password,enable)
                    self.dbDict[dbName]=dbInfo
            
            
            if SqoopEtlTool.str2Bool(registUDFOnHive):
                    udfConfigList=[]
                    sql="select id,funName,packageName,jarName,hdfsPath,namenodeUrl,hiveDBNames  from udf_conf where enable=1 and needReg=1"
                    fetchResult=DBHelper.query(configDBInfo,sql);
                    if fetchResult is not None:
                        rowncount=fetchResult[0]
                        udfConfList=fetchResult[1]
    
                        if rowncount>0 and udfConfList is not None:
                            for dbrow in udfConfList:
                                sid=dbrow[0]
                                funName=dbrow[1]
                                packageName=dbrow[2]
                                jarName=dbrow[3]
                                hdfsPath=dbrow[4]
                                namenodeUrl=dbrow[5]
                                hiveDBNames=dbrow[6]
                                udfConfig=UDFConf(sid,funName,packageName,jarName,hdfsPath,namenodeUrl,hiveDBNames)
                                udfConfigList.append(udfConfig)
                    if len(udfConfigList)>0:
                        self.registUDF(udfConfigList);
                        logging.warn("CREATE  udf FUNCTION finish!!!")
                    sys.exit(0)
                        
                    
        
        sql='''select a.id, a.tableName, a.isMutTable, a.mergeCol, a.incrementCol, 
        a.createTable, a.etlAllData, a.torder, a.mapperCount,a.pkeyName,a.incrementType,a.etlIncreamData, 
        a.tableSubName,  b.dbName
               from etl_table_template  a  left join etl_db b 
               on a.dbId=b.id  where a.enable=1  
               order by a.torder desc , b.torder desc 
         '''
        fetchResult=DBHelper.query(configDBInfo,sql);
        
        if fetchResult is not None:
            rowncount=fetchResult[0]
            tableNameList=fetchResult[1]
            
            if rowncount>0 and tableNameList is not None:
                for dbrow in tableNameList:
                    ids=dbrow[0]
                    tableName=dbrow[1]
                    isMutTable=dbrow[2]
                    mergeCol=dbrow[3]
                    incrementCol=dbrow[4]
                    createTable=dbrow[5]
                    etlAllData=dbrow[6]
                    torder=int(dbrow[7])
                    mapperCount=int(dbrow[8])
                    pkeyName=dbrow[9]
                    incrementType=dbrow[10]
                    etlIncreamData=int(dbrow[11])
                    tableSubName=dbrow[12]
                    dbName=dbrow[13]
                    self.tableTemplateNameList.append(tableName)
                    
                    tempTable=EtlTableTemplate(ids,tableName,dbName,isMutTable,mergeCol,incrementCol,createTable,etlAllData,torder,pkeyName,incrementType,etlIncreamData,tableSubName,mapperCount)
                    self.tableTemplateDict[tableName]=tempTable
                    
        
        
        logging.info( r"当前环境为:  %s" % envName)
        sql="select id,etlLogPath,newDataTempDir,namenodeUrl   from app_config  where envName='%s' limit 1 "  % self.envName
        fetchResult=DBHelper.query(configDBInfo,sql);
        
        if fetchResult is not None:
            rowncount=fetchResult[0]
            dbNameList=fetchResult[1]
            
            if rowncount>0 and dbNameList is not None:
                for dbrow in dbNameList:
                    ids=dbrow[0]
                    etlLogPath=dbrow[1]
                    newDataTempDir=dbrow[2]
                    namenodeUrl=dbrow[3]
    
                    appInfo=AppInfo(ids,etlLogPath,newDataTempDir,namenodeUrl)
                    self.appInfo=appInfo
        
        now=datetime.datetime.now()
        dataDict={
            "gmt_create":now,
            "gmt_modify":now
            }
        DBHelper.insert(configDBInfo,"exe_batch_info",dataDict);
        batchNumIn=random.randint(100000,900000)
        fetchResult=fetchResult=DBHelper.query(configDBInfo,"select max(batchNum) from exe_batch_info");
        if  fetchResult is not None:
            rowncount=fetchResult[0]
            batchNumList=fetchResult[1]
            
            if rowncount>0 and batchNumList is not None:
                for dbrow in batchNumList:
                    batchNumIn=int(dbrow[0])
        
        self.batchNumIn=batchNumIn
        
        logging.info( r"init db finish ......")
    
    def endFetch(self):
        currentPath=os.path.abspath(os.path.join(os.getcwd(), "."))
        os.system("rm -rf  %s/*.java" % currentPath)
        logging.info( r"endFetch etl ......")
        logging.info( r"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    currentPath=os.path.abspath(os.path.join(os.getcwd(), "."))
    os.system("rm -rf  %s/*.java" % currentPath)
    parser = OptionParser(usage="%prog -f server.list -u root ...  versrion 1",version="%prog 1")
    parser.add_option("-e", "--envName",action="store",dest="envName",help="环境是测试还是线上：dev,test,production",default="all")
    (options, args) = parser.parse_args()
    
    envName=options.envName
    logging.info("当前配置环境为envName==>  "+envName)
    sys.path.append(currentPath)
    conFile="./conf/app-"+envName+".conf"
    conf = ConfigParser.SafeConfigParser()
    conf.read(conFile)
    etlPathStr=conf.get("default", "etlToolEnv.path")
    libPathStr=conf.get("default", "etlTool.lib")
    cdhHadoopHome=conf.get("default", "cdhHadoop.home")
    
    mypath=os.path.abspath(os.path.join(os.getcwd(), "./com"))
    sys.path.append(mypath)
    mypath=os.path.abspath(os.path.join(os.getcwd(), "./conf"))
    sys.path.append(mypath)
    
    ##将各种环境path追加进入python环境
    etlPathList=etlPathStr.split(";")
    libPathList=libPathStr.split(";")
    etlPathList.extend(libPathList)
    
    
    for path in etlPathList:
        path="%s/%s" % (cdhHadoopHome,path.strip())
        if path is not None:
            sys.path.append(path)
            print  path
    



  
    
    reload(sys)     
    sys.setdefaultencoding('utf-8')
    etl=SqoopEtlTool()
    etl.init(conf,envName)
    etl.startFetchTables()
    etl.startEtl()
    etl.endFetch()
