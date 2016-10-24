# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from AIoT.models import test
from mongoengine import *
from pymongo import *
import requests

import json
import math
from datetime import datetime
import locale

client = MongoClient()
db = client.pbl

# データリスト画面 http://127.0.0.1:8000/AIoT/datalist/
def datalist(request):
  dt = str(datetime.now())
  dataset = []
  dataset += db.test.find({"datetime":{"$lte":dt}, "test":"aaaaa"}).sort("datetime", DESCENDING)
  return render_to_response('AIoT/datalist.html', {"dataset":dataset,"data_len":len(dataset)})