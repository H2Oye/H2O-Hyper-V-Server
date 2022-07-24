# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, render_template, request, session
from modular import core, auxiliary, virtual_machine, user

import platform
if platform.system().lower() == 'windows':
    from modular import hyper_v_windows as hyper_v
else:
    from modular import hyper_v_other as hyper_v

import multiprocessing
import psutil
import platform
import time
import datetime
import base64

MANAGEMENT_APP = Blueprint('MANAGEMENT_APP', __name__)

@MANAGEMENT_APP.route('/management/')
def redirect_d():
    return redirect('./index')
    
@MANAGEMENT_APP.route('/management/index', methods=['GET', 'POST'])
def index():
    return render_template(
        'management/index.html',
        title=core.get_core('title'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        cpu_number=multiprocessing.cpu_count(),
        memory_size=round(psutil.virtual_memory().total / (1024 ** 3)),
        operating_system=platform.platform(),
        virtual_machine_number=len(hyper_v.get()),
        distribution_virtual_machine_number=len(core.read('virtual_machine')),
        user_number=len(core.read('user')),
        now_year=auxiliary.get_now_year()
    )

@MANAGEMENT_APP.route('/management/virtual_machine', methods=['GET', 'POST'])
def virtual_machine_d():
    return render_template(
        'management/virtual_machine.html',
        title=core.get_core('title'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        now_year=auxiliary.get_now_year()
    )

@MANAGEMENT_APP.route('/management/user', methods=['GET', 'POST'])
def user_d():
    return render_template(
        'management/user.html',
        title=core.get_core('title'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        now_year=auxiliary.get_now_year(),
    )

@MANAGEMENT_APP.route('/management/core', methods=['GET', 'POST'])
def core_d():
    return render_template(
        'management/core.html',
        title=core.get_core('title'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        notice=core.get_notice(),
        now_year=auxiliary.get_now_year()
    )

@MANAGEMENT_APP.route('/management/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('../login')

@MANAGEMENT_APP.route('/management/ajax', methods=['GET', 'POST'])
def ajax():
    parameter = core.get_request_parameter(request)
    action = parameter.get('action')
    
    if auxiliary.empty(action):
        return core.generate_response_json_result('参数错误')

    if action == 'revise_password':
        new_password = parameter.get('new_password')

        if auxiliary.empty(new_password):
            return core.generate_response_json_result('参数错误')

        if not auxiliary.empty(new_password) and len(new_password) < 8:
            return core.generate_response_json_result('密码长度至少8位')
        else:
            core.set_core('password', auxiliary.get_md5(new_password))
            return core.generate_response_json_result('修改成功')
    elif action == 'get_virtual_machine':
        format_d = parameter.get('format')
        page = parameter.get('page')
        limit = parameter.get('limit')

        if not page.isdigit() or not limit.isdigit():
            return core.generate_response_json_result('参数错误')
        page = int(page)
        limit = int(limit)

        if page < 0 or limit < 0:
            return core.generate_response_json_result('参数错误')

        data = hyper_v.get()
        if format_d == 'layui':
            data_count_d = len(data)
            if data_count_d == 0:
                return core.generate_layui_response_json_result(0, {})
            data = auxiliary.split_dict(data, limit)
            if page > len(data):
                return core.generate_response_json_result('参数错误')
            data = hyper_v.compound(data[page-1])
            information = []
            for data_count in data:
                data_single = data.get(data_count)
                information.append({
                    'id': data_count,
                    'name': data_single.get('name'),
                    'state': data_single.get('state'),
                    'cpu_count': data_single.get('cpu_count'),
                    'memory_size': data_single.get('memory_size'),
                    'account_number': virtual_machine.get_account_number(data_count),
                    'due_date': virtual_machine.get_due_date(data_count),
                    'remarks': virtual_machine.get_remarks(data_count, 'management')
                })
            return core.generate_layui_response_json_result(data_count_d, information)
        else:
            data = hyper_v.compound(data)
            information = {}
            for data_count in data:
                information[data_count] = data.get(data_count)
                information[data_count]['account_number'] = virtual_machine.get_account_number(data_count)
                information[data_count]['due_date'] = virtual_machine.get_due_date(data_count)
                information[data_count]['remarks'] = virtual_machine.get_remarks(data_count, 'management')
            return core.generate_response_json_result(information)
    elif action == 'revise_user_password':
        account_number = parameter.get('account_number')
        new_password = parameter.get('new_password')

        if auxiliary.empty_many(account_number, new_password):
            return core.generate_response_json_result('参数错误')
        
        if len(new_password) < 8:
            return core.generate_response_json_result('密码长度至少8位')
        user.set(account_number, 'password', auxiliary.get_md5(new_password))
        return core.generate_response_json_result('修改成功')
    elif action == 'get_user':
        format_d = parameter.get('format')
        page = parameter.get('page')
        limit = parameter.get('limit')

        if not page.isdigit() or not limit.isdigit():
            return core.generate_response_json_result('参数错误')
        page = int(page)
        limit = int(limit)

        if page < 0 or limit < 0:
            return core.generate_response_json_result('参数错误')

        data = core.read('user')
        if format_d == 'layui':
            data_count_d = len(data)
            if data_count_d == 0:
                return core.generate_layui_response_json_result(0, {})
            data = auxiliary.split_dict(data, limit)
            if page > len(data):
                return core.generate_response_json_result('参数错误')
            data = hyper_v.compound(data[page-1])
            information = []
            for data_count in data:
                data_single = data.get(data_count)
                information.append({
                    'account_number': data_count,
                    'password': data_single.get('password'),
                    'qq_number': data_single.get('qq_number'),
                    'register_date': user.get_register_date(data_count)
                })
            return core.generate_layui_response_json_result(data_count_d, information)
        else:
            return core.generate_response_json_result(information)
    elif action == 'add_user':
        account_number = parameter.get('account_number')
        password = parameter.get('password')
        qq_number = parameter.get('qq_number')
        
        if auxiliary.empty_many(account_number, password, qq_number):
            return core.generate_response_json_result('参数错误')
        
        if user.existence(account_number) or account_number == 'admin':
            information = '帐号已存在'
        elif len(account_number) < 8:
            information = '帐号长度至少8位'
        elif not account_number.isalnum():
            information = '帐号只允许数字和字母'
        elif len(password) < 8:
            information = '密码长度至少8位'
        elif auxiliary.empty(qq_number):
            information = '请输入QQ帐号'
        else:
            user.register(account_number, password, qq_number)
            information = '添加成功'
        return core.generate_response_json_result(information)
    elif action == 'delete_user':
        account_number = parameter.get('account_number')

        if auxiliary.empty(account_number):
            return core.generate_response_json_result('参数错误')
        
        user.delete(account_number)
        return core.generate_response_json_result('删除成功')
    elif action == 'revise_core':
        title = parameter.get('title')
        keyword = parameter.get('keyword')
        description = parameter.get('description')
        notice = parameter.get('notice')

        if auxiliary.empty_many(title, keyword, description, notice):
            return core.generate_response_json_result('参数错误')
        
        notice = notice.strip()
        notice = str(base64.b64encode(notice.encode('utf-8')), 'utf-8')
        core.set_core('title', title)
        core.set_core('keyword', keyword)
        core.set_core('description', description)
        core.set_core('notice', notice)
        return core.generate_response_json_result('修改成功')
    
    id_d = parameter.get('id')
    
    if auxiliary.empty(id_d):
        return core.generate_response_json_result('参数错误')
    
    if not hyper_v.existence(id_d):
        return core.generate_response_json_result('虚拟机不存在')
    
    name = hyper_v.get_name(id_d)
    
    if action == 'revise_virtual_machine_config':
        cpu_count = parameter.get('cpu_count')
        memory_size = parameter.get('memory_size')

        if auxiliary.empty_many(cpu_count, memory_size) or cpu_count == '0' or memory_size == '0':
            return core.generate_response_json_result('参数错误')
        
        if int(memory_size) % 2 != 0:
            return core.generate_response_json_result('运行内存大小必须是2的倍数')
        elif int(memory_size) < 32:
            return core.generate_response_json_result('运行内存大小必须大于32MB')
        
        if hyper_v.get_state(id_d) != '关机':
            return core.generate_response_json_result('请先关机')

        if hyper_v.revise_config(name, cpu_count, memory_size):
            return core.generate_response_json_result('修改成功')
        return core.generate_response_json_result('修改失败')
    elif action == 'start_virtual_machine':
        if hyper_v.start(id_d):
            return core.generate_response_json_result('开机成功')
        return core.generate_response_json_result('开机失败')
    elif action == 'shutdown_virtual_machine':
        if hyper_v.shutdown(id_d):
            return core.generate_response_json_result('关机成功')
        return core.generate_response_json_result('关机失败')
    elif action == 'force_shutdown_virtual_machine':
        if hyper_v.force_shutdown(name):
            return core.generate_response_json_result('强制关机成功')
        return core.generate_response_json_result('强制关机失败')
    elif action == 'restart_virtual_machine':
        if hyper_v.restart(id_d):
            return core.generate_response_json_result('重启成功')
        return core.generate_response_json_result('重启失败')
    elif action == 'get_virtual_machine_checkpoint':
        information = ''
        checkpoint = hyper_v.get_checkpoint(id_d)
        for checkpoint_count in checkpoint:
            information += checkpoint_count + '\n'
        if information:
            information = information[:-1]
        return core.generate_response_json_result(information)
    elif action == 'apply_virtual_machine_checkpoint':
        checkpoint_name = parameter.get('checkpoint_name')
    
        if auxiliary.empty(checkpoint_name):
            return core.generate_response_json_result('参数错误')
    
        if checkpoint_name not in hyper_v.get_checkpoint(id_d):
            return core.generate_response_json_result('检查点不存在')
        
        if hyper_v.get_state(id_d) != '关机':
            return core.generate_response_json_result('请先关机')
        
        if hyper_v.apply_checkpoint(id_d, checkpoint_name):
            return core.generate_response_json_result('应用检查点成功')
        return core.generate_response_json_result('应用检查点失败')
    elif action == 'rename_virtual_machine':
        new_name = parameter.get('new_name')
        
        if auxiliary.empty_many(id_d, new_name):
            return core.generate_response_json_result('参数错误')
        
        if new_name in hyper_v.get():
            return core.generate_response_json_result('名称已存在')
        if hyper_v.rename(name, new_name):
            return core.generate_response_json_result('重命名成功')
        return core.generate_response_json_result('重命名失败')
    elif action == 'remarks_virtual_machine':
        content = parameter.get('content')
        
        if auxiliary.empty(content):
            return core.generate_response_json_result('参数错误')
        
        virtual_machine.set_remarks(id_d, 'management', content)
        return core.generate_response_json_result('备注成功')
    elif action == 'distribution_virtual_machine':
        account_number = parameter.get('account_number')
        
        if auxiliary.empty(account_number):
            return core.generate_response_json_result('参数错误')
        
        if account_number == '取消分配':
            virtual_machine.set(id_d ,'account_number', '未分配')
            return core.generate_response_json_result('取消分配成功')
        else:
            virtual_machine.set(id_d ,'account_number', account_number)
            return core.generate_response_json_result('分配成功')
    elif action == 'set_due_date_virtual_machine':
        due_date = parameter.get('due_date')
    
        if auxiliary.empty_many(due_date):
            return core.generate_response_json_result('参数错误')
        
        if due_date == '永久':
            virtual_machine.set(id_d ,'due_timestamp', '永久')
        else:
            virtual_machine.set(id_d ,'due_timestamp', auxiliary.date_to_timestamp(due_date))
        return core.generate_response_json_result('设置到期日期成功')
    return core.generate_response_json_result('参数错误')