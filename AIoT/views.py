# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from AIoT.models import test, collect_data
from mongoengine import *
from pymongo import *
import requests

import json
import math
from datetime import datetime, timedelta
import locale

client = MongoClient()
db = client.pbl

# データリスト画面 http://127.0.0.1:8000/AIoT/datalist/
def datalist(request):
  dt = datetime.now()
  dataset = []
  dataset += db.collect_data.find({"datetime":{"$lte":dt}}).sort("datetime", DESCENDING)
  return render_to_response('AIoT/datalist.html', {"dataset":dataset,"data_len":len(dataset)})


# 詳細画面 http://127.0.0.1:8000/AIoT/detail/20161031
def detail(request):
    dt = request.GET.get('datetime', 'now')
    if dt == 'now':
        gt = dt_from_14digits_to_iso("20161027000000")
        print(dt)
    else:
        gt = dt_from_14digits_to_iso(dt+"000000")
        print("query")
    lt = gt + timedelta(hours = 23, minutes = 50)
    print(lt)
    dataset = []
    dataset += db.collect_data.find({"datetime":{"$gte":gt, "$lte":lt}}).sort("datetime", ASCENDING)
    return render_to_response('AIoT/detail.html', {"dataset":dataset,"data_len":len(dataset)})

def dt_from_14digits_to_iso(dt):
  from datetime import datetime
  dt = str(dt[0:4])+"-"+str("0"+dt[4:6])[-2:]+"-"+str("0"+dt[6:8])[-2:]+" "+str("00"+dt[8:10])[-2:]+":"+str("00"+dt[10:12])[-2:]+":"+str("00"+dt[12:14])[-2:]
  dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
  return dt