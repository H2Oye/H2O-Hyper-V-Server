# encoding = utf-8

from flask import Blueprint, redirect, render_template, request, session
from modular import core, auxiliary, user

INDEX_APP = Blueprint('INDEX_APP', __name__)

@INDEX_APP.route('/')
def redirect_distinguisher():
    return redirect('./login')

@INDEX_APP.route('/login', methods=['GET', 'POST'])
def login():
    information = '登录你的帐户'
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        username = parameter.get('username')
        password = parameter.get('password')
        if auxiliary.empty(username):
            information = '请输入帐号'
        elif auxiliary.empty(password):
            information = '请输入密码'
        else:
            password = auxiliary.get_md5(password)
            if username == 'admin':
                if password == core.get_core('password'):
                    session['username'] = 'admin'
                    return redirect('./management/index', 301)
                else:
                    information = '密码错误'
            elif not user.existence(username):
                information = '帐户不存在'
            elif password == user.get_password(username):
                session['username'] = username
                return redirect('./user/index', 301)
            else:
                information = '密码错误'
    return render_template(
        'index.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        notice=core.get_core('notice').split('\n'),
        now_year=auxiliary.get_now_year(),
        type_text='登录',
        information=information,
        type_name='login',
        want_type_name='register',
        want_type_text='注册'
    )

@INDEX_APP.route('/register', methods=['GET', 'POST'])
def register():
    information = '注册你的帐户'
    if request.method == 'POST':
        parameter = core.get_request_parameter(request)
        username = parameter.get('username')
        password = parameter.get('password')
        qq_number = parameter.get('qq_number')
        if auxiliary.empty(username):
           information = '请输入帐号'
        elif username == 'admin' or user.existence(username):
           information = '帐户已存在'
        elif len(username) < 8:
            information = '帐号长度至少8位'
        elif not username.isalnum():
            information = '帐号只允许数字和字母'
        elif auxiliary.empty(password):
           information = '请输入密码'
        elif len(password) < 8:
            information = '密码长度至少8位'
        elif auxiliary.empty(qq_number):
           information = '请输入QQ帐号'
        else:
            user.register(username, password, qq_number)
            information = '注册成功'
    return render_template(
        'index.html',
        title=core.get_core('title'),
        subtitle=core.get_core('subtitle'),
        keyword=core.get_core('keyword'),
        description=core.get_core('description'),
        notice=core.get_core('notice').split('\n'),
        now_year=auxiliary.get_now_year(),
        type_text='注册',
        information=information,
        type_name='register',
        want_type_name='login',
        want_type_text='登录'
    )