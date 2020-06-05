#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/6 16:15
# -----------------------------------------
import json
import os
import re
import time
import unittest

from ddt import data, ddt

from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.objects_page.recite_word_page import ReciteWordPage
from app.wordbook.objects_page.restore_word_page import RestoreWordPage
from app.wordbook.objects_page.spell_word_page import SpellWordPage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from app.wordbook.test_data.account import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, teststep, testcase
from utils.assert_func import ExpectingTest


class ErrorBook(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = WordHomePage()
        cls.game = NewWordGameOperatePage()
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, STU_PASSWORD)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ErrorBook, self).run(result)


    @testcase
    def test_error_book(self):
        if self.home.wait_check_home_page():
            SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        if self.home.wait_check_home_page():
            stu_id = self.game.data.get_student_id(STUDENT_ACCOUNT)
            book_id = self.home.driver.current_url.split('/')[-1]
            print('书籍id：', book_id)
            print(self.home.wordbook_tip_content())
            pro_path = os.path.abspath('.')
            with open(pro_path + '\\app\\wordbook\\test_data\\wrong.json', 'r') as f:
                wrong_record = json.load(f)
            self.home.click_error_book_btn()
            tip_content = self.home.start_text()
            print(tip_content)
            if len(wrong_record):
                if '易错词' not in tip_content:
                    self.base_assert.except_error('★★★ 错误列表不为空， 但是页面未提示有易错词存在')
                else:
                    self.home.click_start_button()
            else:
                if '暂无' not in tip_content:
                    self.base_assert.except_error('★★★ 错误列表为空， 但是页面未提示继续努力')
                else:
                    self.home.exit_icon().click()
            before_fluency = {x: self.game.data.get_explain_fluency_by_word_id(stu_id, x) for x in list(wrong_record.keys())}
            second_wrong_words = []
            wrong_id_list = []
            wrong_count = [0, 0]
            while self.game.wait_check_container_page():
                game_container, game_mode, explain_id = self.game.game_container()
                if game_container == 'hydc-container':
                    RestoreWordPage().error_note_restore_word_operate(stu_id, book_id, wrong_id_list, second_wrong_words, wrong_count=wrong_count)
                elif game_container == 'dcpx-container':
                    SpellWordPage().error_note_spell_game_operate(stu_id, book_id, second_wrong_words, wrong_count=wrong_count)
            ReciteWordPage().check_recite_word_fluency_operate(stu_id, before_fluency)
            if wrong_count[0] != 5:
                self.base_assert.except_error('还原单词错题次数不为5')

            if any([x not in list(set(wrong_id_list)) for x in list(wrong_record.keys())]):
                self.base_assert.except_error('记录的错题不在错题再练列表中， 错题再练列表{}, 记录错题列表{}'
                                              .format(str(wrong_id_list), str(list(wrong_record.keys()))))
            self.home.exit_icon().click()










