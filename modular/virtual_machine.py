# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import core, auxiliary, hyper_v
import time

def get():
    return core.read('virtual_machine')

def is_due(name):
    if int(time.time()) > get_due_timestamp(name):
        return True
    return False

def set(name, key, value):
    data = get()
    if name not in data:
        data[name] = {}
    data[name][key] = value
    core.write('virtual_machine', data)

def get_account_number(name):
    if name in get():
        return get().get(name).get('account_number', '未分配')
    return '未分配'

def get_due_timestamp(name):
    if name in get():
        due_timestamp = get().get(name).get('due_timestamp', '永久')
        if due_timestamp == '永久':
            return 3093527923200
        return due_timestamp
    return 3093527923200

def get_due_date(name):
    if name in get():
        due_timestamp = get().get(name).get('due_timestamp', '永久')
        if due_timestamp == '永久':
            return '永久'
        return auxiliary.timestamp_to_date(due_timestamp)
    return '永久'

def get_use_user(account_number):
    hyper_v_data = hyper_v.get()
    virtual_machine_data = get()
    information = {}
    for virtual_machine_data_count in virtual_machine_data:
        if virtual_machine_data_count in hyper_v_data and virtual_machine_data.get(virtual_machine_data_count).get('account_number') == account_number:
            information[virtual_machine_data_count] = hyper_v_data.get(virtual_machine_data_count)
    return information