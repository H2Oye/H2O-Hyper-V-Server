# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, render_template, request, session
from modular import core, auxiliary, hyper_v, virtual_machine, user
import multiprocessing
import psutil
import platform
import time
import datetime

MANAGEMENT_APP = Blueprint('MANAGEMENT_APP', __name__)

@MANAGEMENT_APP.route('/management/')
def redirect_d():
    return redirect('./index')
    
@MANAGEMENT_APP.route('/management/index', methods=['GET', 'POST'])
def index():
    information = ''
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        password = parameter.get('password')
        if len(password) < 8:
            information = '密码长度至少8位'
        else:
            password = auxiliary.get_md5(password)
            core.set_core('password', password)
            information = '修改成功'
    return render_template(
        'management/index.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        select_index='layui-this',
        cpu=multiprocessing.cpu_count(),
        memory=round(psutil.virtual_memory().total / (1024 ** 3)),
        ram=round(psutil.disk_usage('/').total / (1024 ** 3)),
        operating_system=platform.platform(),
        running_time=datetime.timedelta(seconds=time.time() - psutil.boot_time()),
        virtual_machine_number=len(hyper_v.get()),
        distribution_virtual_machine_number=len(virtual_machine.get()),
        user_number=len(user.get()),
        now_year=auxiliary.get_now_year(),
        information=information
    )

@MANAGEMENT_APP.route('/management/virtual_machine', methods=['GET', 'POST'])
def virtual_machine_d():
    checkpoint_information = ''
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        action = parameter.get('action')
        name = parameter.get('name')
        if action == 'start':
            state = virtual_machine.start(name)
            if state == False:
                return '过期无法开机'
            return '开机成功'
        elif action == 'shutdown':
            hyper_v.shutdown(name)
            return '关机成功'
        elif action == 'restart':
            state = virtual_machine.restart(name)
            if state == False:
                return '过期无法重启'
            return '重启成功'
        elif action == 'distribution':
            username = parameter.get('username')
            virtual_machine.set(name ,'username', username)
            return '分配成功'
        elif action == 'renew':
            due_date = parameter.get('due_date')
            virtual_machine.set(name ,'due_timestamp', auxiliary.date_to_timestamp(due_date))
            return '续费成功'
        elif action == 'get_checkpoint':
            checkpoint = hyper_v.get_checkpoint(name)
            for checkpoint_count in checkpoint:
                checkpoint_information += checkpoint_count + '\n'
            if checkpoint_information:
                checkpoint_information = checkpoint_information[:-1]
            return checkpoint_information
        checkpoint_name = parameter.get('checkpoint_name')
        if checkpoint_name not in hyper_v.get_checkpoint(name):
            return '检查点不存在'
        hyper_v.apply_checkpoint(name, checkpoint_name)
        return '恢复检查点成功'
    data_information = ''
    data = hyper_v.get()
    for data_count in data:
        data_single = data.get(data_count)
        data_information += '{ "name": "' + data_count + '", "state": "' + data_single.get('state') + '", "uptime": "' + data_single.get('uptime') + '", "username": "' + virtual_machine.get_username(data_count) + '", "due_date": "' + virtual_machine.get_due_date(data_count) + '" },'
    if data_information:
        data_information = data_information[:-1]
    return render_template(
        'management/virtual_machine.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        select_virtual_machine='layui-this',
        data=data_information,
        checkpoint=checkpoint_information,
        now_year=auxiliary.get_now_year(),
        now_url=request.base_url
    )

@MANAGEMENT_APP.route('/management/user', methods=['GET', 'POST'])
def user_d():
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        action = parameter.get('action')
        username = parameter.get('username')
        if action == 'reset_password':
            password = parameter.get('password')
            if len(password) < 8:
                return '密码长度至少8位'
            user.reset_password(username, password)
            return '修改成功'
        user.delete(username)
        return '删除成功'
    information = ''
    data = user.get()
    for data_count in data:
        data_single = data.get(data_count)
        information += '{ "username": "' + data_count + '", "password": "' + data_single.get('password') + '", "qq_number": "' + data_single.get('qq_number') + '", "register_date": "' + user.get_register_date(data_count) + '" },'
    information = information[:-1]
    return render_template(
        'management/user.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        select_user='layui-this',
        data=information,
        now_year=auxiliary.get_now_year(),
        now_url=request.base_url
    )

@MANAGEMENT_APP.route('/management/core', methods=['GET', 'POST'])
def core_d():
    information = ''
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        title = parameter.get('title')
        subtitle = parameter.get('subtitle')
        keyword = parameter.get('keyword')
        description = parameter.get('description')
        notice = parameter.get('notice')
        core.set_core('title', title)
        core.set_core('subtitle', subtitle)
        core.set_core('keyword', keyword)
        core.set_core('description', description)
        core.set_core('notice', notice)
        information = '修改成功'
    return render_template(
        'management/core.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        select_core='layui-this',
        notice=core.get_core('notice'),
        now_year=auxiliary.get_now_year(),
        information=information
    )

@MANAGEMENT_APP.route('/management/logout')
def logout():
    session.clear()
    return redirect('../login')