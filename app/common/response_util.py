# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

from flask import make_response
import json


class Response(object):
    ERR_NONE = 200
    ERR_INTERERR = 500
    ERR_ERRREQUEST = 400
    simple_template = '{"code":500, "msg":%s, "content": null}'
    def __init__(self, content, code=ERR_NONE, msg='ok'):
        self.code = code
        self.msg = msg
        self.content = content
    def __str__(self):
        try:
            data = '{"code":%s, "msg":"%s", "content": %s}' %(self.code, self.msg, json.dumps(self.content))
        except Exception, e:
            return Response.simple_template % e.message
        return data

def make_rest_response(content, code=Response.ERR_NONE, msg='ok'):
    return make_response(str(Response(content, code, msg)))
