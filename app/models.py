# -*- coding:utf8 -*-
'''
Add database models.
'''
from . import db
from deamon.command import Command, command_queue, queue
import datetime
from common import port_manager
import logging

class Port(db.Model):
    __tablename__ = 'port'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    bandwidth = db.Column(db.Float, nullable=False, default=0)
    bandwidth_used = db.Column(db.Float, nullable=False, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    @staticmethod
    def add_port(name, user_id, port, password, bandwidth):
        CommandModel.add_user(port, password)
        qu = Port.query.filter(Port.user_id == user_id).first()
        if qu:
            qu.name = name
            qu.port = port
            qu.password = password
            qu.bandwidth += bandwidth
            qu.active = True
        else:
            p = Port(user_id=user_id, name=name, password=password, port=port, bandwidth=bandwidth)
            db.session.add(p)
        db.session.commit()

    @staticmethod
    def update_by_user(name, user_id, password, bandwidth):
        qu = Port.query.filter(Port.user_id == user_id).first()
        if qu:
            if name:
                qu.name = name
            if password:
                qu.password = password
            if bandwidth:
                qu.bandwidth += bandwidth
            qu.active = True
            db.session.commit()

    @staticmethod
    def query_by_port(port, user_id):
        ps = Port.query.filter(Port.port==port, Port.user_id == user_id).first()
        re = []
        for p in ps:
            re.append({
                'id': p.id,
                'user_id': p.user_id,
                'port': p.port,
                'password': p.password,
                'name': p.name,
                'active': p.active,
                'bandwidth': p.bandwidth,
                'bandwidth_used': p.bandwidth_used,
                'create_time': p.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return re
    @staticmethod
    def query_by_port(port):
        p = Port.query.filter(Port.port==port).first()
        if p:
            p = {
                'id': p.id,
                'user_id': p.user_id,
                'port': p.port,
                'password': p.password,
                'name': p.name,
                'active': p.active,
                'bandwidth': p.bandwidth,
                'bandwidth_used': p.bandwidth_used,
                'create_time': p.create_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        return p


    @staticmethod
    def lists():
        ps = Port.query.filter().all()
        re = []
        for p in ps:
            re.append({
                'id': p.id,
                'user_id': p.user_id,
                'port': p.port,
                'password': p.password,
                'name': p.name,
                'active': p.active,
                'bandwidth': p.bandwidth,
                'bandwidth_used': p.bandwidth_used,
                'create_time': p.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return re

    @staticmethod
    def remove_port(port):
        CommandModel.remove_user(port)
        p = Port.query.filter(Port.active==True, Port.port==port).first()
        if p is None:
            return
        p.active = False
        p.port = -2
        db.session.commit()

    @staticmethod
    def reenable_port_all():
        '''
        从port表查出所有可用的用户，并重新开启端口
        :return:
        '''
        ports = Port.query.filter(Port.active==True).all()
        for p in ports:
            if port_manager.genport(p.user_id, p.port) > 0:
                CommandModel.add_user(p.port, p.password)
                logging.info("reenable %d port, with %s user" % (p.port, p.user_id))
            else:
                p.active = False
                logging.error("%s is duplicate port with %d" % (p.user_id, p.port))

        db.session.commit()

class Stat(db.Model):
    __tablename__ = 'stat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    bw_use = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    @staticmethod
    def backup(data_map):
        for key, value in data_map.items():
            st = Stat(port=key, bw_use=value['bw'], user_id=value['id'])
            db.session.add(st)
            # 校验用户流量
            p = Port.query.filter(Port.active == True, Port.port == key, Port.user_id==value['id']).first()
            if p:
                p.bandwidth_used += value['bw']
                # 用户流量超限，删除
                if p.bandwidth_used >= p.bandwidth:
                    p.active = False
                    p.port = -2
                    CommandModel.remove_user(key)
        db.session.commit()
        data_map.clear()

    @staticmethod
    def get_bandwidth_by_port(port, starttime, endtime):
        '''
        某一天 比如2016 10 20
        starttime=datetime.datetime.strptime('2016-10-20','%Y-%m-%d')
        delta=datetime.timedelta(days=1)
        endtime=starttime+delta
        近七天 比如2016 10 20
        starttime=datetime.datetime.strptime('2016-10-20','%Y-%m-%d')
        delta=datetime.timedelta(days=7)
        endtime=starttime-delta
        近30天 比如2016 10 20
        starttime=datetime.datetime.strptime('2016-10-20','%Y-%m-%d')
        delta=datetime.timedelta(days=30)
        endtime=starttime-delta
        近一年 比如2016 10 20
        starttime=datetime.datetime.strptime('2016-10-20','%Y-%m-%d')
        delta=datetime.timedelta(days=365)
        endtime=starttime-delta
        :param port:
        :param starttime:
        :param endtime:
        :return:
        '''
        sts = Stat.query.filter(Stat.port==port, Stat.create_time.between(starttime, endtime)).all()
        re = []
        datetime.timedelta
        for st in sts:
            re.append({
                'id': st.id,
                'user_id': st.user_id,
                'port': st.port,
                'bw_use': st.bw_use,
                'create_time': st.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return re
    @staticmethod
    def get_bandwidths_result(starttime, endtime):
        sts = Stat.query.filter(Stat.create_time.between(starttime, endtime)).all()
        re = []
        for st in sts:
            re.append({
                'id': st.id,
                'user_id': st.user_id,
                'port': st.port,
                'bw_use': st.bw_use,
                'create_time': st.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return re
    @staticmethod
    def get_bandwidth_by_port_report(port, starttime, endtime, type):
        if type == 'day':
            dtype = 'hour'
            label = range(0, 24)
        elif type == 'month':
            dtype = 'day'
            label = range(1, 31)
        else:
            dtype = 'month'
            label = range(1, 13)
        sts = db.session.query(db.func.sum(Stat.bw_use), db.extract(dtype, Stat.create_time)).filter(Stat.port==port, Stat.create_time.between(starttime, endtime)).group_by(Stat.port, db.extract(dtype, Stat.create_time)).all()
        port_list = [0] * len(label)
        for st in sts:
            port_list[st[1]-1] = st[0]
        return {
            "label": label,
            "data": port_list
        }
    @staticmethod
    def get_bandwidths_result_report(starttime, endtime, type):
        if type == 'day':
            dtype = 'hour'
            label = range(0, 24)
        elif type == 'month':
            dtype = 'day'
            label = range(1, 31)
        else:
            dtype = 'month'
            label = range(1, 13)
        sts = db.session.query(Stat.port, db.func.sum(Stat.bw_use), db.extract(dtype, Stat.create_time)).filter(Stat.create_time.between(starttime, endtime)).group_by(Stat.port, db.extract(dtype, Stat.create_time)).all()
        port_list = {}
        for st in sts:
            if not port_list.has_key(st[0]):
                port_list[st[0]] = [0] * len(label)
            port_list[st[0]][st[2]-1] = st[1]
        return {
            "label": label,
            "data": port_list
        }

class CommandModel:
    @staticmethod
    def add_user(alloc_port, password):
        queue.push(command_queue, Command(alloc_port, password, Command.ADD_COMMAND))

    @staticmethod
    def remove_user(alloc_port):
        queue.push(command_queue, Command(alloc_port, '', Command.REMOVE_COMMAND))


