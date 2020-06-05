import random
import time
import unittest

from app.common_ele.select_course import SelectCoursePage
from app.passion.object_page.chapter_page import ChapterPage
from app.passion.object_page.exam_list import ExamPage
from app.passion.object_page.home_page import PassionHomePage
from app.passion.object_page.game_study import GameStudy
from app.passion.test_data.passion_config import *

from app.common_ele.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, teststeps, testcase
from utils.assert_func import ExpectingTest


class ChapterExam(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = PassionHomePage()
        cls.chapter = ChapterPage()
        cls.exam = ExamPage()
        cls.wrong_note = {}
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, SCHOOL_PASSWORD)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ChapterExam, self).run(result)

    @testcase
    def test_chapter_exam(self):
        SelectCoursePage().select_course_operate('地理', card_index=0, book_index=0)
        if self.home.wait_check_home_page():
            book_id = self.home.book_id()
            # 点击章考试 中途退出
            self.home.chapter_study().click()
            time.sleep(2)
            if self.chapter.wait_chapter_page():
                self.chapter.chapter_exam_btn().click()
                before_chapter_score = self.chapter.chapter_exam_score()
                if self.home.wait_check_tip_box_page():
                    print(self.home.tip_box_content())
                    self.home.cancel_btn().click()
                if self.home.wait_check_start_study_page():
                    print(self.home.start_text(), '\n')
                    self.home.click_start_button()
                mine_answer_info = {}
                self.exam.exam_operate(do_right=True, half_exit=True, mine_answer_info=mine_answer_info)

                #  验证中途退出分数是否发生变化
                if self.home.wait_check_tip_box_page():
                    print(self.home.tip_box_content())
                    self.home.confirm_btn().click()
                if self.chapter.wait_chapter_page():
                    print('页面分数：', self.chapter.chapter_exam_score())
                    if self.chapter.chapter_exam_score() != before_chapter_score:
                        self.base_assert.except_error('章考核中途退出后章考核分数发生变化')

                # 验证中途退出再次进入上次做的题是否依然处于完成状态
                self.chapter.chapter_exam_btn().click()
                if self.chapter.wait_check_tip_box_page():
                    print(self.home.tip_box_content())
                    self.home.confirm_btn().click()
                if not self.exam.wait_check_answer_card_page():
                    self.base_assert.except_error("点击从上一次退出的地方进入未进入试卷答题卡页面")
                else:
                    if 'filled' not in self.exam.exam_bank_num()[0].get_attribute('class'):
                        self.base_assert.except_error('从退出的地方进入第一题答题卡显示未作答')
                    self.exam.exam_bank_num()[0].click()
                    if self.exam.wait_check_exam_page():
                        select_opt_letters = self.exam.select_bank_opt_letter()
                        if not len([x for x in select_opt_letters if 'activate' not in x.get_attribute('class')]):
                            self.base_assert.except_error('页面不存在已选择选项，但是答题卡显示该题已选择')

                #  做试卷，查看答案
                mine_answer_info = {}
                do_right = random.choice([False, True])
                self.exam.exam_operate(do_right=do_right, half_exit=False, mine_answer_info=mine_answer_info)
                print('我的答案：', mine_answer_info, '\n')
                if self.exam.wait_check_answer_card_page():
                    exam_result_score = self.exam.exam_result_score()
                    check_score = 100 if do_right else 0
                    if exam_result_score != check_score:
                        self.base_assert.except_error('试卷得分与计算得分不一致')
                    self.exam.check_answer_operate(do_right, mine_answer_info)
                    self.exam.exit_icon().click()



