# coding: utf-8
import sys
import unittest
import time
import functools
import HTMLTestRunner
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart
from lib.data import *
from lib.func import *
from lib.log import *
from selenium import webdriver


""" 
    1.生成测试报告(带截图)
    2.发送邮件
"""


# 生成测试报告
def run_suite(suite_class, prefix='test_'):
    """
    testcase加入TestSuite，生成测试报告
    :param suite_class: 测试套TestSuite(类)
    :param prefix: 用例前缀，即类中方法的前缀，默认'test_'，即将test_开头的方法（用例）加入测试套
    :return:
    """
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    test_suite = unittest.TestSuite()
    HtmlFile = os.path.join(SJ_RESULT, '%s.html' % now)
    for test in dir(suite_class):
        if test.startswith(prefix) and hasattr(getattr(suite_class, test), '__call__'):
            test_suite.addTest(suite_class(test))
    with open(HtmlFile, "wb") as fp:
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"三江智慧云PLMS", description=u"""用例测试结果""", verbosity=2, browser= browser)
        runner.run(test_suite)

# 获取截图的装饰器，保存为图片，链接到html
def screenshot(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except AssertionError as msg:
            path = os.path.join(SJ_RESULT, 'screenshot')
            timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            if not os.path.isdir(path):
                os.makedirs(path)
            # 文件路径
            file_name = os.path.join(path, '%s.png'%timestamp)
            self.plms.driver.get_screenshot_as_png()
            self.plms.driver.save_screenshot(file_name)
            print('screenshot: ' + timestamp + '.png')
            traceback.print_exc()
            raise AssertionError(msg)
        except:
            path = os.path.join(SJ_RESULT, 'screenshot')
            timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            if not os.path.isdir(path):
                os.makedirs(path)
            # 文件路径
            file_name = os.path.join(path, '%s.png' % timestamp)
            self.plms.driver.get_screenshot_as_png()
            self.plms.driver.save_screenshot(file_name)
            print('screenshot: ' + timestamp + '.png')
            traceback.print_exc()
            raise Exception
    return wrapper

# 发送邮件(使用非SSL协议发送，端口25号，如163邮箱发送)
def send_mail_not_SSL(subject, content, attach=''):
    """
    发送邮件，不含附件
    :param subject: 主题
    :param content: 内容
    :param attach:  附件地址，为空则不传附件
    :return:
    """
    # 构造MIMEMultipart对象做为根容器
    msg = MIMEMultipart()
    msg['From'] = Header(u'<%s>' % SENDER, 'utf-8')
    msg['To'] = Header(';'.join(RECEIVERS), 'utf-8')
    if 'CC' in globals().keys():
        msg['Cc'] = Header(';'.join(CC), 'utf-8')
    else:
        CC = []
    msg['Subject'] = Header(subject, 'utf-8')

    # 设定纯文本信息
    text_msg = MIMEText(content, 'plain', 'utf-8')
    msg.attach(text_msg)

    # 如果传入附件，则构造附件，读入测试报告文件并格式化
    if attach:
        # file_result = open(attach, 'rb').read()
        # att1 = MIMEText(file_result, 'base64', 'gb2312')
        with open(attach, 'r') as fp:
            file_result = fp.read()
        att1 = MIMEText(file_result, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"'% attach
        msg.attach(att1)

    # 发送邮件
    smtp = smtplib.SMTP()
    try:
        smtp.connect(MAIL_HOST, 25)     # 25为SMTP端口号,465或者994为SSL协议端口
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(SENDER, RECEIVERS, msg.as_string())
        print(u"发送邮件成功")
    except smtplib.SMTPException as e:
        print(u"Error, 发送邮件失败")
        traceback.print_exc()
    finally:
        smtp.quit()

# 发送邮件(使用SSL协议发送，腾讯企业邮箱)
def send_mail(subject, plain_contant=None, attach=''):
    """
    发送邮件，可含附件  -- 修改于2018年2月9日 yangshifu，
    :param subject: 主题
    :param plain_contan: 纯文本内容
    :param attach:  附件地址，为空则不传附件
    :return:
    """
    # 构造MIMEMultipart对象做为根容器
    msg = MIMEMultipart()
    msg['From'] = Header(u'<%s>' % SENDER, 'utf-8')
    msg['To'] = Header(';'.join(RECEIVERS), 'utf-8')
    if 'CC' in globals().keys():
        global CC
        msg['Cc'] = Header(';'.join(CC), 'utf-8')
    else:
        CC = []
    msg['Subject'] = Header(subject, 'utf-8')

    # 添加纯文本信息
    if plain_contant:
        text_msg = MIMEText(plain_contant, 'plain', 'utf-8')
        msg.attach(text_msg)

    # 如果传入附件，则构造附件，读入测试报告文件并格式化
    if attach:
        with open(attach, 'r', encoding='utf-8') as fp:
            file_result = fp.read()
        att1 = MIMEText(file_result, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', os.path.basename(attach)))
        # att1["Content-Disposition"] = 'attachment; filename="%s"'% attach
        msg.attach(att1)

    # 发送邮件
    try:
        smtp = smtplib.SMTP_SSL(MAIL_HOST, port=465)   # 25为SMTP端口号,465或者994为SSL协议端口
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(SENDER, RECEIVERS + CC, msg.as_string())
        print("发送邮件成功")
    except smtplib.SMTPException:
        print("Error, 发送邮件失败")
        traceback.print_exc()
    finally:
        smtp.quit()

if __name__ == "__main__":
    subject = u'【请阅】三江智慧云PLMS平台测试报告'
    content = u'测试范围：消防设备-无线报警主机\n' \
              u'Notes：测试报告预览和打开模式可能会出现乱码，且页面效果元素效果无法显示，请下载后打开'
    file_html = scan_dir(SJ_RESULT, 'html')
    send_mail(subject, content, attach=file_html)
