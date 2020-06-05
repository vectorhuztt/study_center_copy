# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/29 8:57
# -------------------------------------------
import logging


class Log:
    @classmethod
    def set_logger(cls, device_name, file):
        logger = logging.getLogger('selenium')
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(file)
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s' + ' - %s' % device_name +
                                      ' - %(levelname)s' + ' - %(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        cls.logger = logger

    def d(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def i(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def c(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def e(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
