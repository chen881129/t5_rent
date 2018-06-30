#! /usr/bin/env python
#coding=utf-8

from BaseHTTPServer import HTTPServer
from handler.ToDoHandler import TodoHandler
import MySQLdb
import sys
from conf import *

def main():
    port = LISTEN_PORT
    if (len(sys.argv) == 2):
        port = int(sys.argv[1])
    server = HTTPServer(('0.0.0.0', port), TodoHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()

if __name__ == '__main__':
    main()
