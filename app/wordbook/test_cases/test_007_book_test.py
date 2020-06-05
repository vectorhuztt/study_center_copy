#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/27 10:50
# -----------------------------------------
import re
import time
import unittest

import allure
from ddt import data, ddt, unpack

from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.exam_game_page import ExamGamePage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.test_data.account import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class TestBookTest(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = WordHomePage()
        cls.game = NewWordGameOperatePage()
        cls.exam = ExamGamePage()
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
        super(TestBookTest, self).run(result)

    @allure.step('本书测试')
    @data(
        [True, False],
        # [False, True],
        # [False, False],
        # [True, True]
    )
    @unpack
    @testcase
    def test_book_test(self, vocab_right, spell_right):
        SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        unit_status = self.home.status_list()  # 所有单元状态
        not_complete_unit = [x for x in unit_status if '100%' not in x.text]
        self.home.click_book_test_btn()
        if len(not_complete_unit):
            if self.game.wait_check_error_flash_page():
                print(self.game.error_content())
            else:
                self.base_assert.except_error('未完成本书所有单元， 点击本书测试未提示请先完成本书的学习再来进行整体测试')
        else:
            start_content = self.home.start_text()  # 页面文本
            print(start_content)
            book_test_time = {}
            self.home.click_start_button()  # 开始学习
            book_id = re.findall(r'\d+', self.home.driver.current_url)[0]
            print('书籍id：', book_id)
            book_word_ids = self.game.data.get_student_book_word_count(self.stu_id, book_id)
            print('本书已背单词个数：', book_word_ids)
            book_test_time['本书测试'] = self.exam.exam_game_operate(self.stu_id, book_id, book_word_ids, exam_name_suffix='本书测试',
                                                                 vocab_right=vocab_right, spell_right=spell_right, is_book_test=True)
            print(book_test_time)
