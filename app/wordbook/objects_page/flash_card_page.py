#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/28 16:24
# -----------------------------------------
import datetime
import time
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep, teststeps


class FlashWordPage(WordBookPublicElePage):

    def __init__(self):
        super().__init__()
        self.home = WordHomePage()

    @teststep
    def wait_check_flash_card_page(self):
        locator = (By.CSS_SELECTOR, '.sk-container')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_word_explain_page(self):
        """单词解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.main .explain')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_sentence_explain_page(self):
        """句子解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.example .example-explain')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_speak_page(self):
        """句子解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.icon-components-mic:not([style="display: none;"])')
        return self.wait.wait_check_element(locator, timeout=3)

    @teststep
    def wait_check_commit_btn_page(self):
        """句子解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.icon-components-arrow.circle')
        return self.wait.wait_check_element(locator)


    @teststep
    def wait_check_mine_sound_page(self):
        """句子解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.icon-components-triangle')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_copy_page(self):
        """闪卡抄写模式页面检查点"""
        locator = (By.CSS_SELECTOR, '.main .input')
        return self.wait.wait_check_element(locator)

    @teststep
    def hide_show_explain(self):
        """显示隐藏解释按钮"""
        locator = (By.CSS_SELECTOR, ".el-dialog__body .sk-container .switch")
        self.wait.wait_find_element(locator).click()

    @teststep
    def normal_flash_word(self):
        """正常闪卡游戏的单词"""
        locator = (By.CSS_SELECTOR, '.main .word')
        return self.wait.wait_find_element(locator).text

    @teststep
    def click_word_voice(self):
        """点击单词发音按钮"""
        locator = (By.CSS_SELECTOR, ".main .speaker")
        self.wait.wait_find_element(locator).click()

    @teststep
    def sentence(self):
        """句子"""
        locator = (By.CSS_SELECTOR, '.example .sentence')
        return self.wait.wait_find_element(locator).text

    @teststep
    def sentence_explain(self):
        """句子解释"""
        locator = (By.CSS_SELECTOR, '.example .sentence')
        return self.wait.wait_find_element(locator).text

    @teststep
    def mine_mic(self):
        locator = (By.CSS_SELECTOR, '.icon-components-mic')
        return self.wait.wait_find_element(locator)


    @teststep
    def stop_speak(self):
        locator = (By.CSS_SELECTOR, '.icon-components-rect')
        self.wait.wait_find_element(locator).click()

    @teststep
    def copy_word(self):
        """抄写单词"""
        locator = (By.CSS_SELECTOR, '.main .text .word')
        return self.wait.wait_find_element(locator).text

    @teststep
    def copy_input_wrap(self):
        """抄写输入栏"""
        locator = (By.CSS_SELECTOR, '.main .input input')
        return self.wait.wait_find_element(locator)


    @teststeps
    def normal_flash_card_operate(self, stu_id, book_id, *, word_info, is_enhanced=True):
        """正常闪卡游戏过程"""
        print('======= 正常闪卡游戏 ======= \n')
        word_list = []
        begin_time = round(time.time())
        while self.wait_check_sentence_explain_page():
            _, _, word_id = self.game_container()
            word = self.normal_flash_word()
            word_type = '短语' if ' ' in word else '单词'
            if word in word_list:
                self.base_assert.except_error('单词已存在， 单词未去重')
            word_list.append(word)
            explain = self.word_explain()
            sentence = self.sentence()
            sentence_explain = self.sentence_explain()
            print('单词：' + word,
                  '解释：' + explain,
                  '句子：' + sentence,
                  '句子解释：' + sentence_explain,
                  sep='\n')
            word_info[word_id] = (word, explain, word_type)
            if is_enhanced:
                db_all_explain = WordBookSqlHandle().get_student_explain_list_by_word_id(stu_id, book_id, word_id)
                print('查询到的单词解释：', db_all_explain)
                print('解释分割：', explain.split('；'))
                if db_all_explain != explain.split('；'):
                    self.base_assert.except_error('题目解释不是已学解释合并')
            self.commit_btn().click()
            print('-'*30, '\n')
            time.sleep(1)
        spend_seconds = round(time.time()) - begin_time
        return spend_seconds

    @teststeps
    def speak_flash_card_operate(self, word_info):
        print('======= 闪卡录音游戏 ======= \n')
        index = 0
        begin_time = round(time.time())
        while self.wait_check_speak_page():
            word = self.normal_flash_word()
            word_type = "短语" if ' ' in word else '单词'
            explain = self.word_explain()
            _, _, explain_id = self.game_container()
            sentence = self.sentence()
            sentence_explain = self.sentence_explain()
            word_info[explain_id] = (word, explain, word_type)
            print('单词：' + word,
                  '解释：' + explain,
                  '解释id：' + explain_id,
                  '句子：' + sentence,
                  '句子解释：' + sentence_explain,
                  sep='\n')
            # if index == 0 and not do_right:
            #     time.sleep(11)
            #     if self.game_container()[-1] == explain_id:
            #         self.base_assert.except_error('限制时间过后， 单词未发生变化')
            # else:
            self.mine_mic().click()
            time.sleep(2)
            self.stop_speak()
            while not self.wait_check_commit_btn_page():
                time.sleep(2)
            self.commit_btn().click()
            index += 1
            print('-'*30, '\n')
            time.sleep(1)
        spend_seconds = round(time.time()) - begin_time
        return spend_seconds

    @teststep
    def flash_copy_operate(self, word_id):
        """抄写模式处理"""
        if self.wait_check_copy_page():
            print('抄写id：', self.game_container()[-1])
            print('默写id：', word_id)
            if self.game_container()[-1] != word_id:
                self.base_assert.except_error('单词抄写的页面单词与错误单词不一致')

            self.commit_btn_judge()
            copy_word = self.copy_word()
            copy_explain = self.word_explain()
            print('闪卡抄写单词：', copy_word)
            print('闪卡抄写解释：', copy_explain, '\n')
            self.copy_input_wrap().send_keys(copy_word)
            self.commit_btn_judge(status=True)
            self.commit_btn().click()
            time.sleep(2)
        else:
            self.base_assert.except_error('该单词累计默写错误4次，未出现闪卡抄写页面 {}'.format(word_id))






