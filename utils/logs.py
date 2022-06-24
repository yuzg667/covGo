"""
封装log方法
"""

import os
import time
import logging.handlers

# 日志打印等级
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# 创建一个日志
logger = logging.getLogger()
level = 'default'


# 创建日志文件方法
def create_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass


# 给logger添加handler 添加内容到日志句柄中
def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)


# 在记录日志之后移除句柄
def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)


def get_current_time():
    from datetime import datetime
    return(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))


class MyLog:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = path + '../covGoLog/log.log'
    err_file = path + '../covGoLog/err.log'
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S.f'

    # 创建一个handler，用于写入日志文件date
    handler = logging.FileHandler(log_file, encoding='utf-8')
    err_handler = logging.FileHandler(err_file, encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        # 文件中输出模式
        logger.debug( log_meg)
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        # logger.info(log_meg)
        logger.info("[info] %s %s" % (get_current_time(), log_meg))
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        # logger.warning(log_meg)
        logger.warning("[warning] %s %s" % (get_current_time(), log_meg))
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        # logger.error(log_meg)
        logger.error("[error] %s %s" %(get_current_time(),log_meg))
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        # logger.error(log_meg)
        logger.error("[critical] %s %s" % (get_current_time(), log_meg))
        remove_handler('critical')

    # 设置控制台输出格式
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'
        # '[%(levelname)s] %(message)s', '%s,%03d'
    )
    # 再创建一个handler，用于输出到控制台
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    console.setLevel(logging.NOTSET)


if __name__ == "__main__":
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error")
    MyLog.critical("This is critical message")