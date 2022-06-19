# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from modular import virtual_machine

def get():
    information = {}
    information['12345678'] = {
        'name': '新建虚拟机',
        'state': '关机',
        'memory_size': 1024,
        'cpu_count': 2
    }
    return information

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