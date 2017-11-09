# -*- coding:utf8 -*-
'''
index route.
'''
from flask import render_template, make_response, request
from . import main
from ..models import Stat, Port
from ..common.response_util import make_rest_response, Response
from ..common import port_manager

# 定义路由函数
@main.route('/', methods=['GET', 'POST'])
def index_route():
    return render_template('index.html', name='anomymous')

@main.route('/add-port', methods=['POST'])
def add_port():
    password = request.form.get('password')
    user_id = int(request.form.get('user_id', default=-1))
    if user_id>0 and port_manager.hasuserid(user_id):
        return make_rest_response('you have a port or userid is invalid!', code=Response.ERR_INTERERR)
    port = port_manager.genport(user_id)
    name = request.form.get('name')
    bandwidth = float(request.form.get('bandwidth', default=0))
    if port > 0 and user_id>0 and name and password:
        Port.add_port(name, user_id, port, password, bandwidth)
        return make_rest_response({"port": port})

    return make_rest_response('no more port for you!', code=Response.ERR_INTERERR)
@main.route('/update-user', methods=['POST'])
def update_user():
    password = request.form.get('password')
    user_id = int(request.form.get('user_id', default=-1))
    if user_id>0 and port_manager.hasuserid(user_id):
        return make_rest_response('you have a port or userid is invalid!', code=Response.ERR_INTERERR)
    name = request.form.get('name')
    bandwidth = float(request.form.get('bandwidth', default=0))
    if user_id>0 and name and password:
        Port.update_by_user(name, user_id, password, bandwidth)
        return make_rest_response(None)

    return make_rest_response('no more port for you!', code=Response.ERR_INTERERR)
@main.route('/remove-port', methods=['POST'])
def remove_port():
    port = int(request.form.get('port', default='-1'))
    if port > 0 and port_manager.hasport(port):
        port_manager.removeport(port)
        Port.remove_port(port)
        return make_rest_response(None)

    return make_rest_response('not found the port!', code=Response.ERR_INTERERR)

@main.route('/query-port', methods=['GET'])
def query_port():
    return make_rest_response(Port.lists())

@main.route('/query-port/<port>', methods=['GET'])
def query_port_by_port(port):
    return make_rest_response(Port.query_by_port(port))


@main.route('/stat', methods=['GET'])
def stat():
    return make_rest_response(Stat.get_bandwidths_result())

@main.route('/stat/<port>', methods=['GET'])
def stat_port(port):
    return make_rest_response(Stat.get_bandwidth_by_port(port))