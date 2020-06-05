#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/27 10:51
# -----------------------------------------
import datetime
import time
import unittest
import numpy as np

from app.back_text.object_page.word_choice import WordChoice
from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.exam_game_page import ExamGamePage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.test_data.account import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class TestExamToEnd(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
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
        super(TestExamToEnd, self).run(result)

    @testcase
    def test_book_test(self):
        if self.game.wait_check_home_page():
            SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        if self.game.wait_check_home_page():
            book_id = self.game.driver.current_url.split('/')[-1]
            print('书籍id：', book_id)
            unit_status = self.game.home.status_list()
            not_complete_unit = [x for x in unit_status if '100%' != x.text]
            self.game.home.click_test_to_end_btn()
            if len(not_complete_unit):
                if self.game.wait_check_error_flash_page():
                    print(self.game.error_content())
                else:
                    self.base_assert.except_error('未完成本书所有单元， 点击本书测试未提示请先完成本书的学习再来进行整体测试')
            else:
                start_content = self.game.start_text()
                print(start_content)
                test_to_end_time_info = {}
                self.game.click_start_button()
                star_time = round(time.time())
                print('开始时间：', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                time_msg = {'结束时间': '', '大题时间': {'词汇选择': 0}, '总用时': 0}
                while self.exam.vocab.wait_check_word_choice_page():
                    self.game.commit_btn_judge()
                    word_id = self.exam.game_container()[-1]
                    game_container = self.exam.vocab.word_choice_container_no_index()
                    answer_word = self.exam.data.get_word_by_word_id(word_id)
                    explain_list = self.exam.data.get_student_explain_list_by_word_id(self.stu_id, book_id, word_id)
                    print('单词id：', word_id)
                    print('测试单词：', answer_word)
                    print('解释列表：', explain_list)

                    right_index = -1
                    options = self.exam.vocab.options(game_container)
                    for i, x in enumerate(options):
                        if x.text.split('；') == explain_list:
                            print('正确答案：', x.text)
                            right_index = i
                            break
                    if right_index == -1:
                        self.base_assert.except_error('★★★ 选项不存在该单词%s F值>=1 解释合并在一起的选项' % answer_word)
                    options[right_index].click()
                    self.exam.commit_btn_judge(True)
                    self.exam.commit_btn().click()
                    time.sleep(2)
                    print('-'*30, '\n ')

                end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                used_time = round(time.time()) - star_time
                time_msg['结束时间'] = end_time
                time_msg['大题时间']['词汇选择'] = used_time
                time_msg['总用时'] = used_time
                test_to_end_time_info['一测到底'] = time_msg
                print(test_to_end_time_info)
                if self.exam.wait_check_finish_page():
                    print(self.exam.finish_content())
                    self.exam.exit_icon().click()






