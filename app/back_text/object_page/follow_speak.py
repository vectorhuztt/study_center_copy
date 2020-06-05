#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/21 15:46
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps
from utils.get_attr import GetAttribute


class FollowSpeaking(GameCommonElePage):
    # ===================== 口语跟读  ==========================
    @teststep
    def wait_check_follow_speak_page(self):
        """口语跟读页面检查点"""
        locator = (By.CSS_SELECTOR, 'ky-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_explain_page(self):
        """解释页面检查点"""
        locator = (By.CLASS_NAME, 'explain')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_seconds_page(self):
        """录音时间页面检查点"""
        locator = (By.CLASS_NAME, 'seconds')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_mine_sound_page(self):
        """我的录音"""
        locator = (By.CSS_SELECTOR, '.icon-components-triangle')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_speaking_next_btn(self):
        """口语跟读下一步按钮"""
        locator = (By.CSS_SELECTOR, '.icon-components-arrow')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_next_bank_tip_page(self):
        """下一题提示页面检查点"""
        locator = (By.XPATH, '//*[contains(text(),"进入下一题吧")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def speaking_sentence(self):
        """口语英文句子"""
        ele = self.driver.find_element_by_class_name('text')
        return ele.text

    @teststep
    def show_explain_btn(self):
        """展开解释"""
        ele = self.driver.find_element_by_css_selector(".question-wrap  .operation")
        return ele

    @teststep
    def speaking_sentence_explain(self):
        """口语跟读的解释"""
        ele = self.driver.find_element_by_class_name('explain')
        return ele.text

    @teststep
    def speaking_voice_play_icon(self):
        """系统发音按钮"""
        ele = self.driver.find_element_by_css_selector('.speaker')
        return ele

    @teststep
    def speaking_score(self):
        """口语评分"""
        ele = self.driver.find_element_by_class_name('inactive')
        return ele.get_attribute('title')

    @teststep
    def is_speaking_btn(self):
        """正在录音按钮"""
        ele = self.driver.find_element_by_css_selector('.pulse')
        return ele

    @teststep
    def speaking_mic_icon(self):
        """口语跟读下方图标"""
        ele = self.driver.find_element_by_css_selector('.icon-components-mic')
        return ele

    @teststep
    def pause_speaking_icon_btn(self):
        """暂停说话按钮"""
        ele = self.driver.find_element_by_css_selector('.icon-components-rect')
        return ele

    @teststep
    def small_image(self):
        """小图片"""
        ele = self.driver.find_element_by_css_selector('.float-wrap img')
        return ele


    @teststep
    def speaking_operate(self):
        """录音操作"""
        self.speaking_mic_icon().click()
        time.sleep(4)
        self.pause_speaking_icon_btn().click()
        if self.wait_check_error_tip_page():
            print(self.error_content())
        time.sleep(5)
        if self.wait_check_speaking_next_btn():
            if not self.wait_check_mine_sound_page():
                print('★★★ 录音结束， 未发现我的录音按钮')
        else:
            self.speaking_operate()

    @teststeps
    def speaking_game_process(self):
        """口语跟读游戏过程"""
        print('======== 口语跟读 ========\n')
        start_time = round(time.time())
        index = 0
        while self.wait_check_container_page():
            if self.commit_btn().is_displayed():
                print('★★★  口语跟读游戏的下一步按钮默认出现')
            self.check_image_zoom_size(self.small_image)
            sentence = self.speaking_sentence()
            print('口语句子：', sentence)

            self.show_explain_btn().click()
            time.sleep(1)
            if not self.wait_check_explain_page():
                print('★★★ 点击展开解释按钮，未发现解释文本')
            count = 0
            if index == 0:
                self.speaking_mic_icon().click()
                time.sleep(22)
                if not self.wait_check_error_tip_page():
                    self.base_assert.except_error('录音时间超过20s， 未提示录音超时')
                else:
                    print(self.error_content())
                if self.is_speaking_btn().is_displayed():
                    self.base_assert.except_error('★★★ 录音时长超过20秒，但是未停止录音')
                if self.commit_btn().is_displayed():
                    count += 1

                while count < 5:
                    self.speaking_operate()
                    if self.commit_btn().is_displayed():
                        count += 1

                time.sleep(3)
                if not self.wait_check_next_bank_tip_page():
                    print('★★★ 录音超过5次， 未出现进入下一题提示')

                if 'disabled' not in GetAttribute().get_class(self.speaking_mic_icon()):
                    print('★★★ 录音超过5次， 开始说话按钮未置灰')

            else:
                self.speaking_operate()

            time.sleep(3)
            print(self.speaking_score())
            self.commit_btn().click()
            time.sleep(2)
            index += 1
            print('-'*30, '\n')
        used_time = round(time.time()) - start_time
        return used_time


