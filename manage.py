# -*- coding:utf8 -*-
'''
Apply command for user to control flask.
'''
from config import Config, root_dir
import os
from app import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import logging

# 动态创建app实例，然后继续使用
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 创建命令行管理
manager = Manager(app, with_default_commands=True)
# 创建数据库迁移管理
migrate = Migrate(app, db)

# 吧数据模型导入python解释器用于测试
def make_shell_context():
    reflec_maps = {}
    from app import models
    for obj_name in models.__dict__:
        obj = getattr(models, obj_name)
        if hasattr(obj, '__bases__') and len(obj.__bases__) > 0 and obj.__bases__[0] is db.Model:
            reflec_maps[obj_name] = obj
    reflec_maps['app'] = app
    reflec_maps['db'] = db
    return reflec_maps
manager.add_command("shell", Shell(make_context=make_shell_context))

# 添加数据迁移命令
manager.add_command('db', MigrateCommand)

# 添加测试命令
@manager.command
def test():
    '''Run the unit tests.'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def update():
    # 自动更新需求库
    print 'output requirements file.....'
    os.system('pip freeze > requirements.txt')

# 添加自动生成生产环境配置命令
@manager.command
def config():
    '''根据配置自动生成 生产环境配置，只支持nginx uwsgi'''
    if not os.path.exists('logs'):
        os.mkdir('logs')
    if not os.path.exists('pids'):
        os.mkdir('pids')
    # 利用bash命令删除所有的xml 和 conf文件，这些就是nginx和uwsgi的配置文件
    os.system('rm *-nginx.conf')
    os.system('rm *-uwsgi.xml')
    # 执行数据迁移和更新
    os.system('python manage.py db migrate')
    os.system('python manage.py db upgrade')

    nginx_conf =\
'''server {
    listen 80;
    server_name %s;
    access_log  %s;
    error_log  %s;
    location / {
        include uwsgi_params;
        uwsgi_pass localhost:%d;
    }
    location /static/ {
        root %s;
    }
}''' % (Config.HOST, os.path.join(os.path.join(root_dir, 'logs'), 'nginx.log'), os.path.join(os.path.join(root_dir, 'logs'), 'nginx.err'), Config.PORT, os.path.join(root_dir, 'app'))

    '''
    如果需要在uwsgi中使用多线程必须，添加下面两个字段，
    一个是threads 一个是enable-threads否则不能运行，为了提高性能肯定是越多进程越多线程的好。
    '''
    uwsgi_conf =\
'''<uwsgi>
    <pythonpath>%s</pythonpath>
    <module>manage</module>
    <callable>app</callable>
    <socket>%s:%d</socket>
    <master/>
    <processes>%d</processes>
    <threads>%d</threads>
    <enable-threads/>
    <memory-report/>
    <daemonize>logs/uwsgi.log</daemonize>
    <buffer-size>16384</buffer-size>
    <pidfile>pids/uwsgi.pid</pidfile>
</uwsgi>'''% (root_dir, Config.ACCESSIPS, Config.PORT, 4, 4)
    print 'output nginx config file.....'
    file = open(Config.HOST+'-nginx.conf', 'w')
    file.truncate()
    file.write(nginx_conf)
    file.close()

    print 'output uwsgi config file.....'
    file = open(Config.HOST+'-uwsgi.xml', 'w')
    file.truncate()
    file.write(uwsgi_conf)
    file.close()

from app.models import Port
def data_related_initial():
    '''
    从port表查出所有可用的用户，并重新开启端口
    :return:
    '''
    logging.info("重新使能有效端口.....")
    Port.reenable_port_all()

from deamon.threads import StatThread, CliThread
# 添加默认执行启动服务器的命令
@manager.command
def default_server():
    print 'start at %s:%s' % (Config.ACCESSIPS, Config.PORT)
    logging.info("数据初始化.....")
    data_related_initial()
    app.run(debug=True, host=Config.ACCESSIPS, port=Config.PORT, use_reloader=False)

# 启动主进程
if __name__ == '__main__':
    # 启动后台监控进程
    # thread = StatThread(app)
    thread = CliThread(app)
    thread.start()
    # 执行数据初始化工作
    manager.run(default_command=default_server.__name__)