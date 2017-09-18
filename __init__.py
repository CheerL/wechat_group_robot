import os
import sys
import gevent
import geventwebsocket
from flask_socketio import SocketIO
from flask import Flask, Blueprint

# 路径处理
if getattr(sys, 'frozen', False):
    ROOT_PATH = os.path.dirname(sys.executable)
else:
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

SRC_PATH = os.path.join(ROOT_PATH, 'src')
LOG_PATH = os.path.join(ROOT_PATH, 'log')
PIC_PATH = os.path.join(SRC_PATH, 'pic')
CONF_PATH = os.path.join(SRC_PATH, 'config')
PKL_PATH = os.path.join(SRC_PATH, 'robot.pkl')
PUID_PATH = os.path.join(SRC_PATH, 'puid.pkl')

for path in [SRC_PATH, LOG_PATH, PIC_PATH]:
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)

# 网络常量定义
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = False
api = Blueprint('api', __name__)
socket = SocketIO(app, async_mode='gevent')

def server_send(data, time=0):
    socket.emit('server-send', data)
    server_pause(time)

def server_pause(time=0):
    socket.sleep(time)

def server_backgroud(target):
    socket.start_background_task(target=target)