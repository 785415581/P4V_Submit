#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/12 17:30
"""
import os
import getpass
import logging
import logging.handlers


class ToolsLogger(object):
    LOG_FILE_SIZE = 1000000
    LOG_FILE_NUM = 10

    @classmethod
    def get_log_dir(cls, log_name):
        return "%s/%s" % ("R:/ProjectX/Scripts/log", log_name)

    @classmethod
    def get_logger(cls, log_name, save_log=False, debug=None, log_location=None):
        """
        :params:
            log_name: str
                log file name
            save_log: bool
                save log in a file or not
            debug: bool
                turn on debug mode or not
            log_location: str
                where to store the file, a directory

        """
        logger = logging.getLogger(log_name)
        if not len(logger.handlers):
            if save_log:

                log_dir = log_location
                if not log_location:
                    log_dir = cls.get_log_dir(log_name)
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                log_file = "%s/%s.log" % (log_dir, log_name)
                hdlr = logging.handlers.RotatingFileHandler(log_file, "a", ToolsLogger.LOG_FILE_SIZE,
                                                            ToolsLogger.LOG_FILE_NUM)
                # https://www.cnblogs.com/chenyibai/p/10676574.html
                fmt = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
            else:
                hdlr = logging.StreamHandler()
                fmt = logging.Formatter('%(name)s - %(message)s')

            hdlr.setFormatter(fmt)
            logger.addHandler(hdlr)
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        logging.raiseExceptions = 0
        return logger


if __name__ == "__main__":
    log_name = getpass.getuser()
    logger = ToolsLogger.get_logger(log_name, save_log=True)

    logger.info("publish test...")
    logger.warning('saaaaaaaaaaaaaaaaaa')