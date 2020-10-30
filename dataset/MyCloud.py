# -*- coding: utf-8 -*-
import pymysql
import datetime

from  MyLog import mylog

class MyCloudData:
  def __init__(self):
    """create a class for tencent mysql cloud"""
    self.conn = None
    self.cursor =None
    self.table = []
    pass
  
  def __del__(self):
    self.conn.close()

  def init(self,host="cdb-mqzvz536.bj.tencentcdb.com",port=10146,user='visitor',password='visitor'):
    self.conn = pymysql.connect(host=host,port =port,user=user,password=password)
    self.cursor=self.conn.cursor()
    self.cursor.execute("use stock_data;")
    tablename = self.cursor.execute("show tables ").fetchall()
    self.tables = [ i[0] for i in tablename]
  
  def has_table(self,table_name):
    return table_name in self.tables

  def create_table(self,table_name,structs):
    self.exec("create table {} ({})".format(table_name,structs))
    self.tables.append(table_name)
  
  def exec(self,command):
    mylog.log("execute command : {}".format(command),'Log')
    if(type(command)==list):
      self.cursor.executemany(command)
    else:
      self.cursor.execute(command)
    data = self.cursor.fetchall()
    return data

