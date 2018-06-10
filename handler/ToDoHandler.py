#! /usr/bin/env python
#coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler
import MySQLdb
from handler.MysqlHandler import MysqlHandler

import simplejson
import cgi
import jieba
from conf import *

class TodoHandler(BaseHTTPRequestHandler):
    """A simple TODO server
 
    which can display and manage todos for you.
    """
    list_json = '{"retcode":5,"result":[{"id":1,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0,"pic":"http://pic1.58cdn.com.cn/anjuke_58/92c2d0cf7e65d888729c3b2fb664df76?w=640&h=480&crop=1"},{"id":2,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0,"pic":"http://pic3.58cdn.com.cn/anjuke_58/14d4f6e0a12cc24f93afb6bd41f95318?w=640&h=480&crop=1"},{"id":3,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0,"pic":"http://pic3.58cdn.com.cn/anjuke_58/16a4846a6fddfe2aebfee5dcb789e7d2?w=640&h=480&crop=1"},{"id":4,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0,"pic":"http://pic3.58cdn.com.cn/anjuke_58/1c5ce20ab5720a69c47549a0f2f1e3fa?w=640&h=480&crop=1"},{"id":5,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0,"pic":"http://pic2.58cdn.com.cn/anjuke_58/f34ec6e33a2e7593edfa35782505602b?w=640&h=480&crop=1"}]}'
    detail_json = '{"id":1,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0,"pic":"http://pic1.58cdn.com.cn/anjuke_58/92c2d0cf7e65d888729c3b2fb664df76?w=640&h=480&crop=1","room":[{"area":14.6, "faceto":"北", "tenent":{"college":"北京交通大学", "age": 28, "sex":"男"}, "price": 1400.00},{"area":13.6, "faceto":"北", "tenent":{"college":"北京科技大学", "age": 27, "sex":"男"}, "price": 1300.00},{"area":11.6, "faceto":"北", "tenent":{"college":"北京航空航天大学", "age": 28, "sex":"男"}, "price": 1200.00}]}'
    # Global instance to store todos. You should use a database in reality.
    #TODOS = MysqlHandler(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    jieba.initialize()
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.mysqlHandler = []
 
    def do_GET(self):
        # return all todos
 
 
        # Just dump data to json, and return it
        pos = self.path.find("?")
        if (True):
            operation = self.path[0:pos]
            param = self.path[pos+1:len(self.path)]
            print "ok"
            if self.path.find('house_list') != -1:
                #message = simplejson.dumps(self.list_json)
     
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(self.list_json)
                return
            elif self.path.find('house_detail') != -1:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(self.detail_json)
                return
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('{"retcode":-1,"result":[]}')
 
    def do_POST(self):
        """Add a new todo
 
        Only json data is supported, otherwise send a 415 response back.
        Append new todo to class variable, and it will be displayed
        in following get request
        """
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            post_values = simplejson.loads(self.rfile.read(length))
            self.TODOS.append(post_values)
        else:
            self.send_error(415, "Only json data is supported.")
            return
 
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
 
        self.wfile.write(post_values)
