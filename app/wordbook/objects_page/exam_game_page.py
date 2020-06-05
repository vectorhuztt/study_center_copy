#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/11/26 16:12
# -----------------------------------------
import datetime
import random
import re
import string
import time
import numpy as np
from selenium.webdriver.common.by import By
from app.wordbook.objects_page.exam_page import ExamPage
from conf.decorator import teststep, teststeps


class ExamGamePage(ExamPage):

    @teststep
    def wait_check_exam_wrap_page(self):
        """试卷页面检查点"""
        locator = (By.CSS_SELECTOR, '.exam-wrap')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_exam_result_page(self):
        locator = (By.CSS_SELECTOR, '.exam-result')
        return self.get_wait_check_page_result(locator)


    @teststeps
    def exam_game_operate(self, stu_id, book_id, db_words, exam_name_suffix,
                          vocab_right=None, spell_right=None, is_book_test=False, exam_type=2):
        """试卷做题过程
            :param is_book_test: 是否为本书测试
            :param book_id:   书籍id
            :param spell_right: 单词拼写是否做对
            :param vocab_right:  词汇选择是否做对
            :param exam_type: 试卷类型，1：新学  2：已学
            :param exam_name_suffix: 试卷名称后缀
            :param db_words: 数据库查询单词数据
            :param stu_id 学生id
        """
        start_time = round(time.time())
        time_msg = {'结束时间': '',  '大题时间': {'词汇选择': 0, '单词拼写': 0}, '总用时': 0, '得分': 0}
        if vocab_right and spell_right:
            time_msg['得分'] = 100
        bank_time = time_msg['大题时间']
        mine_answer_info = {'词汇选择': {}, '单词拼写': {}}
        if self.vocab.wait_check_word_choice_page():
            vocab_answer, spend_time = self.vocab_select_game_operate(stu_id, book_id, db_words, vocab_right, exam_type)
            mine_answer_info['词汇选择'].update(vocab_answer)
            bank_time['词汇选择'] = spend_time

        if self.spell.wait_check_spell_word_page():
            spell_answer, spend_time = self.spell_game_operate(stu_id, book_id, db_words, spell_right)
            mine_answer_info['单词拼写'].update(spell_answer)
            bank_time['单词拼写'] += spend_time

        if self.listen_spell.wait_check_listen_spell_page():
            listen_spell_answer, spend_time = self.listen_spell_game_operate(db_words, spell_right)
            mine_answer_info['单词拼写'].update(listen_spell_answer)
            bank_time['单词拼写'] += spend_time

        self.click_carry_out_btn()
        self.alert_tab_operate()
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exam_spend_time = round(time.time()) - start_time
        time_msg['总用时'] = exam_spend_time
        time_msg['结束时间'] = end_time
        print(time_msg)
        if self.wait_check_exam_result_page():
            print(self.exam_name())
            if exam_name_suffix not in self.exam_name():
                self.base_assert.except_error("试卷类型为已学单词， 但是试卷题目未标明为已学")
            self.exam_result_page_operate(mine_answer_info, vocab_right, spell_right, is_book_test)
        return time_msg

    @teststeps
    def exam_result_page_operate(self, mine_answer_info, vocab_right, spell_right, is_book_test):
        score = self.score()
        all_items = self.get_all_item()
        if vocab_right and spell_right:
            if score != 100:
                self.base_assert.except_error('★★★ 计算分数与实际分数不一致，实际分数为%d，计算分数为100' % score)
            else:
                print('分数核对成功， 得分为%d分' % score)
        else:
            check_score = 0
            if not is_book_test:
                if vocab_right:
                    check_score = round(float(len(mine_answer_info['词汇选择']) / len(all_items)) * 100)
                if spell_right:
                    check_score = round(float(len(mine_answer_info['单词拼写']) / len(all_items)) * 100)

            if score != check_score:
                self.base_assert.except_error('★★★ 计算分数与实际分数不一致，实际分数为%d，计算分数为%d' % (score, check_score))
            else:
                print('分数核对成功， 得分为%d分' % score)

        right_answer = []
        for x in all_items:
            word_index = self.word_index(x)
            word = self.result_words(x).strip()
            word_explain = self.result_word_explain(x)
            word_game_type = self.word_game_type(x)
            if '词汇选择' in word_game_type:
                mine_answer_status = self.vocab_select_icon(x)
            else:
                mine_answer_status = self.spell_icon(x)

                mine_answer = mine_answer_info['单词拼写'][word]
                if mine_answer != mine_answer_status.text:
                    self.base_assert.except_error('页面展示的我的单词与实际填入单词不一致, 页面为{}, '
                                                  '我输入的{}'.format(mine_answer_status.text, mine_answer))
                else:
                    right_answer.append(word)

            if 'success' in mine_answer_status.get_attribute('class'):
                status = '正确'
            else:
                status = '错误'

            print(word_index, word, word_explain, word_game_type, mine_answer_status.text, status, sep='  ')
            if '词汇选择' in word_game_type:
                if vocab_right:
                    if status == '错误':
                        self.base_assert.except_error('单词{}做题状态错误， 应为正确， 实际为错误'.format(word))
                else:
                    if status == '正确':
                        self.base_assert.except_error('单词{}做题状态错误， 应为错误， 实际为正确'.format(word))

            elif '单词拼写' in word_game_type:
                if spell_right:
                    if status == '错误':
                        self.base_assert.except_error('单词{}做题状态错误， 应为正确， 实际为错误'.format(word))
                else:
                    if status == '正确':
                        self.base_assert.except_error('单词{}做题状态错误， 应为错误， 实际为正确'.format(word))

            if word_game_type not in list(mine_answer_info.keys()):
                self.base_assert.except_error('单词{}类型不在选择测试类型列表中'.format(word))
        self.exit_icon().click()
        time.sleep(3)
