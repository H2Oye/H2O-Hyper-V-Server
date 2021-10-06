# encoding = utf-8

from flask import make_response
from modular import auxiliary
import os

def get_root_path():
    return os.path.abspath(os.path.join(__file__, '../..')) + '/'

def read(name):
    with open(get_root_path() + 'data/' + name + '.json', encoding='utf-8') as file:
        data = file.read()
    return auxiliary.text_to_json(data)

def write(name, data):
    with open(get_root_path() + 'data/' + name + '.json', 'w', encoding='utf-8') as file:
        file.write(auxiliary.json_to_text(data))

def get_request_parameter(request):
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.form
        if not data:
            data = request.get_json()
        if not data:
            data = {}
    return dict(data)

def get_core(key):
    return read('core')[key]

def set_core(key, value):
    data = read('core')
    data[key] = value
    write('core', data)