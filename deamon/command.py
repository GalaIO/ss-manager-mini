# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'
import Queue


class queue:
    @staticmethod
    def push(queue, element):
        queue.put(element, block=True, timeout=None)

    @staticmethod
    def pop(queue):
        try:
            return queue.get(block=True, timeout=60)#接收消息
        except Queue.Empty:
            return None

command_queue = Queue.Queue(100)

class Command:
    '''
    命令对象
    '''
    def __init__(self, alloc_port, password, ctype):
        self.alloc_port = alloc_port
        self.password = password
        self.ctype = ctype

    def get_command(self):
        if isinstance(self.ctype, int) == False or self.ctype > len(Command.SWITCH):
            raise Exception('unknow_command')
        return Command.SWITCH[self.ctype](self)

    def get_add_command(self):
        return b'add: {"server_port":%s, "password":"%s"}' % (self.alloc_port, self.password)

    def get_remove_command(self):
        return b'remove: {"server_port":%s}' % self.alloc_port


    ADD_COMMAND = 0x01
    REMOVE_COMMAND = 0x02
    SWITCH = {
        ADD_COMMAND: get_add_command,
        REMOVE_COMMAND: get_remove_command
    }