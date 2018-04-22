#! /usr/bin/env
#coding=utf-8

import MySQLdb
import threading

class MysqlHandler():
    def __init__(host, user, password, database, charset='utf-8'):
        for i in range(0,10):
            conn = MySQLdb.connect(host, user, password, database, charset='utf-8')
            self.cursors.append(self.conn.cursor())
        self.mutex = threading.Lock()
        self.used_cursors = []

    def GetFreeCursor():
        i = -1
        self.mutex.acquire
        for i in range(len(self.cursors)):
            if (i not in self.used_cursors):
                self.used_cursors.append(i)
                break
        self.mutex.release()
        return i

    def FreeCursor(k):
        if (k in self.used_cursors):
            self.used_cursors.remove(k)

    def GetDocIdList(termList):
        docList = []
        k = self.GetFreeCursor()
        cursor = self.cursors[k]
        for term in termList:
            n = cursor.execute("SELECT id FROM house WHERE title like '\%%s\%'")
            for row in cursor.fetchall():
                docList.append(row)
        self.FreeCursor(k)
        return docList

    def GetContent(docList):
        sql = "SELECT title, content from house WHERE id in ("
        firstFlag = true
        for doc in docList:
            if (firstFlag):
                sql += str(doc)
                firstFlag = false
                continue
            sql += ',' + str(doc)
        sql += ')'
        k = self.GetFreeCursor()
        cursor = self.cursors[k]
        n = cursor.execute(sql)
        contentList = []
        for row in cursor.fetchall():
            pass
