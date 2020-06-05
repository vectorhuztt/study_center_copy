#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/6 16:36
# -----------------------------------------
import time
import unittest

from app.common_ele.select_course import SelectCoursePage
from app.passion.object_page.chapter_page import ChapterPage
from app.passion.object_page.home_page import PassionHomePage
from app.passion.object_page.game_study import GameStudy
from app.passion.test_data.passion_config import *

from app.common_ele.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, teststeps, testcase
from utils.assert_func import ExpectingTest


class ChapterOrder(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = PassionHomePage()
        cls.chapter = ChapterPage()
        cls.game = GameStudy()
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
        super(ChapterOrder, self).run(result)

    @testcase
    def test_section_all_process(self):
        # self.chapter.data.delete_student_all_record()
        SelectCoursePage().select_course_operate('地理', card_index=0, book_index=0)
        if self.home.wait_check_home_page():
            book_id = self.home.book_id()
            self.home.chapter_study().click()
            time.sleep(2)
            if self.chapter.wait_chapter_page():
                active_chapters = self.chapter.check_chapter_is_available(book_id)
                chapter_ele, chapter_id = active_chapters[CHAPTER_INDEX]
                print('选择章节：', chapter_ele.text, '\n')
                chapter_ele.click()
                time.sleep(2)
                active_section_index = self.chapter.check_section_available_status(book_id, chapter_id)
                exit_start_text = 0
                for x in range(len(active_section_index)):
                    if self.chapter.wait_chapter_page():
                        self.chapter.order_study_btn().click()
                        if self.home.wait_check_start_study_page():
                            print(self.home.start_text())
                            if exit_start_text:
                                if self.home.start_text() != exit_start_text:
                                    self.base_assert.except_error('顺序学习中途退出后，再次点击顺序学习， 页面提示与退出时的提示不一致')
                            self.home.click_start_button()
                            time.sleep(1)
                            knowledge_exit_text = self.game.section_knowledge_operate(self.wrong_note, do_right=True, is_order_study=True)
                            if self.chapter.wait_chapter_page():
                                self.chapter.order_study_btn().click()
                                time.sleep(1)
                                if self.home.wait_check_start_study_page():
                                    print('======= 小节练习 ========\n')
                                    print(self.chapter.start_text(), '\n')
                                    if knowledge_exit_text != self.chapter.start_text():
                                        self.base_assert.except_error('顺序学习中途退出后，再次点击顺序学习， 页面提示与退出时的提示不一致')
                                    self.chapter.click_start_button()
                                    time.sleep(1)
                                    exit_id, exit_start_text = self.game.section_sync_operate(self.wrong_note, do_right=True, is_order_study=True)





