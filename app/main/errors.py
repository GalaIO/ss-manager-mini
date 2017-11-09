# -*- coding:utf8 -*-
'''
web error control..
'''
from flask import render_template
from . import main

# 向程序全局注册404 错误处理，其他路由处理可以省掉，页面未找到
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 向程序全局注册500 错误处理，其他路由处理可以省掉，服务器内部错误
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 向程序全局注册403 错误处理，其他路由处理可以省掉，禁止访问
@main.app_errorhandler(403)
def internal_server_error(e):
    return render_template('403.html'), 403