# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, render_template, request, session
from modular import core, auxiliary, hyper_v, virtual_machine, user
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
        
        data = hyper_v.get()
        if format_d == 'layui':
            information = []
            for data_count in data:
                data_single = data.get(data_count)
                information.append({
                    'name': data_count,
                    'state': data_single.get('state'),
                    'account_number': virtual_machine.get_account_number(data_count),
                    'due_date': virtual_machine.get_due_date(data_count),
                    'remarks': virtual_machine.get_remarks(data_count, 'management')
                })
            return core.generate_layui_response_json_result(information)
        else:
            information = {}
            for data_count in data:
                data_single = data.get(data_count)
                information[data_count] = {
                    'state': data_single.get('state'),
                    'account_number': virtual_machine.get_account_number(data_count),
                    'due_date': virtual_machine.get_due_date(data_count),
                    'remarks': virtual_machine.get_remarks(data_count, 'management')
                }
            return core.generate_response_json_result(information)
    elif action == 'get_virtual_machine_checkpoint':
        name = parameter.get('name')
    
        if auxiliary.empty(name):
            return core.generate_response_json_result('参数错误')
        
        checkpoint_information = ''
        checkpoint = hyper_v.get_checkpoint(name)
        for checkpoint_count in checkpoint:
            checkpoint_information += checkpoint_count + '\n'
        if checkpoint_information:
            checkpoint_information = checkpoint_information[:-1]
        return core.generate_response_json_result(checkpoint_information)
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
        
        data = core.read('user')
        if format_d == 'layui':
            information = []
            for data_count in data:
                data_single = data.get(data_count)
                information.append({
                    'account_number': data_count,
                    'password': data_single.get('password'),
                    'qq_number': data_single.get('qq_number'),
                    'register_date': user.get_register_date(data_count)
                })
            return core.generate_layui_response_json_result(information)
        else:
            information = {}
            for data_count in data:
                data_single = data.get(data_count)
                information[data_count] = {
                    'password': data_single.get('password'),
                    'qq_number': data_single.get('qq_number'),
                    'register_date': user.get_register_date(data_count)
                }
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
    
    name = parameter.get('name')
    
    if auxiliary.empty(name):
        name = parameter.get('old_name')
        if auxiliary.empty(name):
            return core.generate_response_json_result('参数错误')
    
    if name not in hyper_v.get():
        return core.generate_response_json_result('虚拟机不存在')
    
    if action == 'start_virtual_machine':
        hyper_v.start(name)
        return core.generate_response_json_result('开机成功')
    elif action == 'shutdown_virtual_machine':
        hyper_v.shutdown(name)
        return core.generate_response_json_result('关机成功')
    elif action == 'force_shutdown_virtual_machine':
        hyper_v.force_shutdown(name)
        return core.generate_response_json_result('强制关机成功')
    elif action == 'restart_virtual_machine':
        hyper_v.restart(name)
        return core.generate_response_json_result('重启成功')
    elif action == 'apply_virtual_machine_checkpoint':
        checkpoint_name = parameter.get('checkpoint_name')
    
        if auxiliary.empty(checkpoint_name):
            return core.generate_response_json_result('参数错误')
    
        if checkpoint_name not in hyper_v.get_checkpoint(name):
            return core.generate_response_json_result('检查点不存在')
        hyper_v.apply_checkpoint(name, checkpoint_name)
        return core.generate_response_json_result('恢复检查点成功')
    elif action == 'rename_virtual_machine':
        old_name = parameter.get('old_name')
        new_name = parameter.get('new_name')
        
        if auxiliary.empty_many(old_name, new_name):
            return core.generate_response_json_result('参数错误')
        
        if new_name in hyper.get() or new_name in core.read('virtual_machine'):
            return core.generate_response_json_result('名称已存在')
        hyper_v.rename(old_name, new_name)
        return core.generate_response_json_result('重命名成功')
    elif action == 'remarks_virtual_machine':
        content = parameter.get('content')
        
        if auxiliary.empty(content):
            return core.generate_response_json_result('参数错误')
        
        virtual_machine.set_remarks(name, 'management', content)
        return core.generate_response_json_result('备注成功')
    elif action == 'distribution_virtual_machine':
        account_number = parameter.get('account_number')
        
        if auxiliary.empty(account_number):
            return core.generate_response_json_result('参数错误')
        
        if account_number == '取消分配':
            virtual_machine.set(name ,'account_number', '未分配')
            return core.generate_response_json_result('取消分配成功')
        else:
            virtual_machine.set(name ,'account_number', account_number)
            return core.generate_response_json_result('分配成功')
    elif action == 'set_due_date_virtual_machine':
        due_date = parameter.get('due_date')
    
        if auxiliary.empty_many(due_date):
            return core.generate_response_json_result('参数错误')
        
        if due_date == '永久':
            virtual_machine.set(name ,'due_timestamp', '永久')
        else:
            virtual_machine.set(name ,'due_timestamp', auxiliary.date_to_timestamp(due_date))
        return core.generate_response_json_result('设置到期日期成功')
    return core.generate_response_json_result('参数错误')