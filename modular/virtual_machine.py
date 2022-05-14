# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import core, auxiliary, hyper_v
import time

def is_due(name):
    if int(time.time()) > get_due_timestamp(name):
        return True
    return False

def set(name, key, value):
    data = core.read('virtual_machine')
    if name not in data:
        data[name] = {}
    data[name][key] = value
    core.write('virtual_machine', data)

def get_account_number(name):
    data = core.read('virtual_machine')
    if name in data:
        return data.get(name).get('account_number', '未分配')
    return '未分配'

def get_due_timestamp(name):
    data = core.read('virtual_machine')
    if name in data:
        due_timestamp = data.get(name).get('due_timestamp', '永久')
        if due_timestamp == '永久':
            return 3093527923200
        return due_timestamp
    return 3093527923200

def get_due_date(name):
    data = core.read('virtual_machine')
    if name in data:
        due_timestamp = data.get(name).get('due_timestamp', '永久')
        if due_timestamp == '永久':
            return '永久'
        return auxiliary.timestamp_to_date(due_timestamp)
    return '永久'

def set_remarks(name, type_d, content):
    data = core.read('virtual_machine')
    single_virtual_machine = data.get(name, {})
    if 'remarks' not in single_virtual_machine:
        single_virtual_machine['remarks'] = {}
    single_virtual_machine['remarks'][type_d] = content
    data[name] = single_virtual_machine
    core.write('virtual_machine', data)

def get_use_user(account_number):
    hyper_v_data = hyper_v.get()
    virtual_machine_data = core.read('virtual_machine')
    information = {}
    for virtual_machine_data_count in virtual_machine_data:
        if virtual_machine_data_count in hyper_v_data and virtual_machine_data.get(virtual_machine_data_count).get('account_number') == account_number:
            information[virtual_machine_data_count] = hyper_v_data.get(virtual_machine_data_count)
            information[virtual_machine_data_count]['due_date'] = get_due_date(virtual_machine_data_count)
            information[virtual_machine_data_count]['remarks'] = virtual_machine_data[virtual_machine_data_count]['remarks']
    return information

def reset_use_user(account_number):
    data = core.read('virtual_machine')
    for data_count in get_use_user(account_number):
        data[data_count]['account_number'] = '未分配'
        data[data_count]['remarks']['user'] = ''
        data[data_count]['due_timestamp'] = '永久'
    core.write('virtual_machine', data)

def get_remarks(name, type_d):
    return core.read('virtual_machine').get(name, {}).get('remarks', {}).get(type_d)

def rename(old_name, new_name):
    data = core.read('virtual_machine')
    if old_name in data:
        dict.update({new_name: data.pop(old_name)})
        core.write('virtual_machine', data)