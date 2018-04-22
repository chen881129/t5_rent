#! /usr/bin/env python
#coding=gbk

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
 
    # Global instance to store todos. You should use a database in reality.
    #TODOS = MysqlHandler(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    list_json= u'{"retcode":5,[{"id":1,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0},{"id":2,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0},{"id":3,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0},{"id":4,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0},{"id":5,  "title":"大钟寺大柳树皂君庙东里单间2500元农科院铁科院交通大学财经大学", "subdistrict":"皂君东里","faceto":"北","floor":3,"year":1999,"dinner_num":1,"room_num":3,"fitment":"中装修","area":84.0}]}'
    jieba.initialize()
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.mysqlHandler = []
 
    def do_GET(self):
        # return all todos
 
 
        # Just dump data to json, and return it
        pos = self.path.find("?")
        if (pos != -1):
            operation = self.path[0:pos]
            param = self.path[pos+1:len(self.path)]
            if operation == "/house_list":
                message = simplejson.dumps(self.list_json)
     
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(message)
                return
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(simplejson.dumps('{"retcode":-1,[]}'))
 
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
