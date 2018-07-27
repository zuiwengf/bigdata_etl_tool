#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 2018年7月17日
@author: zuiweng.df
@summary: 数据库查询工具
'''


import datetime
import os
import re
import  subprocess
import sys
import traceback
import logging

from DBUtils.PooledDB import PooledDB
import MySQLdb


class DBHelper(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    @staticmethod
    def query(dbInfo,sql):
        fetchResult=None
        pool=None
        conn=None
        rowcount=0
        try:
            pool = PooledDB(MySQLdb,2,host=dbInfo.dbHost,user=dbInfo.userName,passwd=dbInfo.password,db=dbInfo.dbName,port=int(dbInfo.dbPort)) 
            conn = pool.connection()  
            cursor=conn.cursor()
            cursor.execute(sql)
            fetchResult=cursor.fetchall()
            rowcount=cursor.rowcount
            if rowcount > 0 :
#                 print ("DBHelper query sql success! "+sql)
                pass
            if cursor is not None:
                cursor.close()
        except Exception as e:
            logging.error('DBHelper query sql fail! sql ： %s   , reason %s ' % (sql,str(e)))
            traceback.print_exc()
        finally:
            if conn is not None:
                conn.close()
            if pool is not None:
                pool.close()
        return (rowcount,fetchResult)
    
    
    @staticmethod
    def insert(dbInfo,tableName,dataDict):
        pool=None
        conn=None
        try:
            dataValues = "(" + "%s," * (len(dataDict)) + ")"
            dataValues = dataValues.replace(',)', ')')
            dbField = dataDict.keys()
            dataTuple = tuple(dataDict.values())
            dbField = str(tuple(dbField)).replace("'",'')
            pool = PooledDB(MySQLdb,2,host=dbInfo.dbHost,user=dbInfo.userName,passwd=dbInfo.password,db=dbInfo.dbName,port=int(dbInfo.dbPort)) 
            conn = pool.connection() 
            cursor = conn.cursor()
            sql = """ insert into %s %s values %s """ % (tableName,dbField,dataValues)
            params = dataTuple
            cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            return 1
    
        except Exception as e:
            logging.error('DBHelper insert sql fail! sql ： %s   , reason %s ' % (sql,str(e)))
            traceback.print_exc()
            return 0
        
        finally:
            if conn is not None:
                conn.close()
            if pool is not None:
                pool.close()
                
                
        
        
    '''
        此方法未测试，清无用。忙.......................
    '''   
    @staticmethod
    def update(dbInfo,sql):
        pool=None
        conn=None
        try:
            pool = PooledDB(MySQLdb,2,host=dbInfo.dbHost,user=dbInfo.userName,passwd=dbInfo.password,db=dbInfo.dbName,port=int(dbInfo.dbPort)) 
            conn = pool.connection() 
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return 1
    
        except Exception as e:
            logging.error('DBHelper update sql fail! sql ： %s   , reason %s ' % (sql,str(e)))
            traceback.print_exc()
            return 0
        
        finally:
            if conn is not None:
                conn.close()
            if pool is not None:
                pool.close()
        