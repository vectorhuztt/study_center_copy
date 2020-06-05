#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/29 10:03
# -----------------------------------------
import json
import os
import random
import re
import time
import unittest
from ddt  import ddt, data

from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.objects_page.new_word_test_page import NewWordTestPage
from conf.base_page import BasePage
from conf.decorator import teardown, setup, testcase
from app.wordbook.test_data.account import *
from utils.assert_func import ExpectingTest

@ddt
class StudyWord(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = WordHomePage()
        cls.word_test = NewWordTestPage()
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
        super(StudyWord, self).run(result)

    @data(False, True)
    @testcase
    def test_study_word(self, test_do_right):
        """测试新词学习"""
        if self.home.wait_check_home_page():
            SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        if self.home.wait_check_home_page():
            book_id = self.home.driver.current_url.split('/')[-1]
            print('书籍id：', book_id)
            stu_id = self.word_test.data.get_student_id(STUDENT_ACCOUNT)
            print('学生id：', stu_id)
            student_name = self.word_test.data.get_user_name(stu_id)
            print('学生名称：', student_name)
            book_name = self.home.book_name()
            print('书籍名称：', book_name)
            book_type = self.word_test.data.get_book_type(book_id, stu_id)
            print('书籍类型：', book_type)

            # 选择一个单元， 若存在未完成单元，则选择， 若不存在则随机选择一个单元
            unit_list = self.home.unit_list()
            uncomplete_unit_index = [i for i, x in enumerate(unit_list) if x.text not in ['未完成', "100%"]]
            random_index = random.randint(0, len(unit_list) - 1)
            unit_index = uncomplete_unit_index[0] if uncomplete_unit_index else random_index
            unit_name = unit_list[unit_index].text
            unit_state = self.home.status_list()[unit_index].text
            unit_id = self.word_test.data.get_unit_catalog_id(book_id, unit_name)
            print('单元id：', unit_id)
            self.game.data.delete_student_unit_word_record(stu_id, book_id, unit_id)
            # 删除学生学习记录后， 清空错题记录文本内容
            pro_path = os.path.abspath('.')
            with open(pro_path + '\\app\\wordbook\\test_data\\wrong.json', 'w') as f:
                f.write(json.dumps({}))
            self.home.driver.refresh()
            time.sleep(3)

            # 开始学前测试， 验证提交后的页面以及单元状态
            select_unit = self.home.unit_list()[unit_index]
            select_unit.click()
            time.sleep(1)
            self.home.click_study_word_tab()
            unit_words_count = self.word_test.data.get_unit_words_count(unit_id)
            unit_translation_ids = self.word_test.data.get_unit_word_translations_ids(unit_id)
            page_word_count = self.word_test.page_words_count()[0]
            if unit_words_count != int(page_word_count):
                self.base_assert.except_error('页面单词个数与数据库查询个数不一致')

            # 学前测试流程
            print("学前测试是否做对：", test_do_right)
            self.word_test.start_test_btn().click()
            mine_input_answer, right_words, _ =\
                self.word_test.word_test_process(stu_id, unit_translation_ids, do_right=test_do_right)
            # 全部做对,弹出奖状， 未做全对，给出做题详情
            if test_do_right:
                self.word_test.test_report_page_operate(student_name, book_name, unit_name, len(right_words))
                self.home.click_study_word_tab()
            else:
                self.word_test.word_before_test_fail_operate(mine_input_answer, len(right_words), is_before_test=True)
                self.word_test.submit_btn().click()
                time.sleep(1)
                if not self.word_test.wait_check_start_study_page():
                    self.base_assert.except_error('点击继续学习， 未进入错词新学开始页面')
                else:
                    if len(right_words) != int(self.word_test.page_words_count()[1]):
                        self.base_assert.except_error('页面显示完成个数与测试正确个数不一致')

            if self.word_test.wait_check_start_study_page():
                start_content = self.home.start_text()
                print(start_content, '\n')
                content_num = re.findall(r'\d+', self.home.content_desc())
                print('content_num:', content_num)
                unit_total_words = int(content_num[0])
                if len(right_words) == unit_total_words:
                    if "重新学习" not in start_content:
                        self.base_assert.except_error("学前测试已做全对， 页面提示内容不是重新学习提示")
                if len(content_num) == 2:
                    if int(content_num[-1]) != len(right_words):
                        self.base_assert.except_error("页面显示完成个数与测试正确个数不一致")
                self.home.exit_icon().click()









