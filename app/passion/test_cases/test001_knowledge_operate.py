#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2020/1/16 8:14
# -----------------------------------------
import time
import unittest

from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.passion.object_page.chapter_page import ChapterPage
from app.passion.object_page.game_study import GameStudy
from app.passion.object_page.home_page import PassionHomePage
from app.passion.test_data.passion_config import *
from conf.base_page import BasePage
from conf.decorator import setup, teststeps, testcase, teardown
from utils.assert_func import ExpectingTest


class KnowledgeOperate(unittest.TestCase):
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
        self.home.write_data_to_file('wrong.json', 'w', self.wrong_note)

    def run(self, result=None):
        self.result = result
        super(KnowledgeOperate, self).run(result)

    @testcase
    def test_chapter_last_oder(self):
        self.chapter.data.delete_student_all_record()
        SelectCoursePage().select_course_operate('地理', card_index=0, book_index=0)
        if self.home.wait_check_home_page():
            book_id = self.home.book_id()
            page_chapter_num = self.home.chapter_total_num()
            self.chapter.chapter_num_check(book_id, page_chapter_num)
            self.home.chapter_study().click()
            time.sleep(2)
            if self.chapter.wait_chapter_page():
                # 校验章节和小节是否已上架
                active_chapters = self.chapter.check_chapter_is_available(book_id)
                chapter_ele, chapter_id = active_chapters[CHAPTER_INDEX]
                print('选择章节：', chapter_ele.text, '\n')
                chapter_ele.click()
                time.sleep(3)
                self.chapter.check_shelves_chapter_data(book_id, chapter_id)
                active_section_index = self.chapter.check_section_available_status(book_id, chapter_id)
                select_section_index, section_id = active_section_index[SECTION_INDEX]

                section_ele = self.chapter.section_father_box_ele()[select_section_index]
                progress = self.chapter.section_progress(section_ele)
                print('图书进度：', progress)
                self.chapter.section_knowledge_btn(section_ele).click()
                time.sleep(2)
                quit_start_text = 0
                # 知识点中途退出操作
                if self.home.wait_check_start_study_page():
                    print(self.home.start_text())
                    self.home.click_start_button()
                    quit_start_text = self.game.section_knowledge_operate(self.wrong_note, is_half_exit=True)
                if self.chapter.wait_chapter_page():

                    # 验证完成一组后小节进度是否发生变化
                    if quit_start_text:
                        section_ele = self.chapter.section_father_box_ele()[select_section_index]
                        section_progress = self.chapter.section_progress(section_ele)
                        print('完成一组后的小节进度：', section_progress)
                        if section_progress == progress:
                            self.base_assert.except_error("完成一组知识点中途退出后，小节进度未发生变化")
                        # 验证完成一组后再次点击进入页面提示是否发生改变
                        self.chapter.section_knowledge_btn(section_ele).click()
                        if self.home.wait_check_start_study_page():
                            if self.home.start_text() != quit_start_text:
                                self.base_assert.except_error("完成一组知识点退出后， 再次进入知识点，页面提示内容不为下一组知识点")
                            self.home.click_start_button()
                            # 完成剩下所有知识点操作
                            self.game.section_knowledge_operate(self.wrong_note)
                    else:
                        print('========= 该小节知识点只有一组 =========\n')