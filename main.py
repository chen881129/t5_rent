#! /usr/bin/env python
#coding=utf-8

from BaseHTTPServer import HTTPServer
from handler.ToDoHandler import TodoHandler
import MySQLdb
from conf import *

def main():
    server = HTTPServer(('0.0.0.0', LISTEN_PORT), TodoHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()

if __name__ == '__main__':
    main()
