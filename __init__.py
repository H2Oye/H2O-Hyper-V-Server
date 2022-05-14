# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

from flask import Flask, session, request, redirect
import datetime
import flask_cors
from view.index import INDEX_APP
from view.management import MANAGEMENT_APP
from view.user import USER_APP
from modular import core, virtual_machine, hyper_v
import threading
import datetime
import time

APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'h2o_hyper_v'
APP.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)
flask_cors.CORS(APP, resources=r'/*')
APP.register_blueprint(INDEX_APP)
APP.register_blueprint(MANAGEMENT_APP)
APP.register_blueprint(USER_APP)

@APP.errorhandler(404)
def errorhandler_404(error):
    return '未找到文件'

@APP.errorhandler(500)
def errorhandler_500(error):
    return '未知错误'

@APP.before_request
def before_request():
    account_number = session.get('account_number')
    url = request.path.split('/')
    if account_number != 'admin' and url[1] == 'management':
        return redirect('../login')
    elif (not account_number or account_number == 'admin') and url[1] == 'user':
        return redirect('../login')

def check():
    while True:
        now_date = datetime.datetime.now()
        if now_date.hour == 0 and now_date.minute == 0:
            virtual_machine_data = virtual_machine.get()
            hyper_v_data = hyper_v.get()
            for virtual_machine_data_count in virtual_machine_data:
                if virtual_machine_data_count in hyper_v_data:
                    if virtual_machine.is_due(virtual_machine_data_count) and hyper_v_data.get(virtual_machine_data_count).get('state') != '关机':
                        hyper_v.shutdown(virtual_machine_data_count)
                    time.sleep(10)
        time.sleep(30)

def initialization():
    thread = threading.Thread(target=check)
    thread.setDaemon(True)
    thread.start()

if __name__ == '__main__':
    initialization()
    #APP.run(host='0.0.0.0', port=core.get_core('port'), debug=True, processes=True)
    WSGIServer(('0.0.0.0', core.get_core('port')), APP).serve_forever()