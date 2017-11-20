# -*- coding:utf8 -*-
'''
index route.
'''
from flask import render_template, make_response, request
from . import main
from ..models import Stat, Port
from ..common.response_util import make_rest_response, Response
from ..common import port_manager
import datetime

# 定义路由函数
@main.route('/', methods=['GET', 'POST'])
def index_route():
    return render_template('index2.html', name='anomymous')

@main.route('/port-manage', methods=['GET', 'POST'])
def port_manage_route():
    return render_template('user_manage.html', name='anomymous')

@main.route('/stat-manage', methods=['GET', 'POST'])
def stat_manage_route():
    return render_template('stat_manage.html', name='anomymous')

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

    port_manager.removeport(port)
    return make_rest_response('no more port for you!', code=Response.ERR_INTERERR)
@main.route('/update-user', methods=['POST'])
def update_user():
    password = request.form.get('password')
    user_id = int(request.form.get('user_id', default=-1))
    if user_id>0 and not port_manager.hasuserid(user_id):
        return make_rest_response('the port or userid is invalid!', code=Response.ERR_INTERERR)
    name = request.form.get('name')
    bandwidth = float(request.form.get('bandwidth', default=0))
    if user_id>0:
        Port.update_by_user(name, user_id, password, bandwidth)
        return make_rest_response(None)

    return make_rest_response('no more port for you!', code=Response.ERR_INTERERR)
@main.route('/remove-port/<port>', methods=['GET'])
def remove_port(port):
    port = int(port)
    if port > 0:
        Port.remove_port(port)
    if port > 0 and port_manager.hasport(port):
        port_manager.removeport(port)
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
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    type = request.args.get('type')
    if type == 'delta' :
        if starttime and endtime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d')
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d) and endtime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'day':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            endtime = starttime + delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'week':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=7)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'month':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=30)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'year':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=365)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    else:
        return make_rest_response('you should send right type!',
                                  code=Response.ERR_ERRREQUEST)

    return make_rest_response(Stat.get_bandwidths_result(starttime, endtime))

@main.route('/stat/<port>', methods=['GET'])
def stat_port(port):
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    type = request.args.get('type')
    if type == 'delta' :
        if starttime and endtime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d')
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d) and endtime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'day':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            endtime = starttime + delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'week':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=7)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'month':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=30)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'year':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=365)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    else:
        return make_rest_response('you should send right type!',
                                  code=Response.ERR_ERRREQUEST)

    return make_rest_response(Stat.get_bandwidth_by_port(port, starttime, endtime))
@main.route('/stat-report', methods=['GET'])
def stat_report():
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    type = request.args.get('type')
    if type == 'day':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            endtime = starttime + delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)

    elif type == 'month':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')

            starttime += datetime.timedelta(days=1)
            delta = datetime.timedelta(days=starttime.day-1)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'year':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            starttime += datetime.timedelta(days=1)
            endtime = starttime
            starttime = datetime.datetime.strptime('%s-1-1' % starttime.year, '%Y-%m-%d')
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    else:
        return make_rest_response('you should send right type!',
                                  code=Response.ERR_ERRREQUEST)

    return make_rest_response(Stat.get_bandwidths_result_report(starttime, endtime, type))

@main.route('/stat-report/<port>', methods=['GET'])
def stat_report_port(port):

    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    type = request.args.get('type')
    if type == 'day':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            endtime = starttime + delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)

    elif type == 'month':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')

            starttime += datetime.timedelta(days=1)
            delta = datetime.timedelta(days=starttime.day-1)
            endtime = starttime
            starttime = starttime - delta
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    elif type == 'year':
        if starttime:
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            starttime += datetime.timedelta(days=1)
            endtime = starttime
            starttime = datetime.datetime.strptime('%s-1-1' % starttime.year, '%Y-%m-%d')
        else:
            return make_rest_response('you should send starttime(%Y-%m-%d)!',
                                      code=Response.ERR_ERRREQUEST)
    else:
        return make_rest_response('you should send right type!',
                                  code=Response.ERR_ERRREQUEST)

    return make_rest_response(Stat.get_bandwidth_by_port_report(port, starttime, endtime, type))