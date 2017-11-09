# -*- encoding: utf-8 -*-
import config

__author__ = 'GalaIO'

import threading
import socket
import json
import logging
from command import Command, command_queue, queue
from handler import stat_port_map, handle_stat
from config import Config

BUF_SIZE = 1024

class CliThread(threading.Thread):
    def __init__(self):
        self.stop_thread = False
        threading.Thread.__init__(self)

    def run(self):
        while not self.stop_thread:
            # 从键盘读入
            data = input('>')
            if data == 1:
                print 'print map'
                for key, value in stat_port_map.items():
                    print key, value
            queue.push(command_queue, Command(8001, '7cd308cc059', Command.ADD_COMMAND))
        print 'CliThread exit!'

    def stop(self):
        self.stop_thread = True

class StatThread(threading.Thread):
    def __init__(self):
        self.stop_thread = False
        threading.Thread.__init__(self)

    def run(self):
        logging.info('build socket udp....' + str(Config.SSSERVER_ADDR))
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        logging.info('connection timeout is 0.6s..')
        logging.info('send ping')
        client.sendto(b'ping', Config.SSSERVER_ADDR)
        data,addr = client.recvfrom(BUF_SIZE)
        logging.info('receive', data)
        client.settimeout(0.6)
        while True:
            # 检查队列
            while command_queue.qsize() > 0:
                command = queue.pop(command_queue)
                msg = command.get_command()
                logging.info('queue command send..', msg)
                client.sendto(msg, Config.SSSERVER_ADDR)
                data,addr = client.recvfrom(BUF_SIZE)
                logging.info('queue command receive..', data)
            try:
                data,addr = client.recvfrom(BUF_SIZE)
            except Exception, e:
                continue
            logging.info('receive stat..', data)
            handle_stat(data)
        client.close()
        print 'StatThread exit!'

    def stop(self):
        self.stop_thread = True

if __name__ == '__main__':
    th1 = StatThread()
    th2 = CliThread()
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    print 'app is exit!!!'

