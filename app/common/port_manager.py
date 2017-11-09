# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

from config import Config

port_avaliable_map = {}
cur_max_port = Config.SSPORT_INIT

def genport():
    global cur_max_port
    if len(port_avaliable_map) < Config.SSPORT_SIZE:
        cur_max_port += 1
        port_avaliable_map[cur_max_port] = True
        return cur_max_port
    else:
        for key, value in port_avaliable_map.items():
            if value == False:
                port_avaliable_map[key] = True
                return key
    # 没找到 返回负数
    return -1

def hasport(port):
    if port_avaliable_map.has_key(port):
        return port_avaliable_map[port]
    return False

def removeport(port):
    port_avaliable_map[port] = False

# test
if __name__ == '__main__':
    print genport()
    print hasport(Config.SSPORT_INIT+1)
    removeport(Config.SSPORT_INIT+1)
    print hasport(Config.SSPORT_INIT+1)
    print genport()
