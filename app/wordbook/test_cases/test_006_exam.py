#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/4 16:41
# -----------------------------------------
import random
import re
import time
import unittest

from ddt import ddt, data, unpack

from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from app.wordbook.objects_page.exam_game_page import ExamGamePage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.test_data.account import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class ExamProcess(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = WordHomePage()
        cls.exam = ExamGamePage()
        cls.game = NewWordGameOperatePage()
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, STU_PASSWORD)
        cls.stu_id = cls.exam.data.get_student_id(STUDENT_ACCOUNT)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ExamProcess, self).run(result)

    @data(
            [False, False],
            # [True, False],
            # [True, True]
          )
    @unpack
    @testcase
    def test_exam_operate(self, vocab_do_right, spell_do_right):
        if self.home.wait_check_home_page():
            SelectCoursePage().select_course_operate('英语', card_index=CARD_INDEX, book_index=BOOK_INDEX)
        if self.home.wait_check_home_page():
            stu_id = self.game.data.get_student_id(STUDENT_ACCOUNT)
            book_id = self.home.driver.current_url.split('/')[-1]
            print('书籍id：', book_id)
            print(self.home.wordbook_tip_content(), '\n')
            unit_list = self.home.unit_list()
            unit_index = 0
            unit_name = unit_list[unit_index].text
            unit_id = self.game.data.get_unit_catalog_id(book_id, unit_name)
            unit_list[unit_index].click()
            self.home.click_test_tab()
            time.sleep(2)
            print(self.exam.tab_content())
            exam_labels = self.exam.exam_labels()
            unit_translation_ids = self.game.data.get_unit_word_translations_ids(unit_id)
            reform_unit_ids = str(unit_translation_ids).replace('[', '').replace(']', '')
            label_info = {}
            for i in range(len(exam_labels)):
                label = self.exam.exam_labels()[i]
                label_text = label.text.strip()
                label_count = int(re.findall(r'\d+', label_text)[0])
                if '今日新学' in label_text:
                    db_data = self.game.data.get_unit_word_id_today(stu_id, reform_unit_ids)
                elif '已学' in label_text:
                    db_data = self.game.data.get_unit_word_id_already(stu_id, reform_unit_ids)
                else:
                    db_data = self.game.data.get_unit_all_word_id(stu_id, reform_unit_ids)
                label_info[label_text.split('（')[0]] = db_data
                if len(db_data) != label_count:
                    self.base_assert.except_error('页面显示的单词数与查询单词数不一致， 查询数为%d，页面单词数%d' % (len(db_data), label_count))

                label.click()
                time.sleep(1)
                if 'is-checked' not in label.get_attribute('class'):
                    self.base_assert.except_error('★★★ 点击{}，但是页面显示未点中'.format(label.text))

                for x in self.exam.label_buttons():
                    if label_count == 0:
                        if 'is-disabled' not in x.get_attribute('class'):
                            self.base_assert.except_error('★★★ 今日学习个数为0，{}按钮未置灰'.format(x.text))
                    else:
                        if 'is-disabled' in x.get_attribute('class'):
                            self.base_assert.except_error('★★★ 今日学习个数不为0，{}按钮置灰'.format(x.text))

            print('label_info:', label_info)
            exam_info = {}
            unit_exam_label = self.exam.exam_labels()[-1]
            db_words = label_info['单元卷']
            print('单元单词id：', db_words)
            unit_exam_label.click()
            time.sleep(1)
            self.exam.unit_listening_btn().click()
            exam_info[unit_name + '- 单元听写'] = self.exam.exam_game_operate(self.stu_id, book_id, db_words, exam_name_suffix='单元听写',
                                                                          vocab_right=vocab_do_right, spell_right=spell_do_right)

            if self.exam.wait_check_exam_type_page():
                select_label_index = random.choice([1, 2])
                check_ids = label_info['已学'] if select_label_index == 1 else label_info['单元卷']
                already_label = self.exam.exam_labels()[select_label_index]
                already_label.click()
                time.sleep(1)
                if self.exam.online_test_btn().is_enabled():
                    self.exam.online_test_btn().click()
                    if self.exam.wait_check_exam_bank_type_page():
                        english_to_hans_checkbox = self.exam.bank_type_checkbox()[0]
                        if 'is-checked' not in english_to_hans_checkbox.get_attribute('class'):
                            self.base_assert.except_error('测试类型没有默认选择英译汉')
                        another_bank_type = random.choice(self.exam.bank_type_checkbox()[1:])
                        another_bank_type.click()
                        time.sleep(1)
                        self.exam.definite_btn().click()
                        exam_info[unit_name + '- 已学'] = self.exam.exam_game_operate(self.stu_id, book_id, check_ids, exam_name_suffix='已学',
                                                                                    vocab_right=vocab_do_right, spell_right=spell_do_right)
            self.exam.exit_icon().click()
            time.sleep(2)
            print(exam_info)












