# encoding = utf-8

from modular import core
from modular import auxiliary, virtual_machine
import time

def existence(username):
    return username in get()

def register(username, password, qq_number):
    data = get()
    password = auxiliary.get_md5(password)
    data[username] = {
        'password': password,
        'qq_number': qq_number,
        'register_timestamp': time.time()
    }
    core.write('user', data)

def set(username, key, value):
    data = get()
    if key == 'password':
        value = auxiliary.get_md5(value)
    data[username][key] = value
    core.write('user', data)

def delete(username):
    virtual_machine_data = virtual_machine.get_user(username)
    for virtual_machine_data_count in virtual_machine_data:
        virtual_machine.set(virtual_machine_data_count, 'username', '')
        virtual_machine.set(virtual_machine_data_count, 'due_timestamp', '')
    user_data = get()
    del user_data[username]
    core.write('user', user_data)

def get_password(username):
    return get().get(username).get('password')

def get_register_date(username):
    return auxiliary.timestamp_to_date(get().get(username).get('register_timestamp'))

def get_qq_number(username):
    return get().get(username).get('qq_number')

def get():
    return core.read('user')