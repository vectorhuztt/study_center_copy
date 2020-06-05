#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/18 14:46
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.passion.object_page.passion_common import PassionCommonEle
from app.passion.object_page.passion_sql_handle import PassionSQLHandle
from conf.decorator import teststep


class SingleChoiceGame(PassionCommonEle):

    @teststep
    def wait_check_single_choice_page(self):
        """单选页面检查点"""
        locator = (By.CSS_SELECTOR, '.dx-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def question(self):
        """单选问题"""
        ele = self.driver.find_element_by_css_selector('.exercise-body .question')
        return ele.text

    @teststep
    def opt_letters(self):
        """选项字母"""
        ele = self.driver.find_elements_by_css_selector('.option .letter')
        return ele

    @teststep
    def opt_content(self):
        """选项内容"""
        ele = self.driver.find_elements_by_css_selector('.option .text')
        return ele

    @teststep
    def section_select_explain(self):
        """小节练习单选解析"""
        ele = self.driver.find_element_by_css_selector('.explain')
        return ele.text


    @teststep
    def single_choice_do_process(self, do_right=False, right_answer=None):
        """单项选择做题过程"""
        mine_answer = 0
        for i, x in enumerate(self.opt_content()):
            if do_right:
                if x.text.strip() == right_answer:
                    mine_answer = x.text
                    x.click()
                    break
            else:
                if x.text.strip() != right_answer:
                    mine_answer = x.text
                    x.click()
                    break
        return mine_answer

    @teststep
    def section_single_choice_operate(self, all_do_right, answer_info=None, is_half_exit=False, bank_count=None,
                                      interval_counter=None, wrong_counter=None, wrong_note=None,
                                      wrong_choice_info=None, do_one=False):
        """同步练习单选操作
            :param do_one: 是否只做一道题
            :param answer_info: 正确答案
            :param wrong_choice_info: 错题信息
            :param bank_count 单选总个数
            :param wrong_counter 错题错误次数
            :param interval_counter 间隔统计列表
            :param wrong_note 错题本记录
            :param is_half_exit 是否中途退出
            :param all_do_right 是否做全对
        """
        index, wrong_id = 0, 0
        exit_id = 0
        while self.wait_check_single_choice_page():
            bank_id = self.bank_id()
            question = self.question()
            print('题目id：', bank_id)
            print('问题：', question)
            if answer_info:
                right_answer = answer_info[bank_id]
            else:
                right_answer = PassionSQLHandle().get_ques_right_answer(bank_id)
            print('正确答案：', right_answer)
            if not all_do_right:
                if is_half_exit:
                    if index == 1:
                        exit_id = bank_id
                        self.exit_icon().click()
                        break
                if index == 0:
                    if wrong_choice_info:
                        wrong_id = list(wrong_choice_info.keys())[0]
                    else:
                        wrong_choice_info[bank_id] = []
                        wrong_id = bank_id

                if bank_count < 2:
                    interval_counter.append(('选择', bank_id))
                    self.single_choice_do_process(do_right=True, right_answer=right_answer)
                else:
                    if bank_id != wrong_id or wrong_counter[0] >= 2:
                        if bank_id == wrong_id:
                            wrong_note[bank_id] = (right_answer, 'dx')
                        interval_counter.append(('选择', bank_id))
                        self.single_choice_do_process(do_right=True, right_answer=right_answer)
                    else:
                        wrong_counter[0] += 1
                        self.single_choice_do_process(right_answer=right_answer)
                        interval_counter.append(('选择', bank_id))
            else:
                self.single_choice_do_process(do_right=True, right_answer=right_answer)
            self.next_btn().click()
            time.sleep(0.5)
            index += 1
            if self.wait_check_explain_page():
                print(self.section_select_explain())
            self.next_btn().click()
            time.sleep(1)
            print('-'*30, '\n')
            if do_one:
                break
        return exit_id







