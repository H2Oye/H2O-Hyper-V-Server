# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

from flask import Flask, session, request, redirect
import datetime
from flask_cors import CORS
from view.index import INDEX_APP
from view.management import MANAGEMENT_APP
from view.user import USER_APP
from modular import core, virtual_machine, hyper_v
import threading
import datetime
import time

APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'y3mha918zrpeduezovm5vtks'
APP.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)
CORS(APP, resources=r'/*')
APP.register_blueprint(INDEX_APP)
APP.register_blueprint(MANAGEMENT_APP)
APP.register_blueprint(USER_APP)

@APP.before_request
def before_request():
    username = session.get('username')
    url = request.path.split('/')
    if username != 'admin' and url[1] == 'manage':
        return redirect('../login')
    elif (not username or username == 'admin') and url[1] == 'user':
        return redirect('../login')

def check():
    while True:
        now_date = datetime.datetime.now()
        if now_date.hour == 0 and now_date.minute == 0:
            virtual_machine_data = virtual_machine.get()
            hyper_v_data = hyper_v.get()
            for virtual_machine_data_count in virtual_machine_data:
                if virtual_machine_data_count in hyper_v_data:
                    if virtual_machine.due(virtual_machine_data_count):
                        hyper_v.shutdown(virtual_machine_data_count)
                    time.sleep(10)
        time.sleep(30)

if __name__ == '__main__':
    thread = threading.Thread(target=check)
    thread.setDaemon(True)
    thread.start()
    #APP.run(host='0.0.0.0', port=core.get_core('port'), processes=True, ssl_context=('./ssl.crt', './ssl.key'))
    WSGIServer(('0.0.0.0', core.get_core('port')), APP, keyfile='./ssl.key', certfile='./ssl.crt').serve_forever()