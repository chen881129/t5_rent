#! /usr/bin/env python
#coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler
import MySQLdb
from MysqlHandler import MysqlHandler

import simplejson
import cgi
import jieba
from conf import *

class TodoHandler(BaseHTTPRequestHandler):
    """A simple TODO server
 
    which can display and manage todos for you.
    """
 
    # Global instance to store todos. You should use a database in reality.
    TODOS = MysqlHandler(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    jieba.initialize()
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.mysqlHandler = []
 
    def do_GET(self):
        # return all todos
 
        if self.path != '/':
            self.send_error(404, "File not found.")
            return
 
        # Just dump data to json, and return it
        message = simplejson.dumps(self.TODOS)
 
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(message)
 
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
