# coding: utf-8
"""
    记录日志
"""

"""
    sLog 记录器，暴露了应用程序代码能直接使用的接口。
    Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地。
    Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录。
    Formatter 格式化器，指明了最终输出中日志记录的布局。
"""

import sys
import logging
from datetime import datetime
from lib.data import *
import shutil

__date__ = "2017-08-14"
__author__  = 'yangshifu'

class sLog():
    def __init__(self):
        log_dir = os.path.join(SJ_RESULT, 'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_path = os.path.join(log_dir, 'log.txt')
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def get_logger(self):
        """
        创建根容器，放入文件hangler，定义日志formatter
        :is_print: 是否打印在控制台
        :return: 已装载好的logger对象
        """
        # 创建根容器
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # 创建Handler容器，以及handler的日志级别
        file_handle = logging.FileHandler(self.log_path)
        stream_handler = logging.StreamHandler(sys.stdout)
        file_handle.setLevel(file_log_level)
        stream_handler.setLevel(stream_log_level)
        # 定义Formatter,即记录日志的格式
        formatter = logging.Formatter(fmt= '%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        # 设置handler的日志格式为formatter, 将handler放入根容器中
        file_handle.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        if not logger.handlers:
            logger.addHandler(file_handle)
            if is_print:
                logger.addHandler(stream_handler)
        return logger

logger = sLog().get_logger()

def log_write(msg, level='info'):
    """
    写日志
    :param msg: 日志内容。如：get_current_info() + 'Start browser with %s ...' % browser
    :param level: 日志级别，默认INFO
    :return:
    """
    if level.lower() == 'info':
        logger.info(msg)
    elif level.lower() == 'debug':
        logger.debug(msg)
    elif level.lower() == 'warn' or level.lower() == 'warning':
        logger.warn(msg)
    elif level.lower() == 'error':
        logger.error(msg)
    elif level.lower() == 'critical':
        logger.critical(msg)
    else:
        pass

def get_current_info():
    """日志打印文件名、函数名、行号"""
    file_name = os.path.basename(sys._getframe().f_back.f_code.co_filename) + ' '
    func_name = sys._getframe().f_back.f_code.co_name + ' '
    line_no = '[line:' + str(sys._getframe().f_back.f_lineno) + '] '
    return file_name + func_name + line_no

if __name__ == '__main__':
    log_write(get_current_info()+ 'abcdefgs1', 'ERROR')
    log_write(get_current_info()+ 'abcdefgs2', 'info')
    log_write(get_current_info()+ 'abcdefgs3', 'debug')
