# coding: utf-8

"""
    用例数据管理
"""
import os
import logging


# 浏览器:FireFox，Chrome，IE
browser = 'FireFox'

# 家路径
SJ_HOME = os.path.dirname(os.path.dirname(__file__))
SJ_LIB = os.path.join(SJ_HOME, 'libs')
SJ_RESULT = os.path.join(SJ_HOME, 'result')
SJ_DOCS = os.path.join(SJ_HOME, 'docs')
SJ_DB = os.path.join(SJ_DOCS, 'plms_data') + os.sep + 'plms.db'
SJ_SCRIPTS = os.path.join(SJ_HOME, 'scripts')

# 登陆数据
url = ''   # 登录的url
main_page = ''  # 主页地址
username = '' # 用户名
password = ''   # 密码

# 日志开关
is_log = True   # 是否打开日志
is_print = True # 日志是否输出到控制台
file_log_level = logging.INFO       # 文件中日志级别
stream_log_level = logging.INFO     # 控制台中日志级别

# 测试报告
IS_REPORT = True    # 是否输出测试报告
REPORT_DESC = "web自动化测试"    # 测试报告描述

# 邮件
IS_EMAIL = False    # 是否发送邮件
PASS_RATE = 0.5   # 限制成功率达到多少之后才发送邮件，0则不做限制， 取值[0, 1]
MAIL_HOST = 'smtp.exmail.qq.com'     # 设置邮箱服务器
MAIL_USER = ''  # 用户名
MAIL_PASSWORD = ''             # 密码
SENDER = ''   # 发件人
RECEIVERS= ['', '']     # 收件人
CC = ['']                   # 抄送人

