# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import core
from modular import auxiliary, virtual_machine
import time

def existence(account_number):
    return account_number in get()

def register(account_number, password, qq_number):
    data = get()
    password = auxiliary.get_md5(password)
    data[account_number] = {
        'password': password,
        'qq_number': qq_number,
        'register_timestamp': int(time.time())
    }
    core.write('user', data)

def set(account_number, key, value):
    data = get()
    data[account_number][key] = value
    core.write('user', data)

def delete(account_number):
    virtual_machine_data = virtual_machine.get_use_user(account_number)
    for virtual_machine_data_count in virtual_machine_data:
        virtual_machine.set(virtual_machine_data_count, 'account_number', '未分配')
        virtual_machine.set(virtual_machine_data_count, 'due_timestamp', '永久')
    user_data = get()
    del user_data[account_number]
    core.write('user', user_data)

def get_password(account_number):
    return get().get(account_number).get('password')

def get_register_date(account_number):
    return auxiliary.timestamp_to_date(get().get(account_number).get('register_timestamp'))

def get_qq_number(account_number):
    return get().get(account_number).get('qq_number')

def get():
    return core.read('user')