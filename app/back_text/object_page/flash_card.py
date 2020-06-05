#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/9 16:50
# -----------------------------------------
import random
import string
import time
from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class FlashCard(GameCommonElePage):

    @teststep
    def word(self):
        """单词"""
        ele = self.driver.find_element_by_css_selector('.word')
        return ele.text

    @teststep
    def word_explain(self):
        """单词解释"""
        ele = self.driver.find_element_by_css_selector('.explain')
        return ele.text

    @teststep
    def input_text_wrap(self):
        """抄写输入栏"""
        ele = self.driver.find_element_by_css_selector('.input input')
        return ele

    @teststeps
    def flash_normal_operate(self):
        print('======== 闪卡游戏 ========\n')
        start_time = round(time.time())
        while self.wait_check_container_page():
            print("单词：", self.word())
            print('解释：', self.word_explain())
            self.commit_btn().click()
            time.sleep(1)
            print('-'*30, '\n')
        return round(time.time()) - start_time

    @teststeps
    def flash_copy_operate(self):
        print('======== 闪卡抄写 ========\n')
        start_time = round(time.time())
        right_bank = []
        index = 0
        while self.wait_check_container_page():
            word = self.word()
            print("单词：", word)
            print('解释：', self.word_explain())
            self.commit_btn_judge()
            bank_id = self.bank_id()
            if bank_id in right_bank:
                print('本题已做对，却再次出现')
            if index == 0:
                random_str = ''.join(random.sample(string.ascii_lowercase, 3))
                self.input_text_wrap().send_keys(random_str)
                if 'disable' not in self.commit_btn().get_attribute('class'):
                    print('抄写单词不正确， 但是下一步按钮可点击')

                self.input_text_wrap().clear()
            self.input_text_wrap().send_keys(word)
            if 'disable' in self.commit_btn().get_attribute('class'):
                print('抄写单词正确， 但是下一步按钮不可点击')

            self.commit_btn().click()
            index += 1
            time.sleep(1)
            print('-'*30, '\n')
        used_time = round(time.time()) - start_time
        return used_time

