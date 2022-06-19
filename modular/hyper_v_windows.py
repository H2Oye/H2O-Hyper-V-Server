# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import subprocess
import wmi
import pythoncom
from modular import auxiliary

def get():
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem()
    vm_memory = con.Msvm_MemorySettingData()
    vm_cpu = con.Msvm_ProcessorSettingData()
    information = {}
    for vm_count in vm:
        if vm_count.Caption == '虚拟机':
            if vm_count.EnabledDefault == 2:
                state = '运行'
            elif vm_count.EnabledDefault == 3:
                state = '关机'
            elif vm_count.EnabledDefault == 4:
                state = '正在关机'
            elif vm_count.EnabledDefault == 10:
                state = '正在启动'
            elif vm_count.EnabledDefault == 11:
                state = '正在重启'
            else:
                state = '未知'
            information[vm_count.Name] = {
                'name': vm_count.ElementName,
                'state': state
            }
    for vm_cpu_count in vm_cpu:
        if vm_cpu_count.Description == 'Microsoft 虚拟处理器的设置。':
            id_d = auxiliary.get_middle_text(vm_cpu_count.InstanceID, 'Microsoft:', '\\')
            if id_d in information:
                information[id_d]['cpu_count'] = int(vm_cpu_count.VirtualQuantity)
    for vm_memory_count in vm_memory:
        if vm_memory_count.Description == 'Microsoft 虚拟机内存的设置。':
            id_d = auxiliary.get_middle_text(vm_memory_count.InstanceID, 'Microsoft:', '\\')
            if id_d in information:
                information[id_d]['memory_size'] = int(vm_memory_count.VirtualQuantity)
    return information

def get_name(id_d):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)
    return vm[0].ElementName

def existence(id_d):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)
    if len(vm) == 0:
        return False
    return True

def get_state(id_d):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)

    if len(vm) == 0:
        return False
    
    vm = vm[0]
    if vm.EnabledDefault == 2:
        state = '运行'
    elif vm.EnabledDefault == 3:
        state = '关机'
    elif vm.EnabledDefault == 4:
        state = '正在关机'
    elif vm.EnabledDefault == 10:
        state = '正在启动'
    elif vm.EnabledDefault == 11:
        state = '正在重启'
    else:
        state = '未知'
    return state

def revise_config(name, cpu_count, memory_size):
    try:
        subprocess.check_output(['powershell.exe', f'Set-VMProcessor -VMName "{name}" -Count {cpu_count};Set-VMMemory -VMName "{name}" -StartupBytes {memory_size}MB'], shell=True)
    except Exception:
        return False
    else:
        return True

def start(id_d):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)
    
    if len(vm) == 0:
        return False
    
    vm[0].RequestStateChange(2)
    return True

def shutdown(id_d):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)
    
    if len(vm) == 0:
        return False
    
    vm[0].RequestStateChange(3)
    return True

def force_shutdown(name):
    try:
        subprocess.check_output(['powershell.exe', f'Stop-VM -Name "{name}" –Force'], shell=True)
    except Exception:
        return False
    else:
        return True

def restart(id_d):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)
    
    if len(vm) == 0:
        return False
    
    vm[0].RequestStateChange(10)
    return True

def rename(old_name, new_name):
    try:
        subprocess.check_output(['powershell.exe', f'Rename-VM "{old_name}" "{new_name}"'], shell=True)
    except Exception:
        return False
    else:
        return True

def get_checkpoint(id_d):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)
    
    if len(vm) == 0:
        return False
    
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

def apply_checkpoint(id_d, checkpoint_name):
    pythoncom.CoInitialize()
    con = wmi.WMI(wmi=wmi.connect_server(server='127.0.0.1', namespace=r'root\virtualization\v2'))
    vm = con.Msvm_ComputerSystem(Name=id_d)
    
    if len(vm) == 0:
        return False
    
    vm = vm[0]
    checkpoint = vm.associators(wmi_result_class='Msvm_VirtualSystemSettingData')
    for checkpoint_count in checkpoint:
        if checkpoint_count.ElementName == checkpoint_name:
            management = wmiServerConnection.Msvm_VirtualSystemManagementService()
            management[0].ApplyVirtualSystemSnapshotEx(vm.path(), checkpoint_count.path())
    return True