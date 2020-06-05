#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/3 14:57
# -----------------------------------------
import unittest


from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.recite_word_page import ReciteWordPage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.test_data.account import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class ReciteWordProcess(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = WordHomePage()
        cls.recite = ReciteWordPage()
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, STU_PASSWORD)
        cls.stu_id = cls.recite.data.get_student_id(STUDENT_ACCOUNT)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ReciteWordProcess, self).run(result)


    @testcase
    def test_review_word_operate(self):
        """测试复习单词"""
        if self.home.wait_check_home_page():
            SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        book_id = self.home.driver.current_url.split('/')[-1]
        print('书籍id：', book_id)
        print(self.home.wordbook_tip_content())
        unit_list = self.home.unit_list()
        unit_list[1].click()
        self.home.click_review_word_tab()
        start_content = self.home.start_text()
        print(start_content)
        self.home.click_start_button()
        spend_time_info = {}
        self.recite.recite_word_process(self.stu_id, book_id, start_content)
        print(spend_time_info)
        print('本次做题总用时：', sum([spend_time_info[x]['总用时'] for x in spend_time_info]))

