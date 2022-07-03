# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import core, auxiliary

import platform
if platform.system().lower() == 'windows':
    from modular import hyper_v_windows as hyper_v
else:
    from modular import hyper_v_other as hyper_v

import time

def is_due(id_d):
    if int(time.time()) > get_due_timestamp(id_d):
        return True
    return False

def set(id_d, key, value):
    data = core.read('virtual_machine')
    if id_d not in data:
        data[id_d] = {}
    data[id_d][key] = value
    core.write('virtual_machine', data)

def get_account_number(id_d):
    data = core.read('virtual_machine')
    if id_d in data:
        return data.get(id_d).get('account_number', '未分配')
    return '未分配'

def get_due_timestamp(id_d):
    data = core.read('virtual_machine')
    if id_d in data:
        due_timestamp = data.get(id_d).get('due_timestamp', '永久')
        if due_timestamp == '永久':
            return 3093527923200
        return due_timestamp
    return 3093527923200

def get_due_date(id_d):
    data = core.read('virtual_machine')
    if id_d in data:
        due_timestamp = data.get(id_d).get('due_timestamp', '永久')
        if due_timestamp == '永久':
            return '永久'
        return auxiliary.timestamp_to_date(due_timestamp)
    return '永久'

def set_remarks(id_d, type_d, content):
    data = core.read('virtual_machine')
    single_virtual_machine = data.get(id_d, {})
    if 'remarks' not in single_virtual_machine:
        single_virtual_machine['remarks'] = {}
    single_virtual_machine['remarks'][type_d] = content
    data[id_d] = single_virtual_machine
    core.write('virtual_machine', data)

def get_use_user(account_number):
    hyper_v_data = hyper_v.get()
    virtual_machine_data = core.read('virtual_machine')
    information = {}
    for virtual_machine_data_count in virtual_machine_data:
        if virtual_machine_data_count in hyper_v_data and virtual_machine_data.get(virtual_machine_data_count).get('account_number') == account_number:
            information[virtual_machine_data_count] = hyper_v_data.get(virtual_machine_data_count)
            information[virtual_machine_data_count]['due_date'] = get_due_date(virtual_machine_data_count)
            information[virtual_machine_data_count]['remarks'] = virtual_machine_data.get(virtual_machine_data_count).get('remarks', {}).get('user', '无')
    return information

def reset_use_user(account_number):
    data = core.read('virtual_machine')
    for data_count in get_use_user(account_number):
        data[data_count]['account_number'] = '未分配'
        data[data_count]['remarks']['user'] = ''
        data[data_count]['due_timestamp'] = '永久'
    core.write('virtual_machine', data)

def get_remarks(id_d, type_d):
    return core.read('virtual_machine').get(id_d, {}).get('remarks', {}).get(type_d, '无')