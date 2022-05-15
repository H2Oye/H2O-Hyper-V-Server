# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import make_response
from modular import auxiliary
import os
import base64

def get_root_path():
    return os.path.abspath(os.path.join(__file__, '../..')) + '/'

def read(name):
    with open(f'{get_root_path()}data/{name}.json', encoding='utf-8') as file:
        data = file.read()
    return auxiliary.text_to_json(data)

def write(name, data):
    with open(f'{get_root_path()}data/{name}.json', 'w', encoding='utf-8') as file:
        file.write(auxiliary.json_to_text(data))

def get_request_parameter(request):
    data = {}
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.form
        if not data:
            data = request.get_json()
    return dict(data)

def generate_response_json_result(information, state=200):
    data = {
        'state': state,
        'information': information
    }
    data = auxiliary.json_to_text(data, False)
    response = make_response(data)
    response.mimetype = 'application/json; charset=utf-8'
    return response

def generate_layui_response_json_result(information):
    data = {
        'code': 0,
        'msg': '',
        'count': len(information),
        'data': information
    }
    data = auxiliary.json_to_text(data, False)
    response = make_response(data)
    response.mimetype = 'application/json; charset=utf-8'
    return response

def get_core(key):
    return read('core')[key]

def set_core(key, value):
    data = read('core')
    data[key] = value
    write('core', data)

def get_notice():
    return str(base64.b64decode(get_core('notice')), 'utf-8').split('\n')