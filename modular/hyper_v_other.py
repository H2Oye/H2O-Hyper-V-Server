# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import virtual_machine

def get():
    information = {
        '12345678': {'name': '新建虚拟机', 'state': '关机'},
        '12345679': {'name': '新建虚拟机', 'state': '关机'},
        '12345680': {'name': '新建虚拟机', 'state': '关机'},
        '12345681': {'name': '新建虚拟机', 'state': '关机'},
        '12345682': {'name': '新建虚拟机', 'state': '关机'},
        '12345683': {'name': '新建虚拟机', 'state': '关机'},
        '12345684': {'name': '新建虚拟机', 'state': '关机'},
        '12345685': {'name': '新建虚拟机', 'state': '关机'},
        '12345686': {'name': '新建虚拟机', 'state': '关机'},
        '12345687': {'name': '新建虚拟机', 'state': '关机'},
        '12345688': {'name': '新建虚拟机', 'state': '关机'},
        '12345689': {'name': '新建虚拟机', 'state': '关机'},
        '12345690': {'name': '新建虚拟机', 'state': '关机'},
        '12345691': {'name': '新建虚拟机', 'state': '关机'},
        '12345692': {'name': '新建虚拟机', 'state': '关机'},
        '12345693': {'name': '新建虚拟机', 'state': '关机'},
        '12345694': {'name': '新建虚拟机', 'state': '关机'},
        '12345695': {'name': '新建虚拟机', 'state': '关机'},
        '12345696': {'name': '新建虚拟机', 'state': '关机'},
        '12345697': {'name': '新建虚拟机', 'state': '关机'},
        '12345698': {'name': '新建虚拟机', 'state': '关机'},
        '12345699': {'name': '新建虚拟机', 'state': '关机'},
        '12345700': {'name': '新建虚拟机', 'state': '关机'},
        '12345701': {'name': '新建虚拟机', 'state': '关机'},
        '12345702': {'name': '新建虚拟机', 'state': '关机'},
        '12345703': {'name': '新建虚拟机', 'state': '关机'},
        '12345704': {'name': '新建虚拟机', 'state': '关机'},
        '12345705': {'name': '新建虚拟机', 'state': '关机'},
        '12345706': {'name': '新建虚拟机', 'state': '关机'},
        '12345707': {'name': '新建虚拟机', 'state': '关机'},
        '12345709': {'name': '新建虚拟机', 'state': '关机'},
        '12345710': {'name': '新建虚拟机', 'state': '关机'},
        '12345711': {'name': '新建虚拟机', 'state': '关机'},
        '12345712': {'name': '新建虚拟机', 'state': '关机'},
        '12345713': {'name': '新建虚拟机', 'state': '关机'},
        '12345714': {'name': '新建虚拟机', 'state': '关机'},
        '12345715': {'name': '新建虚拟机', 'state': '关机'},
        '12345716': {'name': '新建虚拟机', 'state': '关机'},
        '12345717': {'name': '新建虚拟机', 'state': '关机'},
        '12345718': {'name': '新建虚拟机', 'state': '关机'},
        '12345719': {'name': '新建虚拟机', 'state': '关机'},
        '12345720': {'name': '新建虚拟机', 'state': '关机'},
        '12345721': {'name': '新建虚拟机', 'state': '关机'},
        '12345722': {'name': '新建虚拟机', 'state': '关机'},
        '12345723': {'name': '新建虚拟机', 'state': '关机'},
        '12345724': {'name': '新建虚拟机', 'state': '关机'},
        '12345725': {'name': '新建虚拟机', 'state': '关机'},
        '12345726': {'name': '新建虚拟机', 'state': '关机'},
        '12345727': {'name': '新建虚拟机', 'state': '关机'},
        '12345728': {'name': '新建虚拟机', 'state': '关机'}
    }
    return information

def compound(data):
    for data_count in data:
        data[data_count]['cpu_count'] = 2
        data[data_count]['memory_size'] = 1024
    return data

def get_name(id_d):
    return '新建虚拟机'

def existence(name):
    return True

def get_state(name):
    return '运行'

def revise_config(name, cpu_count, memory_size):
    return True

def start(name):
    return True

def shutdown(name):
    return True

def force_shutdown(name):
    return True

def restart(name):
    return True

def rename(old_name, new_name):
    virtual_machine.rename(old_name, new_name)
    return True

def get_checkpoint(name):
    information = ['新建检查点']
    return information

def apply_checkpoint(name, checkpoint_name):
    return True