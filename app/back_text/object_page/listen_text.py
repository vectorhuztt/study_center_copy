#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/21 15:42
# -----------------------------------------
import time

import allure
from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps
from utils.get_attr import GetAttribute


class ListenText(GameCommonElePage):

    @teststep
    def wait_check_explain_text_page(self):
        """听力解释页面检查点"""
        locator = (By.CLASS_NAME, 'explain')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_voice_play_page(self):
        """播放按钮页面检查点"""
        locator = (By.CLASS_NAME, 'control')
        return self.get_wait_check_page_result(locator)

    @teststep
    def listening_picture(self):
        """磨耳朵图片"""
        ele = self.driver.find_element_by_class_name('picture')
        return ele

    @teststep
    def listen_voice_play_btn(self):
        """开始播放按钮"""
        ele = self.driver.find_element_by_class_name('control')
        return ele

    @teststep
    def listen_sentence(self):
        """句子"""
        ele = self.driver.find_elements_by_css_selector('.alltext .text')
        return ele

    @teststep
    def listen_explain(self):
        """听力解释文本"""
        ele = self.driver.find_elements_by_css_selector('.alltext .explain')
        return ele

    @teststep
    def explain_show_hide_btn(self):
        """解释隐藏显示按钮"""
        ele = self.driver.find_element_by_css_selector('.switch')
        return ele

    @teststeps
    def listening_text_game_process(self):
        """磨耳朵游戏过程"""
        print('======== 磨耳朵 ========\n')
        start_time = round(time.time())
        while self.wait_check_container_page():
            self.check_image_zoom_size(self.listening_picture)

            if 'open' in self.explain_show_hide_btn().get_attribute('class'):
                self.base_assert.except_error('解释按钮默认状态为显示')
            self.explain_show_hide_btn().click()

            if not self.wait_check_explain_text_page():
                self.base_assert.except_error('点击解释按钮，句子解释未出现')

            for i, x in enumerate(self.listen_sentence()):
                print("句子:" + x.text)
                print('解释：' + self.listen_explain()[i].text, '\n')

            self.explain_show_hide_btn().click()
            if self.wait_check_explain_text_page():
                self.base_assert.except_error('点击解释按钮，句子解释未隐藏')

            self.listen_voice_play_btn().click()
            time.sleep(2)

            self.listening_picture().click()
            if not self.wait_check_voice_play_page():
                self.base_assert.except_error('点击播放按钮后,再次点击图片， 音频未暂停')

            self.listen_voice_play_btn().click()
            time.sleep(2)

            while True:
                if 'disabled' not in GetAttribute().get_class(self.commit_btn()):
                    self.commit_btn().click()
                    time.sleep(2)
                    break
                else:
                    time.sleep(2)
        used_time = round(time.time()) - start_time
        return used_time
