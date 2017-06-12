# -*- coding: utf-8 -*-
from django.db import models
from mongoengine import *

DB_ALIAS = {"db_alias" : "pbl"}

#test用
class test(Document):
    _id         = StringField(max_length=255)
    temperature = FloatField()
    moisture    = FloatField()
    datetime    = StringField(max_length=255)
    test        = StringField(max_length=255)

    meta = DB_ALIAS

class collect_data(Document):
    _id         = StringField(max_length=255)
    datetime    = DateTimeField()
    temperature = FloatField()
    moisture    = FloatField()
    illuminance = FloatField()

    meta = DB_ALIAS

class collect_memo(Document):
    _id         = StringField(max_length=255)
    datetime    = StringField(max_length=255)
    memo        = StringField()

    meta = DB_ALIAS

class threshold(Document):
    _id         = StringField(max_length=255)
    threshold   = StringField(max_length=255)

    meta = DB_ALIAS

class watertime(Document):
    _id         = StringField(max_length=255)
    datetime   = DateTimeField()

    meta = DB_ALIAS

class mailaddress(Document):
    _id         = StringField(max_length=255)
    nowaddress  = StringField(max_length=255)
    newaddress  = StringField(max_length=255)
    randstr     = StringField(max_length=255)

    meta = DB_ALIAS
