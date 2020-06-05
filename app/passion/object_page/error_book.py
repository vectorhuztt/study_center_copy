#！/usr/bin/python3
# -*-conding:utf-8 -*-
# @Author: fengyanan
# @file: error_book.py
# @time: 2019/4/10 14:56
import re
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class ErrorBook(BasePage):

    @teststep
    def wait_check_wrong_note_page(self):
        """错题本页面检查点"""
        locator = (By.XPATH, "//*[text()='错题练习']")
        return self.get_wait_check_page_result(locator)

