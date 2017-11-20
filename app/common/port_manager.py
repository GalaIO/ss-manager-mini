# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'


import json
from config import Config
import app.models
import logging
from datetime import datetime

port_avaliable_map = {}
cur_max_port = Config.SSPORT_INIT

def genport(user_id, cport=-1):
    if cport > 0:
        if (not hasport(cport)) and cport >= Config.SSPORT_INIT \
                and cport <= Config.SSPORT_SIZE + Config.SSPORT_INIT:
            port_avaliable_map[cport] = user_id
            return cport
        return -1
    global cur_max_port
    while cur_max_port <= Config.SSPORT_SIZE + Config.SSPORT_INIT and hasport(cur_max_port):
        cur_max_port += 1

    if cur_max_port <= Config.SSPORT_SIZE + Config.SSPORT_INIT:
        port_avaliable_map[cur_max_port] = user_id
        return cur_max_port

    for key, value in port_avaliable_map.items():
        if value == None:
            port_avaliable_map[key] = user_id
            return key
    # 没找到 返回负数
    return -1

def hasport(port):
    if port_avaliable_map.has_key(port):
        return port_avaliable_map[port]!=None
    return False

def hasuserid(userid):
    for key, value in port_avaliable_map.items():
        if value == userid:
            return True
    return False

def removeport(port):
    if hasport(port):
        port_avaliable_map[port] = None
        return True
    return False


stat_port_map = {}
count = datetime.now()
def handle_stat(data):
    global count
    info = json.loads(data[5:])
    for key, value in info.items():
        key = int(key)
        if stat_port_map.has_key(key):
            stat_port_map[key]['bw'] += float(value)/1000
        else:
            if port_avaliable_map.has_key(key) == False:
                port_avaliable_map[key] = -1
            stat_port_map[key] = {}
            stat_port_map[key]['bw'] = float(value)/1000
            stat_port_map[key]['id'] = port_avaliable_map[key]

    # 每分钟写入
    cur = datetime.now()
    if (cur-count).seconds >= Config.SSBACKUP_COUNT *10:
        logging.info('stat buffer write in db....')
        count = cur
        app.models.Stat.backup(stat_port_map)

# test
if __name__ == '__main__':
    print genport()
    print hasport(Config.SSPORT_INIT+1)
    removeport(Config.SSPORT_INIT+1)
    print hasport(Config.SSPORT_INIT+1)
    print genport()
