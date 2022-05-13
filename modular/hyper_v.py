# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import subprocess
import wmi
import pythoncom
from modular import virtual_machine

def get():
    data = str(subprocess.check_output(['powershell.exe', 'Get-VM'], shell=True), encoding='gbk')
    information = {}
    for data_count in data.splitlines():
        if 'Off' in data_count or 'Running' in data_count:
            data_count = data_count.split(' ')
            data_count = [data_count_count for data_count_count in data_count if data_count_count != '']
            state = data_count[1]
            state = state.replace('Off', '关机')
            state = state.replace('Running', '运行')
            information[data_count[0]] = {
                'state': state,
                'uptime': data_count[4]
            }
    return information

def rename(old_name, new_name):
    subprocess.check_output(['powershell.exe', f'Rename-VM "{old_name}" "{new_name}"'], shell=True)
    virtual_machine.rename(old_name, new_name)

def start(name):
    pythoncom.CoInitialize()
    CON = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = CON.Msvm_ComputerSystem(ElementName=name)
    vm[0].RequestStateChange(2)

def shutdown(name):
    pythoncom.CoInitialize()
    CON = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = CON.Msvm_ComputerSystem(ElementName=name)
    vm[0].RequestStateChange(3)

def force_shutdown(name):
    subprocess.check_output(['powershell.exe', f'Stop-VM -Name "{name}" –Force'], shell=True)

def restart(name):
    pythoncom.CoInitialize()
    CON = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = CON.Msvm_ComputerSystem(ElementName=name)
    vm[0].RequestStateChange(11)

def get_checkpoint(name):
    pythoncom.CoInitialize()
    CON = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = CON.Msvm_ComputerSystem(ElementName=name)
    vm = vm[0]
    checkpoint = vm.associators(wmi_result_class='Msvm_VirtualSystemSettingData')
    information = []
    for checkpoint_count in checkpoint:
        information.append(checkpoint_count.ElementName)
    if information == [name]:
        information.clear()
    else:
        information.remove(name)
        information = list(set(information))
    return information

def apply_checkpoint(name, checkpoint_name):
    pythoncom.CoInitialize()
    CON = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = CON.Msvm_ComputerSystem(ElementName=name)
    vm = vm[0]
    checkpoint = vm.associators(wmi_result_class='Msvm_VirtualSystemSettingData')
    for checkpoint_count in checkpoint:
        if checkpoint_count.ElementName == checkpoint_name:
            management = wmiServerConnection.Msvm_VirtualSystemManagementService()
            management[0].ApplyVirtualSystemSnapshotEx(vm.path(), checkpoint_count.path())