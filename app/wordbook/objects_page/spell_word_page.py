#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/28 17:11
# -----------------------------------------
import random
import string
import time
import numpy as np

from pynput.keyboard import Controller, Key
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.wordbook.objects_page.flash_card_page import FlashWordPage
from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep, teststeps


class SpellWordPage(WordBookPublicElePage):

    flash_copy = FlashWordPage()

    @teststep
    def wait_check_spell_page(self):
        """单词拼写页面检查点"""
        locator = (By.CSS_SELECTOR, '.main .text-input')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_listen_spell_page(self):
        """单词听写页面检查点"""
        locator = (By.CSS_SELECTOR, '.dctx-container')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_answer_page(self):
        """单词答案页面检查点"""
        locator = (By.CSS_SELECTOR, '.main .answer')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_word_explain_page(self):
        """单词解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.main .explain')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_random_spell_page(self):
        """随机拼写页面检查点"""
        locator = (By.CSS_SELECTOR, '.text .letter-input')
        return self.wait.wait_check_element(locator)

    @teststep
    def spell_box(self):
        locator = (By.CSS_SELECTOR, '.dcpx-container')
        return self.wait.wait_find_element(locator)

    @teststep
    def click_skip_btn(self):
        """点击跳过按钮"""
        locator = (By.CSS_SELECTOR, '.component-wrap .menu')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def input_wrap(self):
        """单词拼写输入栏"""
        locator = (By.CSS_SELECTOR, '.main .text-input')
        return self.wait.wait_find_element(locator)

    @teststep
    def listen_spell_right_answer(self):
        """单词听写正确答案"""
        locator = (By.CSS_SELECTOR, '.main .text .word')
        return self.wait.wait_find_element(locator).text

    @teststep
    def random_show_words(self):
        """展示的单词"""
        locator = (By.CSS_SELECTOR, ".text-wrapper .text")
        ele = self.wait.wait_find_elements(locator)
        words  = ["_" if not x.text else x.text for x in ele]
        return words

    @teststep
    def random_input_warp(self):
        """随机拼写输入栏"""
        ele = self.driver.find_elements_by_css_selector('.text-wrapper .letter-input')
        return ele

    @teststep
    def random_spell_process(self, do_right=False, right_answer=None):
        """随机拼写操作"""
        if not do_right:
            for x in self.random_input_warp():
                x.click()
                time.sleep(0.5)
                x.send_keys(random.choice(string.ascii_letters))
                time.sleep(0.5)
        else:
            for i, x in enumerate(self.random_input_warp()):
                x.click()
                time.sleep(0.5)
                x.send_keys(right_answer[i])
                time.sleep(0.5)

    @teststep
    def check_input_is_right(self):
        """查看输入答案是否是正确的"""
        input_warp = self.random_input_warp()
        if any([x for x in input_warp if 'error' in x.get_attribute('class')]):
            return False
        else:
            return True

    @teststep
    def back_spell_operate(self):
        input_warp = self.random_input_warp()
        for x in reversed(input_warp):
            ActionChains(self.driver).click(x).perform()
            x.send_keys(Keys.BACKSPACE)
            x.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)

    @teststep
    def spell_game_process(self, word_id,  wrong_count=None, do_right=False, right_answer=None):
        """单词拼写做题流程"""
        if do_right:
            self.input_wrap().send_keys(right_answer + Keys.ENTER)
            mine_answer = right_answer
            print('我输入的：', mine_answer, '\n')
            time.sleep(3)
        else:
            random_str = ''.join(random.sample(string.ascii_lowercase, 3))
            mine_answer = random_str
            print('我输入的：', mine_answer, '\n')
            self.input_wrap().send_keys(random_str + Keys.ENTER)
            self.commit_btn_judge(status=True)
            self.commit_btn().click()

            if wrong_count is not None:
                if wrong_count != 4:
                    if not self.wait_check_random_spell_page():
                        self.base_assert.except_error('单词做错， 未跳转到随机拼写页面')
                    else:
                        self.random_spell_after_spell_wrong_operate(word_id)
                else:
                    self.flash_copy.flash_copy_operate(word_id)

    @teststeps
    def spell_with_copy_operate(self, word_info, stu_id, do_right,  bank_index,
                                skip_index_info, wrong_index_info, is_recite=False, book_id=None):
        """带有闪卡抄写的单词拼写游戏
        :param book_id: 书籍id
        :param stu_id:  学生id
        :param is_recite: 是否是复习
        :param skip_index_info: 记录跳过单词的索引值
        :param wrong_index_info: 错题索引收录信息
        :param bank_index: 全部题的索引统计
        :param do_right:  是否做全对
        :param word_info:    闪卡记录的正确答案信息
        """
        print('======= 默听游戏 ======= \n')
        begin_time = round(time.time())
        finish_word = []
        index = 0
        while self.wait_check_spell_page():
            finish_count = len(finish_word)
            _, _, word_explain_id = self.game_container()
            print('题目索引：', bank_index[0])
            print('默写解释(单词)id：', word_explain_id)
            explain = self.word_explain()
            print('默写解释：', explain)
            answer_word = word_info[word_explain_id][0]
            print('默写记录答案：', answer_word)
            wrong_id = list(word_info.keys())[0]
            skip_id = list(word_info.keys())[1] if len(word_info) > 1 else -1

            if is_recite:
                db_all_explain = WordBookSqlHandle().get_student_explain_list_by_word_id(stu_id, book_id, word_explain_id)
                print('查询到的单词解释：', db_all_explain)
                print('解释分割：', explain.split('；'))
                if db_all_explain != explain.split('；'):
                    self.base_assert.except_error('题目解释不是已学解释合并')

            if word_explain_id in finish_word:
                self.base_assert.except_error('单词已完成， 但是再次出现 ' + word_explain_id)
            if not do_right:
                # if index == 0:
                #     time.sleep(30)
                #     wrong_index_info.append(bank_index[0])
                #     if self.game_container()[-1] == word_explain_id:
                #         self.base_assert.except_error('限制时间过后， 单词未发生变化')
                # else:=
                if word_explain_id == wrong_id:
                    wrong_index_info.append(bank_index[0])
                    self.spell_game_process(word_explain_id, len(wrong_index_info), right_answer=answer_word)
                    print('此单词错误次数：', len(wrong_index_info))
                    if len(wrong_index_info) == 4:
                        finish_word.append(word_explain_id)
                else:
                    if word_explain_id == skip_id:
                        self.click_skip_btn()
                        print('点击跳过')
                        skip_index_info.append(bank_index[0])
                        self.skip_word_operate(word_explain_id, len(skip_index_info))
                        print('此单词跳过次数：', len(skip_index_info))
                        if len(skip_index_info) == 4:
                            finish_word.append(word_explain_id)
                    else:
                        self.spell_game_process(word_explain_id, do_right=True, right_answer=answer_word)
                        finish_word.append(word_explain_id)
            else:
                self.spell_game_process(do_right=True, right_answer=answer_word)
                finish_word.append(word_explain_id)

            if len(finish_word) == finish_count:
                self.commit_btn().click()
                time.sleep(1)
            index += 1
            bank_index[0] += 1
            print('-'*30, '\n')
        spend_seconds = round(time.time()) - begin_time

        return spend_seconds

    @teststep
    def skip_word_operate(self, word_explain_id, skip_count):
        """跳过单词处理"""
        if skip_count != 4:
            if not self.wait_check_listen_spell_page():
                self.base_assert.except_error('点击跳转游戏后， 未进入单词听写页面')
            else:
                _, _, game_id = self.game_container()
                if game_id != word_explain_id:
                    self.base_assert.except_error('听写单词不为默写跳过单词！')
                self.commit_btn_judge()
                random_str = ''.join(random.sample(string.ascii_lowercase, 3))
                print('\n我的听写答案：', random_str)
                self.input_wrap().send_keys(random_str + Keys.ENTER)
                time.sleep(0.5)
                if not self.wait_check_word_explain_page():
                    self.base_assert.except_error('听写做错， 点击提交未发现单词解释')
                else:
                    print('听写解释：', self.word_explain())
                    print('听写正确答案：', self.listen_spell_right_answer())

                self.commit_btn_judge(status=True)
                self.commit_btn().click()
                print('~' * 20, '\n')
                if not self.wait_check_random_spell_page():
                    self.base_assert.except_error('听写单词后未进入该单词的随机拼写页面')
                else:
                    self.random_spell_after_spell_wrong_operate(word_explain_id)
        else:
            self.flash_copy.flash_copy_operate(word_explain_id)


    @teststep
    def random_spell_after_spell_wrong_operate(self, word_explain_id):
        """紧随单词拼写的随机拼写游戏操作"""
        _, _, game_id = self.game_container()
        if game_id != word_explain_id:
            self.base_assert.except_error('随机拼写单词不为拼写错误单词！')
        self.commit_btn_judge()
        print('随机拼写解释：', self.word_explain())
        self.random_spell_process()
        time.sleep(1)
        if 'disabled' in self.commit_btn().get_attribute('class'):
            for x in range(len(self.random_input_warp())):
                value = self.driver.execute_script('return document.getElementsByClassName("letter-input")[{}]._value'.format(x))
                if value:
                    continue
                else:
                    self.random_input_warp()[x].click()
                    time.sleep(0.5)
                    self.random_input_warp()[x].send_keys(random.choice(string.ascii_letters))

        self.commit_btn_judge(status=True)
        self.commit_btn().click()
        time.sleep(0.5)
        if self.wait_check_answer_page():
            print('随机拼写正确答案：', self.right_answer())
            self.commit_btn().click()
        print('~'*20, '\n')
        time.sleep(2)

    @teststep
    def error_note_spell_game_operate(self, stu_id, book_id, second_wrong_words, wrong_count=None, do_right=False):
        """本书易错词单词拼写游戏处理"""
        index = 0
        while self.wait_check_spell_page():
            _, _, word_id = self.game_container()
            print('默写单词id：', word_id)
            explain = self.word_explain()
            print('默写解释：', explain)
            right_word = WordBookSqlHandle().get_word_by_word_id(word_id)
            db_all_explain = WordBookSqlHandle().get_student_explain_list_by_word_id(stu_id, book_id, word_id)
            if explain.split('；') != db_all_explain:
                self.base_assert.except_error('题目解释不是已学解释合并')
            if index == 0:
                second_wrong_words[0] = word_id

            if not do_right:
                if word_id == second_wrong_words[0]:
                    self.spell_game_process(word_id)
                    wrong_count[1] += 1
                else:
                    self.spell_game_process(word_id, do_right=True, right_answer=right_word)
            else:
                self.spell_game_process(word_id, do_right=True, right_answer=right_word)

            if word_id == second_wrong_words[0]:
                self.commit_btn().click()
                time.sleep(1)
            index += 1
            if wrong_count[1] == 4:
                self.flash_copy.flash_copy_operate(second_wrong_words[0])
                wrong_count[1] = 0
            print('~' * 20, '\n')


    @teststep
    def random_spell_game_operate(self, word_info, do_right, bank_index, wrong_index_info):
        print('===== 单词拼写-随机拼写 ======\n')
        begin_time = round(time.time())
        finish_word = []
        index = 0
        while self.wait_check_random_spell_page():
            _, game_mode, word_explain_id = self.game_container()
            if game_mode == "1":
                wrong_count = len(wrong_index_info)
                print('默写单词id：', word_explain_id)
                print('单词解释：', self.word_explain())
                right_answer = word_info[word_explain_id][0]
                wrong_id = list(word_info.keys())[0]
                self.commit_btn_judge()
                page_words = self.random_show_words()
                input_alpha = [x for x, y in zip(right_answer, page_words) if x != y]
                print("正确输入单词：", input_alpha)
                if word_explain_id in finish_word:
                    self.base_assert.except_error('单词已完成， 但是再次出现 ' + word_explain_id)
                if not do_right:
                    if word_explain_id == wrong_id:
                        wrong_index_info.append(bank_index[0])
                        self.random_spell_process()
                        if len(wrong_index_info) == 5:
                            finish_word.append(word_explain_id)
                    else:
                        self.random_spell_process(do_right=True, right_answer=input_alpha)
                        finish_word.append(word_explain_id)
                else:
                    self.random_spell_process(do_right=True, right_answer=input_alpha)
                    finish_word.append(word_explain_id)

                self.commit_btn_judge(status=True)
                self.commit_btn().click()
                if len(wrong_index_info) != wrong_count:
                    if not self.wait_check_answer_page():
                        self.base_assert.except_error('随机拼写提交后未发现正确答案')
                    else:
                        print('随机拼写正确答案：', self.right_answer())
                    time.sleep(4)
                    self.commit_btn().click()
                index += 1
                bank_index[0] += 1
                time.sleep(3)
                print('-' * 20, '\n')
        spend_seconds = round(time.time()) - begin_time
        return spend_seconds












