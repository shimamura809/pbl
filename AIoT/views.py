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
  dataset += db.collect_data.find({"datetime":{"$lte":dt}}).sort("datetime", DESCENDING).limit(1)
  return render_to_response('AIoT/datalist.html', {"dataset":dataset,"data_len":len(dataset)})


# 詳細画面 http://127.0.0.1:8000/AIoT/detail/20161031
def detail(request):
    dt = request.GET.get('datetime', 'now')
    memo_data = []
    memo_data += db.collect_memo.find({"datetime":dt}).sort("datetime", ASCENDING)
    memo = []
    if len(memo_data) > 0:
      for i in range(len(memo_data[0]["memo"])):
        memo.append("" + memo_data[0]["memo"][i])
    if dt == 'now':
        gt = dt_from_14digits_to_iso("20161027000000")
    else:
        gt = dt_from_14digits_to_iso(dt+"000000")
    lt = gt + timedelta(hours = 23, minutes = 50)
    dataset = []
    dataset += db.collect_data.find({"datetime":{"$gte":gt, "$lte":lt}}).sort("datetime", ASCENDING)
    return render_to_response('AIoT/detail.html', {"dataset":dataset,"data_len":len(dataset),"datetime":gt, "memo_data":memo})

def detail_json(request):
  #urlから各値を取得
  memo = request.GET.get('memo', '').split(",")
  for i in range(len(memo)):
    memo[i] = str(memo[i])
  datetime = request.GET.get('datetime', '')
  #同日のメモを削除
  db.collect_memo.remove({"datetime":datetime})
  #メモをDBに保存
  db.collect_memo.insert({"memo":memo, "datetime":datetime})

  dataset = {"memo":memo}
  return render_json_response(request,dataset)

def dt_from_14digits_to_iso(dt):
  from datetime import datetime
  dt = str(dt[0:4])+"-"+str("0"+dt[4:6])[-2:]+"-"+str("0"+dt[6:8])[-2:]+" "+str("00"+dt[8:10])[-2:]+":"+str("00"+dt[10:12])[-2:]+":"+str("00"+dt[12:14])[-2:]
  dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
  return dt

# JSON出力
def render_json_response(request, data, status=None): # response を JSON で返却

  json_str = json.dumps(data, ensure_ascii=False, indent=2)
  callback = request.GET.get('callback')
  if not callback:
      callback = request.REQUEST.get('callback')  # POSTでJSONPの場合
  if callback:
      json_str = "%s(%s)" % (callback, json_str)
      response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
  else:
      response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
  return response