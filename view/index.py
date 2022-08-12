# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, render_template, session, make_response, request
from captcha.image import ImageCaptcha
import string
import random
import io
from modular import core, auxiliary, user

INDEX_APP = Blueprint('INDEX_APP', __name__)

@INDEX_APP.route('/')
def redirect_d():
    return redirect('./login')

@INDEX_APP.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('account_number'):
        if session.get('account_number') == 'admin':
            return redirect('../management/index')
        else:
            return redirect('../user/index')
    
    return render_template(
        'login.html',
        title=core.get_core('title'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        notice=core.get_notice(),
        now_year=auxiliary.get_now_year(),
    )


@INDEX_APP.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('account_number'):
        if session.get('account_number') == 'admin':
            return redirect('../management/index')
        else:
            return redirect('../user/index')
    
    return render_template(
        'register.html',
        title=core.get_core('title'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        notice=core.get_notice(),
        now_year=auxiliary.get_now_year(),
    )

@INDEX_APP.route('/ajax', methods=['GET', 'POST'])
def ajax():
    parameter = core.get_request_parameter(request)
    action = parameter.get('action')

    if auxiliary.empty(action):
        return core.generate_response_json_result('参数错误')

    if action == 'login':
        account_number = parameter.get('account_number')
        password = parameter.get('password')
        captcha = parameter.get('captcha')

        if auxiliary.empty_many(account_number, password, captcha):
            return core.generate_response_json_result('参数错误')
        
        if captcha.lower() != session.get('captcha', '').lower():
            return core.generate_response_json_result('验证码错误')
        
        if account_number == 'admin':
            if auxiliary.get_md5(password) == core.get_core('password'):
                session['account_number'] = 'admin'
                return core.generate_response_json_result('登录成功')
            else:
                return core.generate_response_json_result('密码错误')

        if not user.existence(account_number):
            information = '账户不存在'
        elif auxiliary.get_md5(password) == user.get_password(account_number):
            session['account_number'] = account_number
            information = '登录成功'
        else:
            information = '密码错误'
        return core.generate_response_json_result(information)
    elif action == 'register':
        account_number = parameter.get('account_number')
        password = parameter.get('password')
        qq_number = parameter.get('qq_number')
        captcha = parameter.get('captcha')
        
        if captcha.lower() != session.get('captcha', '').lower():
            return core.generate_response_json_result('验证码错误')
        
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
            information = '注册成功'
        return core.generate_response_json_result(information)
    return core.generate_response_json_result('参数错误')

@INDEX_APP.route('/captcha', methods=['GET', 'POST'])
def captcha():
    text_all = string.ascii_letters + string.digits
    text_4 = ''.join(random.sample(text_all, 4))
    image = ImageCaptcha().generate_image(text_4)
    bytes_iO = io.BytesIO()
    image.save(bytes_iO, 'jpeg')
    session['captcha'] = text_4
    result = make_response(bytes_iO.getvalue())
    result.headers['Content-Type'] = 'image/gif'
    return result