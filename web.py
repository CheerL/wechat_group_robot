import time
import sys
import random
import psutil
import pickle
import parallel as pl
import json
from flask import send_file, jsonify, request
from __init__ import CONF_PATH, app, api, socket, server_send, server_backgroud

from robot_api import Group_robot, Group, Rule, log

def SUCCESS():
    return jsonify({'res': True})

def ERROR():
    return jsonify({'res': False})

def get_para(req, para):
    para = req.form.get(para)
    try:
        return json.loads(para)
    except:
        return para

@app.route('/')
def index():
    return 'Hello world'

@api.route('/login/status/')
def get_login_status():
    return jsonify(robot.get_login_status())

@api.route('/info/')
def get_robot_info():
    if not robot.loginned:
        return ERROR()
    return jsonify(robot.get_robot_info())

@api.route('/trans/', methods=['POST'])
def change_trans_status():
    if request.method == 'POST':
        trans_status = get_para(request, 'trans_status')
        if trans_status == robot.work:
            return ERROR()
        elif trans_status and not robot.work:
            robot.start()
        else:
            robot.stop()
        return SUCCESS()
    else:
        return ERROR()

@api.route('/time/', methods=['POST'])
def change_delay():
    if request.method == 'POST':
        if not robot.loginned:
            return ERROR() 
        if robot.set_time(get_para(request, 'time')):
            return SUCCESS()
        else:
            return ERROR()
    else:
        return ERROR()

@api.route('/groups/')
def get_groups():
    return jsonify(robot.get_groups_list())

@api.route('/group/', methods=['POST'])
def get_group():
    try:
        if request.method == 'POST':
            if not robot.loginned:
                return ERROR() 
            puid = get_para(request, 'puid')
            info = robot.get_group_info(puid)
            if info:
                return jsonify(info)
            else:
                return ERROR()
        else:
            return ERROR()
    except Exception as e:
        log.error(e)
        return ERROR()

@api.route('/group/trans/', methods=['POST'])
def switch_group_trans():
    if request.method == 'POST':
        if not robot.loginned:
            return ERROR()
        puid = get_para(request, 'puid')
        val = get_para(request, 'val')
        group = robot.find_in_trans(puid)
        if not group:
            group = robot.add_group(puid=puid)
        if val and not group.work:
            group.work = True
            group.start()
        elif not val and group.work:
            group.work = False
            group.stop()
        return SUCCESS()
    else:
        return ERROR()

@api.route('/group/target/', methods=['POST'])
def set_group_target():
    if request.method == 'POST':
        if not robot.loginned:
            return ERROR()
        puid = get_para(request, 'puid')
        target = get_para(request, 'target')
        group = robot.find_in_trans(puid)
        if not group:
            group = robot.add_group(puid=puid)
        group.set_target_group(target)
        return SUCCESS()
    else:
        return ERROR()

@api.route('/group/white/', methods=['POST'])
def set_white():
    if request.method == 'POST':
        if not robot.loginned:
            return ERROR()
        puid = get_para(request, 'puid')
        white = get_para(request, 'white')
        group = robot.find_in_trans(puid)
        if not group:
            group = robot.add_group(puid=puid)
        group.set_white(white)
        return SUCCESS()
    else:
        return ERROR()

@api.route('/group/rule/', methods=['POST'])
def set_group_rule():
    if request.method == 'POST':
        if not robot.loginned:
            return ERROR()
        puid = get_para(request, 'puid')
        rules = get_para(request, 'rules')
        group = robot.find_in_trans(puid)
        if not group:
            group = robot.add_group(puid=puid)
        group.set_rules(rules)
        return SUCCESS()
    else:
        return ERROR()

@api.route('/group/remove/', methods=['POST'])
def remove_members():
    if request.method == 'POST':
        if not robot.loginned:
            return ERROR()
        puid = get_para(request, 'puid')
        members = get_para(request, 'members')
        group = robot.find_in_trans(puid)
        if not group:
            group = robot.add_group(puid=puid)
        group.remove_members(members)
        return SUCCESS()
    else:
        return ERROR()

@socket.on('connect')
def connect():
    pass

@socket.on('login')
def login():
    server_backgroud(robot.login)

@socket.on('logout')
def logout():
    server_backgroud(robot.logout)

host = '0.0.0.0'
port = 9777
app.register_blueprint(api, url_prefix='/api')

try:
    with open(CONF_PATH, 'rb') as conf:
        robot = pickle.load(conf)
        robot.load_config()
except:
    robot = Group_robot()

def end_process(name):
    if len(sys.argv) > 1:
        if sys.argv[1] == 'end':
            process_list = [p for p in psutil.process_iter() if p.name() == name]
            process_list.sort(key=lambda x: x.create_time())
            for p in process_list:
                p.kill()

def exist_process(name):
    return len([p for p in psutil.process_iter() if p.name() == name]) > (4 if app.debug else 2)

if __name__ == '__main__':
    process_name = 'group_robot_api.exe'
    end_process(process_name)
    if not exist_process(process_name):
        socket.run(app, host=host, port=port)
