# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from AIoT.models import test, collect_data
from mongoengine import *
from pymongo import *
import requests
import os.path
import os
from waterorder import *

import json
import math
from datetime import datetime, timedelta
import locale

client = MongoClient()
db = client.pbl

# データリスト画面 http://127.0.0.1:8000/AIoT/datalist/
def datalist(request):
  dt = datetime.now()
  memo_dt = str(dt.year) + ("0"+str(dt.month))[-2:] + ("0"+str(dt.day))[-2:]
  water_gt = dt_from_14digits_to_iso(memo_dt + "000000")
  memo_data = []
  memo_data += db.collect_memo.find({"datetime":memo_dt}).sort("datetime", ASCENDING)
  memo = []
  if len(memo_data) > 0:
    for i in range(len(memo_data[0]["memo"])):
      memo.append("" + memo_data[0]["memo"][i])
  threshold = []
  threshold += db.threshold.find()
  if db.threshold.count() == 0:
    threshold = ""
  else:
    threshold = threshold[0]["threshold"]
  dataset = []
  dataset += db.collect_data.find({"datetime":{"$lte":dt}}).sort("datetime", DESCENDING).limit(1)
  raw_watertime = []
  raw_watertime += db.watertime.find({"datetime":{"$gte":water_gt, "$lte":dt}}).sort("datetime", ASCENDING)
  watertime = []
  # print(raw_watertime[0]["datetime"].minute)
  if len(raw_watertime) != 0:
    for time in raw_watertime:
      watertime.append(str(time["datetime"].hour) + "時" + str(time["datetime"].minute) + "分" + str(time["datetime"].second) + "秒")
  return render_to_response('AIoT/datalist.html', {"dataset":dataset,"data_len":len(dataset),"datetime":dt,"memo_data":memo,"threshold":threshold,"watertime":watertime})

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
      dt = datetime.now()
      dt = str(dt.year) + ("0"+str(dt.month))[-2:] + ("0"+str(dt.day))[-2:]
      gt = dt_from_14digits_to_iso(dt + "000000")
    else:
        gt = dt_from_14digits_to_iso(dt+"000000")
    lt = gt + timedelta(hours = 23, minutes = 50)
    picture = os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/../media/'+dt+".jpg")
    dataset = []
    dataset += db.collect_data.find({"datetime":{"$gte":gt, "$lte":lt}}).sort("datetime", ASCENDING)
    raw_watertime = []
    raw_watertime += db.watertime.find({"datetime":{"$gte":gt, "$lte":lt}}).sort("datetime", ASCENDING)
    print(dataset)
    print(raw_watertime)
    return render_to_response('AIoT/detail.html', {"dataset":dataset,"data_len":len(dataset),"datetime":gt, "memo_data":memo, "picture":picture,"pic_dt":dt,"watertime":raw_watertime})

# 画像一覧用の関数
def pict_list(request):
  # pict_list = []
  pict_list = os.listdir(os.path.dirname(os.path.abspath(__file__)) + '/../media/')
  pict_list.remove('no_data.jpg')
  pict_list.remove('zu1.jpg')
  print(pict_list)
  for i in range(len(pict_list)):
    pict_list[i] = (pict_list[i].split(".jpg"))[0]
  pict_list.sort()
  print(pict_list)
  return render_to_response('AIoT/pict_list.html', {"pict_list":pict_list})

#取得データ一覧用
def getdata(request):
  dt = datetime.now()
  dataset = []
  dataset += db.collect_data.find({"datetime":{"$lte":dt}}).sort("datetime", DESCENDING)
  return render_to_response('AIoT/getdata.html', {"dataset":dataset})

#メモ保存用
def memo_json(request):
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

#閾値更新用関数
def threshold_json(request):
  #urlから値を取得
  threshold = request.GET.get('threshold', '10')
  print(threshold)
  #現在の閾値をを削除
  db.threshold.remove()
  #閾値をDBに保存
  db.threshold.insert({"threshold":threshold})
  print("test")

  dataset = {"threshold":threshold}
  return render_json_response(request,dataset)

#水遣り命令用関数
def water_json(request):
  #urlから値を取得
  water = request.GET.get('water', '')
  order(water)
  # 水遣り時刻をDBに保存
  if water == "ON":
    dtstr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    dt = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
    db.watertime.insert({"datetime":dt})

  dataset = {"water":water}
  return render_json_response(request,dataset)

#時刻の形式変換関数（14文字の文字列→ISO形式）
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