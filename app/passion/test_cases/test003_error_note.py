#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/20 15:46
# -----------------------------------------
import time
import unittest

from app.common_ele.account import *
from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.passion.object_page.chapter_page import ChapterPage
from app.passion.object_page.fill_blank_game import FillBlankGame
from app.passion.object_page.game_study import GameStudy
from app.passion.object_page.home_page import PassionHomePage
from app.passion.object_page.single_choice import SingleChoiceGame
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class ErrorNote(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = PassionHomePage()
        cls.chapter = ChapterPage()
        cls.game = GameStudy()
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, SCHOOL_PASSWORD)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ErrorNote, self).run(result)

    @testcase
    def test_error_note(self):
        wrong_banks = self.home.read_data_from_file('wrong.json')
        wrong_answer_info = {x: wrong_banks[x][0] for x in wrong_banks}
        SelectCoursePage().select_course_operate('地理', card_index=0, book_index=0)
        if self.home.wait_check_home_page():
            page_wrong_num = self.home.error_num()
            if page_wrong_num != len(list(wrong_banks.keys())):
                self.base_assert.except_error('页面错题个数与记录错题个数不一致')

            # 做对一题验证错题数是否减少
            self.home.error_book().click()
            if self.home.wait_check_start_study_page():
                print(self.home.start_text())
                self.home.click_start_button()
            if self.game.wait_check_hk_wrap_page():
                attr = self.game.game_container()
                bank_id = self.game.bank_id()
                if attr == 'dx-container':
                    SingleChoiceGame().section_single_choice_operate(all_do_right=True, answer_info=wrong_answer_info,
                                                                     do_one=True)
                elif attr == 'bq-container':
                    FillBlankGame().fill_blank_operate(all_do_right=True, answer_info=wrong_answer_info,
                                                       do_one=True)
                del wrong_banks[bank_id]
                self.home.exit_icon().click()
                time.sleep(2)
            if self.home.wait_check_home_page():
                after_wrong_num = self.home.error_num()
                print('做对之后的错题数：', after_wrong_num)
                print('计算错题数：', page_wrong_num - 1)
                if after_wrong_num != page_wrong_num - 1:
                    self.base_assert.except_error("已经做对一道错题，但是错题数未减少")

            # 清空错题本， 验证错题间隔
            self.home.error_book().click()
            if self.home.wait_check_start_study_page():
                self.home.click_start_button()

            dx_count = len([x for x in list(wrong_banks.values()) if 'dx' in x])
            tk_count = len([x for x in list(wrong_banks.values()) if 'tk' in x])
            wrong_note = {}
            interval_counter = []
            dx_wrong_counter, tk_wrong_counter = [0], [0]
            wrong_bank_info, wrong_choice_info = {}, {}
            all_do_right = False
            while self.game.wait_check_hk_wrap_page():
                attr = self.game.game_container()
                if attr == 'dx-container':
                    SingleChoiceGame().section_single_choice_operate(all_do_right=all_do_right, answer_info=wrong_answer_info,
                                                                     bank_count=dx_count, interval_counter=interval_counter,
                                                                     wrong_counter=dx_wrong_counter, wrong_note=wrong_note,
                                                                     wrong_choice_info=wrong_choice_info)
                elif attr == 'bq-container':
                    FillBlankGame().fill_blank_operate(all_do_right=all_do_right, answer_info=wrong_answer_info,
                                                       bank_count=tk_count, interval_counter=interval_counter,
                                                       wrong_note=wrong_note, wrong_counter=tk_wrong_counter,
                                                       wrong_bank_info=wrong_bank_info)
            print(interval_counter)
            if self.home.wait_check_start_study_page():
                print(self.home.start_text())
                self.home.exit_icon().click()

            if self.home.wait_check_home_page():
                if self.home.error_num() != 1:
                    self.base_assert.except_error("清除错题本时做错一道题，退出后页面的错题个数不为1，错题未保留在错题本中")






