# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import subprocess
import wmi
import pythoncom
from modular import virtual_machine

def get():
    pythoncom.CoInitialize()
    CON = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = CON.Msvm_ComputerSystem()
    information = {}
    for vm_count in vm:
        if vm_count.Caption == '虚拟机':
            if vm_count.EnabledDefault == 2:
                state = '运行'
            elif vm_count.EnabledDefault == 3:
                state = '关闭'
            elif vm_count.EnabledDefault == 4:
                state = '正在关闭'
            elif vm_count.EnabledDefault == 10:
                state = '正在启动'
            elif vm_count.EnabledDefault == 11:
                state = '正在重启'
            else:
                state = '未知'
            information[vm_count.ElementName] = {
                'state': state
            }
    return information

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
    vm[0].RequestStateChange(10)

def rename(old_name, new_name):
    subprocess.check_output(['powershell.exe', f'Rename-VM "{old_name}" "{new_name}"'], shell=True)
    virtual_machine.rename(old_name, new_name)

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