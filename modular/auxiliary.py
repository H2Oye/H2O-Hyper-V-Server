# -*- coding: utf-8 -*-
# Author: XiaoXinYo

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

def empty_many(*variable):
    for variable_count in variable:
        if empty(variable_count):
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

def get_middle_text(text, text_left='', text_right=''):
    if not text_left:
        return text.split(text_right)[1]
    if not text_right:
        return text.split(text_left)[1]
    try:
        data = text.split(text_left)[1].split(text_right)[0]
    except Exception:
        data = ''
    return data

def split_dict(data, size):
	list_d = []
	dict_len = len(data)
	# 获取分组数
	while_count = dict_len // size + 1 if dict_len % size != 0 else dict_len / size
	split_start = 0
	split_end = size
	while(while_count > 0):
		# 把字典的键放到列表中,根据偏移量拆分字典
		list_d.append({k: data[k] for k in list(data.keys())[split_start:split_end]})
		split_start += size
		split_end += size
		while_count -= 1
	return list_d