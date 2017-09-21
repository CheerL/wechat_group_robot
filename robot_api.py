import os
import wxpy
import time
import copy
import random
import urllib
import pickle
import asyncio
import parallel as pl
from __init__ import PIC_PATH, SRC_PATH, CONF_PATH, PKL_PATH, PUID_PATH, server_send, server_pause
from logger import LogHandler
from collections import OrderedDict

log = LogHandler('robot')
AVA_PATH = os.path.join(PIC_PATH, 'avatar')
if not os.path.exists(AVA_PATH) or not os.path.isdir(AVA_PATH):
    os.mkdir(AVA_PATH)

class Group_robot(object):
    qr_path = os.path.join(SRC_PATH, 'qr.png')
    wx_path = os.path.join(PIC_PATH, 'begin.png')
    trans_delay = 10

    def __init__(self):
        self.work = False
        self.loginning = False
        self.loginned = False
        self.bot = None
        self.name = None
        self.puid = None
        self.avatar_path = None
        self.trans_groups = list()
        self.send_list = list()
        self.trans_count = 0
        self.trans_text_count = 0
        self.trans_pic_count = 0
        self.reject_count = 0
        self.time = {
            'receive_delay': 30,
            'msg_gap_low': 100,
            'msg_gap_up': 300,
            "group_gap_low": 100,
            "group_gap_up": 300,
            "rest_msg_num": 10,
            "rest_time": 5
        }

    def save_config(self):
        with open(CONF_PATH, 'wb') as conf:
            temp_trans = [copy.copy(group) for group in self.trans_groups]
            for group in temp_trans:
                group.robot = None
                group.registered = False
            temp = copy.copy(self)
            temp.bot = None
            temp.loginned = False
            temp.loginning = False
            temp.trans_groups = temp_trans
            pickle.dump(temp, conf)
        log.info('保存设置成功')

    def load_config(self):
        for group in self.trans_groups:
            group.robot = self
        log.info('加载设置成功')

    def clear_config(self):
        self.name = None
        self.puid = None
        self.avatar_path = None
        self.trans_groups = list()
        self.trans_count = 0
        self.trans_pic_count = 0
        self.trans_text_count = 0
        self.reject_count = 0
        for path in [CONF_PATH, PKL_PATH, PUID_PATH]:
            try:
                os.remove(path)
            except:
                pass
        log.info('清理设置')

    def qr_callback(self, uuid, status, qrcode):
        if qrcode:
            log.info('成功获取二维码')
            if os.path.exists(self.qr_path):
                os.remove(self.qr_path)
                self.qr_path = self.qr_path.replace('.png', '0.png')
            with open(self.qr_path, 'wb') as pic:
                pic.write(qrcode)
            server_send({
                'style': 'login',
                'pic_path': self.qr_path,
                'text': '请扫描二维码',
                'status': 1
            })
        else:
            try:
                os.remove(self.qr_path)
            except:
                pass
            log.info('等待确认登录')
            server_send({
                'style': 'login',
                'pic_path': self.wx_path,
                'text': '请稍候',
                'status': 1
            })

    def logout_callback(self):
        self.loginned = False
        self.stop()
        log.info('{}退出登录'.format(self.name))
        server_send({
            'style': 'login',
            'pic_path': self.wx_path,
            'text': '请点击登录按钮',
            'status': 0
        })

    def update_groups(self):
        self.bot.core.get_chatrooms(update=True)

    def login(self):
        if not self.loginned and not self.loginning:
            self.loginning = True
            try:
                self.bot = wxpy.Bot(
                    cache_path=PKL_PATH,
                    qr_path=self.qr_path,
                    qr_callback=self.qr_callback,
                    logout_callback=self.logout_callback
                    )
                self.loginned = True
                self.loginning = False
                self.update_groups()
                self.bot.enable_puid(path=PUID_PATH)
            except:
                self.loginning = False
                server_send({
                    'style': 'error'
                })
                server_send({
                    'style': 'login',
                    'pic_path': self.wx_path,
                    'text': '请点击登录按钮',
                    'status': 0
                })
                os.remove(PKL_PATH)
                return

            if not self.bot.self.name:
                raise Exception
            elif self.name != self.bot.self.name:
                self.clear_config()
                self.name = self.bot.self.name
                self.puid = self.bot.self.puid
                self.avatar_path = os.path.join(AVA_PATH, '{}.png'.format(self.puid))
                self.bot.self.get_avatar(self.avatar_path)
            else:
                for group in self.trans_groups:
                    try:
                        group.check_puid()
                        group.register()
                    except Exception as e:
                        log.error(e)

            log.info('{}登录成功'.format(self.name))
            server_send({
                'style': 'login',
                'pic_path': self.avatar_path,
                'text': '{}登录成功'.format(self.name),
                'status': 2
            })
            self.save_config()
            self.start()
            for file in os.listdir(SRC_PATH):
                if 'qr' in file:
                    file_path = os.path.join(SRC_PATH, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def logout(self):
        self.stop()
        self.bot.logout()
        self.save_config()

    def get_login_status(self):
        if not self.loginned and not self.loginning:
            return {
                'style': 'login',
                'pic_path': self.wx_path,
                'text': '请点击登录按钮',
                'status': 0
            }
        elif self.loginned:
            return {
                'style': 'login',
                'pic_path': self.avatar_path,
                'text': '登录成功',
                'status': 2
            }
        elif self.loginning:
            if os.path.exists(self.qr_path):
                return {
                    'style': 'login',
                    'pic_path': self.qr_path,
                    'text': '请扫描二维码',
                    'status': 1
                }
            else:
                return {
                    'style': 'login',
                    'pic_path': self.wx_path,
                    'text': '请稍候',
                    'status': 1
                }

    def get_robot_info(self):
        if self.loginned:
            return {
                'name': self.name,
                'pic_path': self.avatar_path,
                'group_num': len(self.bot.groups()),
                'trans_swith': self.work,
                'time': self.time,
                'trans_group': [
                    {
                        'name': group.name,
                        'puid': group.puid
                    }
                    for group in self.trans_groups
                    if group.work
                ],
                'trans_count': self.trans_count,
                'trans_text_count': self.trans_text_count,
                'trans_pic_count': self.trans_pic_count,
                'reject_count': self.reject_count
            }
            log.info('发送robot{}信息'.format(self.name))

    def get_avatar(self, member):
        pic_path = os.path.join(AVA_PATH, '{}.png'.format(member.puid))
        if not os.path.exists(pic_path):
            member.get_avatar(pic_path)
            log.info('获取{}头像'.format(member.name))

    def get_groups_list(self):
        self.update_groups()
        log.info('发送群列表')
        return [
            {
                'name': group.name,
                'puid': group.puid
            }
            for group in self.bot.groups()
        ]

    def get_group_info(self, puid):
        self.update_groups()
        group = wxpy.ensure_one(self.bot.search(puid=puid))
        if group:
            # pl.run_thread_pool([(self.get_avatar, (member,)) for member in group.members], False)
            avater_path = os.path.join(AVA_PATH, '{}.png'.format(group.puid))
            group.get_avatar(avater_path)

            _group = self.find_in_trans(group.puid)
            if _group:
                is_trans = _group.work if self.work else False
                rule_list = [rule.__dict__ for _, rule in _group.rules.items()]
                target_group = [
                    {
                        'name': group.name,
                        'puid': group.puid
                    }
                    for group in _group.target_groups()
                ]
                white = _group.white
            else:
                is_trans = False
                rule_list = []
                target_group = []
                white = []
            log.info('发送群{}信息'.format(group.name))
            return {
                'name': group.name,
                'avatar': avater_path,
                'puid': group.puid,
                'member': [
                    {
                        'name': member.name,
                        'puid': member.puid,
                        'pic_path': os.path.join(AVA_PATH, '{}.png'.format(member.puid))
                    }
                    for member in group.members
                ],
                'white': white,
                'people_num': len(group.members),
                'rule': rule_list,
                'is_trans': is_trans,
                'is_owner': group.is_owner,
                'target_group': target_group
            }
        else:
            return None

    def find_in_trans(self, puid):
        temp = [group for group in self.trans_groups if group.puid == puid]
        if temp:
            return temp[0]
        else:
            return None
    def set_time(self, new_time):
        try:
            for key, val in new_time.items():
                new_time[key] = int(val)
            if new_time['msg_gap_low'] <= new_time['msg_gap_up'] and new_time['group_gap_low'] < new_time['group_gap_up']:
                for key, val in new_time.items():
                    self.time[key] = val
                log.info('成功修改时间')
                self.save_config()
                return True
            else:
                return False
        except:
            return False
        
    def get_group(self, puid=None, name=None):
        try:
            if name:
                return wxpy.ensure_one(self.bot.groups().search(name=name))
            else:
                return wxpy.ensure_one(self.bot.search(puid=puid))
        except:
            error = 'No such group with {}'.format('name {}'.format(name) if name else 'puid {}'.format(puid))
            raise Exception(error)

    def add_group(self, puid=None, final_group=None):
        if final_group and isinstance(final_group, Group):
            pass
        elif puid and isinstance(puid, str):
            final_group = Group(self, puid=puid)
        self.trans_groups.append(final_group)
        self.save_config()
        return final_group

    def start(self):
        def run():
            async def get_msg_to_send():
                while self.work:
                    try:
                        for group in self.trans_groups:
                            group.add_to_send()
                        await asyncio.sleep(self.trans_delay)
                    except Exception as e:
                        log.error(e)
                        time.sleep(2)

            async def send_msg_to_target():
                job_list = []
                count = 0
                while self.work:
                    try:
                        if job_list:
                            msg_dict, target, group, sleep_time = job_list.pop(0)
                            group.send_to_target(msg_dict['name'], msg_dict, target)
                            if job_list:
                                log.info('休息{}秒后继续转发{}的消息'.format(str(sleep_time), msg_dict['name']))
                                await asyncio.sleep(sleep_time)
                            else:
                                group.result_report(msg_dict['name'], msg_dict['rule'])
                                group.total_people_num = 0
                                log.info('{}的消息转发完成'.format(msg_dict['name']))
                        elif not job_list and self.send_list:
                            if count is self.time['rest_msg_num']:
                                count = 0
                                await asyncio.sleep(self.time['rest_time'])
                            else:
                                count += 1
                                msg_dict = self.send_list.pop(0)
                                group = self.find_in_trans(msg_dict['puid'])
                                job_list = [(
                                    msg_dict,
                                    target,
                                    group,
                                    random.randint(
                                        self.time['group_gap_low'],
                                        self.time['group_gap_up']
                                        )
                                ) for target in group.target_groups()]
                                sleep_time = random.randint(
                                    self.time['msg_gap_low'],
                                    self.time['msg_gap_up']
                                    )
                                log.info('休息{}秒后开始转发{}的消息'.format(str(sleep_time), msg_dict['name']))
                                await asyncio.sleep(sleep_time)
                        else:
                            # log.info('转发队列为空，休息{}秒'.format(str(self.trans_delay)))
                            await asyncio.sleep(self.trans_delay)
                    except Exception as e:
                        log.error(e)
                        time.sleep(2)

            async def auto_save_config():
                while self.work:
                    try:
                        self.save_config()
                        await asyncio.sleep(60)
                    except Exception as e:
                        log.error(e)
            
            log.info('任务线程打开')
            loop = asyncio.new_event_loop()
            tasks = [send_msg_to_target(), get_msg_to_send(), auto_save_config()]
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()
            log.info('任务线程结束')
            
        self.work = True
        for group in self.trans_groups:
            group.start()

        if not pl.search_thread(name='trans_work'):
            pl.run_thread([(run, ())], 'trans_work', False, 32)
            log.info('开始转发')

    def stop(self):
        self.work = False
        for group in self.trans_groups:
            group.stop()
        if pl.search_thread(name='trans_work'):
            pl.kill_thread(name='trans_work')
        log.info('结束转发')

class Group(object):
    def __init__(self, robot, puid):
        self.robot = robot
        self.work = False
        self.target_puids = set()
        self.recieve_dict = OrderedDict()
        self.rules = dict()
        self.white = list()
        self.total_people_num = 0
        self.puid = puid
        self.name = self.get_group(self.puid).name
        self.registered = False
        self.register()

    def check_puid(self):
        if self.robot and self.robot.bot:
            if self.puid and self.name:
                try:
                    group = self.robot.get_group(self.puid)
                    if group.name != self.name:
                        raise Exception()
                except:
                    try:
                        group = self.robot.get_group(name=self.name)
                        self.puid = group.puid
                    except:
                        raise Exception('trans_group not found')
            elif self.puid and not self.name:
                try:
                    group = self.robot.get_group(self.puid)
                    self.name = group.name
                except:
                    raise Exception('trans_group not found')
            elif not self.puid and self.name:
                try:
                    group = self.robot.get_group(name=self.name)
                    self.puid = group.puid
                except:
                    raise Exception('trans_group not found')
            else:
                raise Exception('trans_group not found')
            
            for puid in copy.copy(self.target_puids):
                try:
                    self.get_group(puid)
                except:
                    self.target_puids.remove(puid)

    def target_groups(self):
        return (self.get_group(puid) for puid in self.target_puids)

    def get_group(self, puid=None):
        if not puid:
            puid = self.puid
        return self.robot.get_group(puid=puid)

    def set_white(self, white):
        member_list = [member.name for member in self.get_group().members]
        for each in copy.copy(white):
            if each not in member_list:
                white.remove(each)
        self.white = white
        log.info('修改群{}的白名单'.format(self.name))

    def set_target_group(self, target_list):
        self.target_puids = {group.get('puid') for group in target_list}
        self.robot.save_config()
        log.info('修改群{}的转发目标'.format(self.name))

    def set_rules(self, rules):
        new_rule_dict = {
            rule['index']: rule
            for rule in rules
        }
        del_set = self.rules.keys() - new_rule_dict.keys()
        for key in del_set:
            del self.rules[key]
        for (key, val) in new_rule_dict.items():
            rule = self.rules.setdefault(key, Rule(val['keyword']))
            rule.include_words = val['include_words']
            rule.reject_words = val['reject_words']
            rule.index = val['index']
            rule.head = val['head']
            rule.tail = val['tail']
            rule.fail_report = val['fail_report']
            rule.success_report = val['success_report']
            rule.result_report = val['result_report']
            rule.include_report = val['include_report']
            rule.start_report = val['start_report']
        self.robot.save_config()
        log.info('修改群{}的转发规则'.format(self.name))

    def register(self):
        if self.robot and self.robot.bot:
            try:
                reply_config = wxpy.api.messages.MessageConfig(
                    self.robot.bot,
                    self.recieve,
                    self.get_group(self.puid),
                    ['Text', 'Picture'],
                    True,
                    True,
                    True
                    )
                self.robot.bot.registered.append(reply_config)
                self.registered = True
            except:
                self.work = False

    def start(self):
        if not self.robot or not self.robot.bot:
            return
        if not self.registered:
            self.register()
        self.robot.bot.registered.enable(self.recieve)
        log.info('群{}开始转发'.format(self.name))
        

    def stop(self):
        if not self.robot or not self.robot.bot:
            return
        self.robot.bot.registered.disable(self.recieve)
        log.info('群{}的停止转发'.format(self.name))

    def recieve(self, message):
        name = message.member.name
        if message.type == 'Text':
            text = message.text
            log.info('{}:{}'.format(name, text))
            if name in self.recieve_dict:
                try:
                    if '中止' in text:
                        self.recieve_dict.pop(name)
                        self.end_receive_report(name)
                        log.info('中止接收来自{}的消息'.format(name))
                    else:
                        rule = self.recieve_dict[name]['rule']
                        if name not in self.white:
                            if not rule.test_reject(text):
                                self.reject_error(name, rule)
                                return
                        self.add_message(name, message, rule, 'Text')
                except Exception as e:
                    log.error(e)

            else:
                for _, rule in self.rules.items():
                    if rule.keyword in text:
                        if name not in self.white:
                            if not rule.test_reject(text):
                                self.reject_error(name, rule)
                                return
                        if not rule.test_include(text):
                            self.include_error(name, rule)
                            return
                        self.add_message(name, message, rule, 'Text')
                        self.start_recieve_report(name, rule)

        elif message.type == 'Picture':
            log.info('{}:[图片]'.format(name))
            if name in self.recieve_dict:
                rule = self.recieve_dict[name]['rule']
                try:
                    self.add_message(name, message, rule, 'Picture')
                except Exception as e:
                    log.error(e)


    def add_message(self, name, message, rule, m_type):
        if m_type == 'Picture':
            tran_message = {
                'type': m_type,
                'path': os.path.join(PIC_PATH, message.file_name)
            }
            message_count = 'pic_num'
            message.get_file(tran_message['path'])
        elif m_type == 'Text':
            tran_message = {
                'type': m_type,
                'text': message.text
            }
            message_count = 'text_num'
        else:
            log.error('错误的消息类型')
            return

        dict_item = self.recieve_dict.setdefault(
            name,
            {
                'name': name,
                'time':time.time(),
                'message':[],
                'rule': rule,
                'text_num': 0,
                'pic_num': 0,
                'puid': self.puid
            }
        )
        dict_item['message'].append(tran_message)
        dict_item[message_count] += 1
        log.info('向{}的消息包中添加一条{}消息'.format(name, m_type))

    def add_to_send(self):
        recieve_dict = copy.copy(self.recieve_dict)
        for name, user_dict in recieve_dict.items():
            if time.time() - user_dict['time'] > int(self.robot.time['receive_delay']):
                self.recieve_dict[name]['message'] = [{
                    'text': '\n'.join([
                        msg['text'] for msg in user_dict['message']
                        if msg['type'] == 'Text'
                        ]),
                    'type': 'Text'
                }] + [msg for msg in user_dict['message'] if msg['type'] == 'Picture']
                self.robot.trans_count += 1
                try:
                    self.robot.send_list.append(self.recieve_dict.pop(name))
                    log.info('将{}的消息包添加到转发队列'.format(name))
                    self.success_report(name, user_dict['rule'], user_dict['pic_num'])
                except Exception as e:
                    log.error(e)
            else:
                break

    def send_to_target(self, name, user_dict, target):
        self.total_people_num += len(target.members)
        rule = user_dict['rule']
        for message in user_dict['message']:
            if message['type'] == 'Text':
                target.send_msg('\n'.join([
                    each for each in [
                        rule.head,
                        message['text'],
                        rule.tail
                    ]
                    if each]))
                self.robot.trans_text_count += 1
            elif message['type'] == 'Picture':
                target.send_image(message['path'])
                self.robot.trans_pic_count += 1
            log.info('向群{}转发来自{}的一条{}消息'.format(target.name, name, message['type']))

    def include_error(self, name, rule):
        text = rule.include_report.replace(
            '【@被收集者】', '@{}\n'.format(name)
        ).replace(
            '【关键词】', rule.keyword
        ).replace(
            '【包含词】', ''.join(['[{}]'.format(word) for word in rule.include_words if word])
        )
        log.info('{}的消息中信息不全，拒绝转发'.format(name))
        self.get_group(self.puid).send(text)

    def start_recieve_report(self, name, rule):
        text = rule.start_report.replace(
            '【@被收集者】', '@{}\n'.format(name)
        ).replace(
            '【关键词】', rule.keyword
        ).replace(
            '【收集时长】', str(self.robot.time['receive_delay'])
        )
        log.info('开始收集{}的消息'.format(name))
        self.get_group(self.puid).send(text)

    def reject_error(self, name, rule):
        text = rule.fail_report.replace(
                '【@被收集者】', '@{}\n'.format(name)
            ).replace(
                '【关键词】', rule.keyword
            ).replace(
                '【广告词】', ''.join(['[{}]'.format(word) for word in rule.reject_words if word])
            )
        self.robot.reject_count += 1
        log.info('{}的消息中含有广告词, 拒绝转发'.format(name))
        self.get_group(self.puid).send(text)

    def success_report(self, name, rule, pic_count):
        text = rule.success_report.replace(
                '【@被收集者】', '@{}\n'.format(name)
            ).replace(
                '【关键词】', rule.keyword
            ).replace(
                '【收集的图片数量】', str(pic_count)
            )
        log.info('{}的消息收集完成'.format(name))
        self.get_group(self.puid).send(text)

    def result_report(self, name, rule):
        text = rule.result_report.replace(
                '【@被收集者】', '@{}\n'.format(name)
            ).replace(
                '【关键词】', rule.keyword
            ).replace(
                '【已发送群数量】', str(len(self.target_puids))
            ).replace(
                '【所有群人数】', str(self.total_people_num)
            )
        self.get_group(self.puid).send(text)
    
    def end_receive_report(self, name):
        text = '@{name}\n中止收集转发本次消息'.format(
            name=name
        )
        log.info('{}主动中止消息收集'.format(name))
        self.get_group(self.puid).send(text)

    def remove_members(self, members):
        members_list = [wxpy.ensure_one(self.robot.bot.search(puid=puid)) for puid in members]
        self.get_group(self.puid).remove_members(members_list)
        self.robot.save_config()


class Rule(object):
    def __init__(self, keyword):
        self.keyword = keyword
        self.reject_words = list()
        self.include_words = list()
        self.head = ''
        self.tail = ''
        self.success_report = '【@被收集者】 已收集到【关键词】消息，并收集到【收集的图片数量】张图片，稍后将为您转发'
        self.fail_report = '【@被收集者】 您发送的消息与【关键词】无关，也请不要包含【广告词】，此类消息不予转发，谢谢'
        self.result_report = '【@被收集者】 已为您成功发送【关键词】消息到【已发送群数量】个群，预计将会被【所有群人数】人看到'
        self.start_report = '【@被收集者】 开始接收【关键词】消息，请在【收集时长】秒内输入相关信息, 若意外触发，请发送[中止]停止收集'
        self.include_report = '【@被收集者】 您所发送的内容信息不全，【关键词】应至少包含【包含词】'
        self.index = str(int(time.time()))
    def test_reject(self, text):
        for reject_word in self.reject_words:
            if reject_word in text:
                return False
        return True

    def test_include(self, text):
        for include_word in self.include_words:
            if include_word not in text:
                return False
        return True

def main():
    try:
        with open(CONF_PATH, 'rb') as conf:
            robot = pickle.load(conf)
            robot.load_config()
    except:
        robot = Group_robot()
    wxpy.embed()
    

if __name__ == '__main__':
    main()
