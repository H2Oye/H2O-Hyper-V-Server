# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, render_template, request, session
from modular import core, user, virtual_machine, auxiliary, hyper_v

USER_APP = Blueprint('USER_APP', __name__)

@USER_APP.route('/user/')
def redirect_d():
    return redirect('./index')

@USER_APP.route('/user/index', methods=['GET', 'POST'])
def index():
    username = session.get('username')
    information = ''
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        password = parameter.get('password')
        qq_number = parameter.get('qq_number')
        if not auxiliary.empty(password) and len(password) < 8:
            information = '密码长度至少8位'
        else:
            user.set(username, 'password', password)
            user.set(username ,'qq_number', qq_number)
            information = '修改成功'
    return render_template(
        'user/index.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        select_index='layui-this',
        username=username,
        password=user.get_password(username),
        qq_number=user.get_qq_number(username),
        register_date=user.get_register_date(username),
        virtual_machine_number=len(virtual_machine.get_user(username)),
        now_year=auxiliary.get_now_year(),
        information=information
    )

@USER_APP.route('/user/virtual_machine', methods=['GET', 'POST'])
def virtual_machine_d():
    username = session.get('username')
    checkpoint_information = ''
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        action = parameter.get('action')
        name = parameter.get('name')
        vm = virtual_machine.get_user(username)
        if name not in vm:
            return '权限错误'
        if virtual_machine.due(name):
            return '过期无法操作'
        if action == 'start':
            hyper_v.start(name)
            return '开机成功'
        elif action == 'shutdown':
            hyper_v.shutdown(name)
            return '关机成功'
        elif action == ' restart':
            hyper_v.restart(name)
            return '重启成功'
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
    information = ''
    data = virtual_machine.get_user(username)
    for data_count in data:
        data_single = data.get(data_count)
        information += '{ "name": "' + data_count + '", "state": "' + data_single.get('state') + '", "uptime": "' + data_single.get('uptime') + '", "due_date": "' + virtual_machine.get_due_date(data_count) + '" },'
    information = information[:-1]
    return render_template(
        'user/virtual_machine.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        select_virtual_machine='layui-this',
        data=information,
        checkpoint=checkpoint_information,
        now_year=auxiliary.get_now_year(),
        now_url=request.base_url
    )

@USER_APP.route('/user/logout')
def logout():
    session.clear()
    return redirect('../login')