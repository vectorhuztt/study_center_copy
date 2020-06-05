#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/30 14:32
# -----------------------------------------
import unittest

from app.common_ele.account import *
from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.objects_page.recite_word_page import ReciteWordPage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.test_data.account import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class EnforceReview(unittest.TestCase):

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
        cls.stu_id = cls.game.data.get_student_id(STUDENT_ACCOUNT)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(EnforceReview, self).run(result)

    @testcase
    def test_enforce_review(self):
        if self.home.wait_check_home_page():
            SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        if self.home.wait_check_home_page():
            book_id = self.home.driver.current_url.split('/')[-1]
            print('书籍id：', book_id)
            update_words = self.game.data.update_student_word_date_to_review(self.stu_id, book_id)
            self.home.click_study_word_tab()
            if self.game.wait_check_start_study_page():
                start_content = self.home.start_text()
                print(start_content, '\n')
                self.home.click_start_button()
                if '强制复习' not in start_content:
                    self.base_assert.except_error("已经设置单词学习记录， 点击单词学习未出现强制复习页面")
                else:
                    recite_word_info = ReciteWordPage().recite_word_process(self.stu_id, book_id, start_content)
                    if [x for x in update_words if str(x) not in list(recite_word_info.keys())]:
                        self.base_assert.except_error("强制复习单词与数据查询单词不一致，查询数据为{}, 实际复习单词为{}"
                                                      .format(str(update_words), str(list(recite_word_info.keys()))))
