# encoding = utf-8

import json
import time
import hashlib
import datetime

def text_to_json(data):
    return json.loads(data)

def json_to_text(data, ascii=True):
    return json.dumps(data, ensure_ascii=ascii)

def empty(variable):
    if variable == None:
        return True
    elif type(variable) == int or type(variable) == float:
        if variable == 0:
            return True
        return False
    elif len(variable) == 0:
        return True
    return False

def get_md5(text):
    data = hashlib.md5()
    data.update(text.encode('utf-8'))
    return data.hexdigest()

def get_now_year():
    return datetime.datetime.now().year

def timestamp_to_date(timestamp):
    return time.strftime("%Y/%m/%d", time.localtime(timestamp))

def date_to_timestamp(date):
    return int(time.mktime(time.strptime(date, '%Y/%m/%d')))