import random
import time
import unittest

from ddt import ddt, data

from app.common_ele.select_course import SelectCoursePage
from app.passion.object_page.chapter_page import ChapterPage
from app.passion.object_page.game_study import GameStudy
from app.passion.object_page.home_page import PassionHomePage

from app.common_ele.login_page import LoginPage
from app.passion.test_data.passion_config import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, teststeps
from utils.assert_func import ExpectingTest


class SectionKnowledge(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = PassionHomePage()
        cls.chapter = ChapterPage()
        cls.game = GameStudy()
        cls.wrong_note = cls.home.read_data_from_file('wrong.json')
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, SCHOOL_PASSWORD)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)
        self.home.write_data_to_file('wrong.json', 'w', self.wrong_note)

    def run(self, result=None):
        self.result = result
        super(SectionKnowledge, self).run(result)

    @teststeps
    def test_chapter_last_oder(self):
        SelectCoursePage().select_course_operate('地理', card_index=0, book_index=0)
        if self.home.wait_check_home_page():
            book_id = self.home.book_id()
            page_chapter_num = self.home.chapter_total_num()
            self.chapter.chapter_num_check(book_id, page_chapter_num)
            self.home.chapter_study().click()
            time.sleep(2)
            if self.chapter.wait_chapter_page():
                # 验证小节是否已上架，并随机选择已上架的一个小节
                active_chapters = self.chapter.check_chapter_is_available(book_id)
                chapter_ele, chapter_id = active_chapters[CHAPTER_INDEX]
                print('选择章节：', chapter_ele.text, '\n')
                chapter_ele.click()
                time.sleep(3)
                self.chapter.check_shelves_chapter_data(book_id, chapter_id)
                active_section_index = self.chapter.check_section_available_status(book_id, chapter_id)
                select_section_index, section_id = active_section_index[SECTION_INDEX]

                section_ele = self.chapter.section_father_box_ele()[select_section_index]
                self.chapter.section_sync_exercise(section_ele).click()
                if self.home.wait_check_start_study_page():
                    print(self.home.start_text(), '\n')
                    self.home.click_start_button()
                    self.game.section_sync_operate(self.wrong_note, section_id=section_id)

                exit_id = 0
                if self.chapter.wait_chapter_page():
                    section_ele = self.chapter.section_father_box_ele()[select_section_index]
                    self.chapter.section_sync_exercise(section_ele).click()
                    time.sleep(2)
                    self.home.click_start_button()
                    exit_id = self.game.section_sync_operate(self.wrong_note, is_half_exit=True, section_id=section_id)
                    print('退出时页面题目id：', exit_id)

                if exit_id == 0:
                    print('同步练习只有一道选择题')
                else:
                    if self.chapter.wait_chapter_page():
                        section_ele = self.chapter.section_father_box_ele()[select_section_index]
                        self.chapter.section_sync_exercise(section_ele).click()
                        time.sleep(2)
                        self.home.click_start_button()
                        time.sleep(2)
                        game_id = self.chapter.bank_id()
                        print('再次进入时题目id：', game_id)
                        if game_id == exit_id:
                            self.base_assert.except_error("同步练习中途退出后， 再次点击进入的题目id与退出时的题目id一致")