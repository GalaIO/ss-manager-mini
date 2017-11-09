# -*- coding:utf8 -*-
'''
Add database models.
'''
from . import db
from deamon.command import Command, command_queue, queue
from datetime import datetime

class Port(db.Model):
    __tablename__ = 'port'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @staticmethod
    def add_port(name, user_id, port, password):
        p = Port(user_id=user_id, name=name, password=password, port=port)
        db.session.add(p)
        db.session.commit()

    @staticmethod
    def remove_port(port):
        p = Port.query.filter(Port.active==True, Port.port==port).first()
        if p is None:
            return
        p.active = False
        db.session.commit()

class Stat(db.Model):
    __tablename__ = 'stat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    bw_use = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @staticmethod
    def backup(data_map):
        for key, value in data_map.items():
            st = Stat(port=key, bw_use=value['bw'], user_id=value['id'])
            db.session.add(st)
        db.session.commit()
        data_map.clear()

    @staticmethod
    def get_bandwidth_by_port(port):
        sts = Stat.query.filter(Stat.port==port).all()
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
    def get_bandwidths_result():
        sts = Stat.query.filter().all()
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

class CommandModel:
    @staticmethod
    def add_user(alloc_port, password):
        queue.push(command_queue, Command(alloc_port, password, Command.ADD_COMMAND))

    @staticmethod
    def remove_user(alloc_port):
        queue.push(command_queue, Command(alloc_port, '', Command.REMOVE_COMMAND))


