#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/7 15:33
# -----------------------------------------
import random
import unittest

from selenium.webdriver import ActionChains

from app.common_ele.select_course import SelectCoursePage
from app.passion.object_page.exam_list import ExamPage
from app.passion.object_page.home_page import PassionHomePage
from app.passion.test_data.passion_config import *
from app.passion.object_page.sql_data import Sql
from app.passion.object_page.game_study import GameStudy
from app.common_ele.login_page import LoginPage
from conf.decorator import setup, teardown
from ddt import ddt, data

from utils.assert_func import ExpectingTest


class Examination(unittest.TestCase):
    sql = Sql()
    sql.start_db()
    # exam_count = sql.get_all_exam(2)[0][0]

    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.game = GameStudy()
        cls.home = PassionHomePage()
        cls.exam = ExamPage()
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, SCHOOL_PASSWORD)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(Examination, self).run(result)

    def test_exam_process(self):
        """试卷做题过程"""
        SelectCoursePage().select_course_operate('地理', card_index=0, book_index=0)
        if self.home.wait_check_home_page():
            self.home.exam().click()
            mine_answer_info = {}
            #  选择一个试卷，并输出试卷信息
            if self.exam.wait_check_exam_record_list_page():
                exam_list = self.exam.exam_group_ele()
                random_index = random.randint(0, len(exam_list) - 1)
                select_exam = exam_list[random_index]
                exam_name = self.exam.exam_name(select_exam)
                exam_date = self.exam.latest_exam_date(select_exam)
                exam_time = self.exam.exam_used_time(select_exam)
                exam_score = self.exam.exam_score(select_exam)

                print('试卷名称：', exam_name, '\n',
                      '试卷最新完成时间：', exam_date, '\n',
                      '试卷耗时：', exam_time, '\n',
                      '试卷得分：', exam_score, '\n')
                start_exam_btn = self.exam.start_exam_by_ele(select_exam)
                ActionChains(self.exam.driver).click(start_exam_btn).perform()

                #  中途做对退出，验证分数是否变化
                if self.home.wait_check_start_study_page():
                    print(self.home.start_text())
                    self.home.click_start_button()
                self.exam.exam_operate(do_right=True, half_exit=True, mine_answer_info=mine_answer_info)
                if self.exam.wait_check_exam_record_list_page():
                    if self.exam.exam_score(select_exam) == exam_score:   # 待议
                        self.base_assert.except_error('已经做对一题， 中途退出以后成绩未发生变化')

                #  完成所有题
                ActionChains(self.exam.driver).click(start_exam_btn).perform()
                if self.home.wait_check_start_study_page():
                    print(self.home.start_text())
                    self.home.click_start_button()
                    mine_answer_info = {}
                    do_right = random.choice([False, True])
                    self.exam.exam_operate(do_right=do_right, half_exit=False, mine_answer_info=mine_answer_info)
                    self.exam.exit_icon().click()

                    # 查看报告，验证记录答案和页面答案是否一致
                    if self.exam.wait_check_exam_record_list_page():
                        check_report_btn = self.exam.check_report(select_exam)
                        ActionChains(self.exam.driver).click(check_report_btn).perform()
                    if self.exam.wait_check_answer_card_page():
                        exam_result_score = self.exam.exam_result_score()
                        check_score = 100 if do_right else 0
                        if exam_result_score != check_score:
                            self.base_assert.except_error('试卷得分与计算得分不一致')
                        self.exam.check_answer_operate(do_right, mine_answer_info)