#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/29 10:03
# -----------------------------------------
import json
import os
import random
import re
import time
import unittest
from ddt  import ddt, data

from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.objects_page.new_word_test_page import NewWordTestPage
from conf.base_page import BasePage
from conf.decorator import teardown, setup, testcase
from app.wordbook.test_data.account import *
from utils.assert_func import ExpectingTest


class StudyWord(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = WordHomePage()
        cls.word_test = NewWordTestPage()
        cls.game = NewWordGameOperatePage()
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, STU_PASSWORD)
        cls.stu_id = cls.game.data.get_student_id(STUDENT_ACCOUNT)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(StudyWord, self).run(result)

    @testcase
    def test_study_word(self):
        """测试新词学习"""
        if self.home.wait_check_home_page():
            SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        if self.home.wait_check_home_page():
            book_id = self.home.driver.current_url.split('/')[-1]
            print('书籍id：', book_id)
            stu_id = self.word_test.data.get_student_id(STUDENT_ACCOUNT)
            print('学生id：', stu_id)
            student_name = self.word_test.data.get_user_name(stu_id)
            print('学生名称：', student_name)
            book_name = self.home.book_name()
            print('书籍名称：', book_name)
            book_type = self.word_test.data.get_book_type(book_id, stu_id)
            print('书籍类型：', book_type)
            print(self.home.wordbook_tip_content(), '\n')

            # 点击一个单元，根据当前所有单元状态， 验证点击单词学习和自主复习后的提示状态
            unit_list = self.home.unit_list()
            uncomplete_unit_index = [i for i, x in enumerate(unit_list) if x.text not in ['未完成', "100%"]]
            random_index = random.randint(0, len(unit_list) - 1)
            unit_index = uncomplete_unit_index[0] if uncomplete_unit_index else random_index
            unit_status_list = self.home.status_list()        # 所有单元状态
            self.home.check_click_tab_tip_by_unit_status(unit_status_list)
            unit_name = unit_list[unit_index].text
            unit_state = unit_status_list[unit_index].text
            unit_id = self.word_test.data.get_unit_catalog_id(book_id, unit_name)
            unit_translation_ids = self.word_test.data.get_unit_word_translations_ids(unit_id)
            # 验证点击单词学习弹出的页面提示, 并清除单元所有学习记录
            print('单元id：', unit_id)
            unit_list[unit_index].click()
            time.sleep(1)
            self.home.click_study_word_tab()
            # 开始单词学习整体流程
            if self.word_test.wait_check_start_study_page():
                start_content = self.home.start_text()
                print(start_content, '\n')
                content_num = re.findall(r'\d+', self.home.content_desc())
                print('content_num:', content_num)
                unit_total_words = int(content_num[0])
                if len(content_num) == 2:
                    rest_word_count = unit_total_words - int(content_num[-1])
                else:
                    rest_word_count = unit_total_words
                group_word_count = 5 if rest_word_count >= 5 else rest_word_count
                self.home.click_start_button()
                all_word_info = {}
                fl_change = False if unit_state == '100%' else True
                # 游戏过程
                self.game.new_word_study_process(stu_id, book_id, all_word_info=all_word_info, fl_change=fl_change,
                                                 group_count=group_word_count, book_type=book_type)
                # 学后测试及错题再练过程
                if self.word_test.wait_check_after_test_page():
                    self.word_test.start_test_btn().click()
                    mine_answer, right_words, wrong_words = \
                        self.word_test.word_test_process(stu_id, unit_translation_ids, do_right=False)
                    self.word_test.word_before_test_fail_operate(mine_answer, len(right_words))
                    if not self.word_test.wait_check_wrong_again_btn_page():
                        self.base_assert.except_error('学后测试未做全对未出现错题再练按钮')
                    else:
                        self.word_test.wrong_again_btn().click()
                        self.word_test.word_test_process(stu_id, unit_translation_ids, do_right=True,
                                                         wrong_word_list=wrong_words)

                    self.word_test.test_report_page_operate(student_name, book_name, unit_name, len(mine_answer))
                    self.word_test.exit_icon().click()
                    time.sleep(2)











