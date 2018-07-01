#! /usr/bin/env python
#coding=utf-8

from handler.ProcessHandler import ProcessHandler
import tornado.ioloop
import tornado.web
import MySQLdb
import sys
from conf import *

def make_app():
    return tornado.web.Application([
        (r"/t5_rent_dev/.*", ProcessHandler),
    ])

def main():
    port = LISTEN_PORT
    if (len(sys.argv) == 2):
        port = int(sys.argv[1])
    app = make_app()
    app.listen(port)
    print("Starting server, use <Ctrl-C> to stop")
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
