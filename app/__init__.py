# -*- coding:utf8 -*-
'''
The flask app, include models, templates, static file and route mapper.
'''
__all__ = []
__version__ = '0.0.1'
__author__ = 'GalaIO'

import os
import sys
from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from config import config, root_dir


# 定义了数据库实例，在随后初始化，传入app上下文
db = SQLAlchemy()

# 一个动态添加蓝图的修饰器，为了简化操作，减少开发者错误的
# 利用了python修饰器的特性和动态类型的特性，返回同命名的蓝图
def addBlueprint(url_prefix=None):
    def decorator(f):
        blueprint = f()
        # 使用异常来报错，检查数据类型
        if not isinstance(blueprint, Blueprint):
            raise Exception('the warped must return a Blueprint object!!!')
        blueprint.url_prefix = url_prefix
        return blueprint
    return decorator

# 一个更灵活的，更简单的生成蓝图的函数
def BlueprintFactory(importname, url_prefix=None, isRootPath=False):
    try:
        name = importname.split('.').pop()
    except IndexError, e:
        raise Exception('please input a correct path, like main or app.main!!')
    if isRootPath:
        url_prefix = None
        print 'build a root path!'
    else:
        url_prefix = '/' + name
        print 'build a '+url_prefix+' path!'
    return Blueprint(name=name, import_name=importname, url_prefix=url_prefix)

# 延迟创建app， 为了让视图和模型与创建分开
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 初始化一些flask扩展库，依赖于flask的app上下文环境
    db.init_app(app)
    # 附加路由和自定义的错误页面
    app_dir = os.path.join(root_dir, 'app')
    # 逐个执行各个路由映射脚本，添加到route_list中
    for routes in os.listdir(app_dir):
        rou_path = os.path.join(app_dir, routes)
        # 只加载包，不是模块
        if not os.path.isfile(rou_path):
            try:
                __import__('app.' + routes)
            except ImportError, e:
                print routes + 'is not a module!'
                continue
            module = sys.modules['app.' + routes]
            # 循环获取是否是需要的类型，然后动态调用
            for obj_name in module.__dict__:
                obj = getattr(module, obj_name)
                if isinstance(obj, Blueprint):
                    if obj.url_prefix is None:
                        app.register_blueprint(obj)
                    else:
                        app.register_blueprint(obj, url_prefix=obj.url_prefix)
                    break
    #返回app实例，让外部模块继续使用
    return app