#! /usr/bin/env
#coding=utf-8

import MySQLdb
import threading
import redis

class MysqlHandler():
    def __init__(self, host, user, password, database, charset='utf8'):
        self.conn = MySQLdb.connect(host, user, password, database, charset = charset)
        self.redisHandler = redis.Redis(host='localhost',port=6379,db=0)

    def GetDocIdList(self, termList):
        docList = []
        cursor = self.conn.cursor()
        print termList
        for term in termList:
            docInRedis = self.redisHandler.smembers(term)
            docListTerm = []
            if len(docInRedis) is 0:
                sql = "SELECT id FROM house WHERE title like '%%%s%%'" % term
                print sql
                n = cursor.execute(sql)
                for row in cursor.fetchall():
                    docListTerm.append(row[0])
                for doc in docListTerm:
                    self.redisHandler.sadd(term, doc)
            else:
                docListTerm = [doc for doc in docInRedis]
            docList.extend(docListTerm)
        docSet = set(docList)
        finalList = [doc for doc in docSet]
        return finalList

    def GetContent(self, docList):
        if len(docList) is 0:
            return []
        sql = "SELECT id, title, subdistrict, faceto, floor, year, dinner_num, room_num, fitment, area, pic from house WHERE id in ("
        firstFlag = True
        for doc in docList:
            if (firstFlag):
                sql += str(doc)
                firstFlag = False
                continue
            sql += ',' + str(doc)
        sql += ')'
        print sql
        cursor = self.conn.cursor()
        n = cursor.execute(sql)
        contentList = []
        for row in cursor.fetchall():
            contentList.append(row)
        return contentList
