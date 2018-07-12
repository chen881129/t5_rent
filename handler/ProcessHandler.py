#! /usr/bin/env python
#coding=utf-8

import tornado.ioloop
import tornado.web

from urllib import unquote
import MySQLdb
from handler.MysqlHandler import MysqlHandler
from data_unit.House import House
import simplejson
import cgi
import jieba
import redis
import time
import datetime
from conf import *
import jwt
import Crypto.PublicKey.RSA as RSA, datetime

NO_RESULT = 'no result'

class ProcessHandler(tornado.web.RequestHandler):
    # Global instance to store todos. You should use a database in reality.
    jieba.initialize()
    #mysqlHandler = MysqlHandler('localhost', 'root', 'Aqaz123!', 't5_rent')
    mysqlHandler = MysqlHandler(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)

    detail_json = ""
    with open('/root/product/t5_rent/room_data') as fd:
        txt = fd.read().replace('\n','')
        detail_json = txt.decode('gbk').encode('utf-8')
    key = RSA.generate(2048)
    priv_pem = key.exportKey()
    pub_pem = key.publickey().exportKey()
    priv_key = RSA.importKey(priv_pem)
    pub_key = RSA.importKey(pub_pem)
 
    def send_res(self, result):
        final_result = '{"retcode":-1,"result":[]}';
        if (result != NO_RESULT):
            final_result = result
        self.write(final_result)

    def check_user(self, claims):
        return True

    def get(self):
        # return all todos
 
 
        # Just dump data to json, and return it
        operation = self.request.uri
        '''
        try:
            token = self.get_argument('token')
        except:
            payload = { 'site': 'zhiliaohou.online', 'name': 'litong'}
            token = jwt.generate_jwt(payload, self.priv_key, 'RS256', datetime.timedelta(minutes=5))
            self.send_res('{"token":"%s"}' % token)
            return
        if (token == None or token == ""):
            self.send_res(NO_RESULT)
            return 
        else:
            try:
                header, claims = jwt.verify_jwt(token, self.pub_key, ['RS256'])
            except:
                self.send_res(NO_RESULT)
                return
            if (self.check_user(claims) is False):
                self.send_res(NO_RESULT)
                return
        '''
        t1 = int(time.time()*1000)
        if operation.find('house_list') != -1:
            result_list = []
            try:
                queryString = self.get_argument('query')
                print queryString
                seg_list = jieba.cut_for_search(unquote(queryString), HMM=False)
                print seg_list
            except:
                seg_list = None
            print seg_list
            doclist = self.mysqlHandler.GetDocIdList(seg_list)
            ret_dic = []
            for doc in doclist:
                print doc
            docs = self.mysqlHandler.GetContent(doclist)
            for doc in docs:
                (id, title, subdistrict, faceto, floor, year, dinner_num, room_num, fitment, area, pic) = doc
                house = House(id, title, subdistrict, faceto, floor, year, dinner_num, room_num, fitment, area, "", "", pic)
                house_dic = house.to_dict()
                result_list.append(house_dic)
            final_result = {'retcode':len(result_list), 'result': result_list}
            json_result = simplejson.dumps(final_result)
            #print json_result
            #send_str = str(simplejson.loads(json_result)).decode('utf8').encode('raw_unicode_escape')
            #print send_str
            self.send_res(json_result)
            t2 = int(time.time()*1000)
            print "[%s] cost=%d,ret=%d" % ((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), t2 - t1, len(result_list))
            return
        elif operation.find('house_detail') != -1:
            self.send_res(self.detail_json)
            t2 = int(time.time()*1000)
            print "[%s] cost=%d,ret=%d" % ((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), t2 - t1, 0)
            return
 
