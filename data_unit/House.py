#! /usr/bin/env/python
#coding=utf-8

import Room

FACE_TO = ['北', '南', '西', '东']
FITMENT = ['精装修', '中装修', '简单装修', '毛坯']

class House:
                       #id, title, subdistrict, faceto, floor, year, dinner_num, room_num, fitment, area, pic
    def __init__(self, id, title, subdistrict, faceto, floor, year, dinner_num, room_num, fitment, area, other_discreption, room, pic):
        self.id_ = id
        self.title_ = title
        self.subdistrict_ = subdistrict
        self.faceto_ = faceto
        self.floor_ = floor
        self.year_ = year
        self.dinner_num_ = dinner_num
        self.room_num_ = room_num
        self.fitment_ = fitment
        self.area_ = area
        self.other_discreption_ = other_discreption
        self.room_ = room
        self.pic_ = pic

    def to_dict(self):
        ret_dict = {'id':self.id_, 'title':self.title_, 'subdistrict':self.subdistrict_, 'faceto':self.convert_faceto(self.faceto_), 'floor':self.floor_, 'year':self.year_, 'dinner_num':self.dinner_num_, 'room_num':self.room_num_, 'fitment':self.convert_fitment(self.fitment_), 'area':self.area_, 'other_discreption':self.other_discreption_, 'room':self.room_, 'pic':self.pic_}
        return ret_dict

    def convert_faceto(self, faceto):
        return FACE_TO[faceto]
    def convert_fitment(self, fit):
        return FITMENT[fit]
