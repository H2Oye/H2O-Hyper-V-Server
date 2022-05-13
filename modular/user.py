# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import core
from modular import auxiliary, virtual_machine
import time

def existence(account_number):
    return account_number in core.read('user')

def register(account_number, password, qq_number):
    data = core.read('user')
    password = auxiliary.get_md5(password)
    data[account_number] = {
        'password': password,
        'qq_number': qq_number,
        'register_timestamp': int(time.time())
    }
    core.write('user', data)

def set(account_number, key, value):
    data = core.read('user')
    data[account_number][key] = value
    core.write('user', data)

def delete(account_number):
    virtual_machine.reset_use_user(account_number)
    user_data = core.read('user')
    if account_number in user_data:
        del user_data[account_number]
        core.write('user', user_data)

def get_password(account_number):
    return core.read('user').get(account_number).get('password')

def get_register_date(account_number):
    return auxiliary.timestamp_to_date(core.read('user').get(account_number).get('register_timestamp'))

def get_qq_number(account_number):
    return core.read('user').get(account_number).get('qq_number')