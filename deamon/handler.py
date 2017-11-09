# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import json

stat_port_map = {}
def handle_stat(data):
    info = json.loads(data[5:])
    for key, value in info.items():
        if stat_port_map.has_key(key):
            stat_port_map[key] += float(value)/1000
        else:
            stat_port_map[key] = float(value)/1000
