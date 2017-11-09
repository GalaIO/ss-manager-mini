# -*- coding:utf8 -*-
'''
Add database models.
'''
from . import db
from deamon.command import Command, command_queue, queue
from deamon.handler import stat_port_map
import json

class System(db.Model):
    __tablename__ = 'system'
    name = db.Column(db.String(64), primary_key=True)
    def __repr__(self):
        return '<System %r>' % self.name

class CommandModel:
    @staticmethod
    def add_user(alloc_port, password):
        queue.push(command_queue, Command(alloc_port, password, Command.ADD_COMMAND))

    @staticmethod
    def remove_user(alloc_port):
        queue.push(command_queue, Command(alloc_port, '', Command.REMOVE_COMMAND))

class StatModel:
    @staticmethod
    def get_bandwidth_by_port(port):
        port = str(port)
        if stat_port_map.haskey(port):
            return stat_port_map[port]
        return 0
    @staticmethod
    def get_bandwidths():
        data = stat_port_map
        stat_port_map.clear()
        return data

