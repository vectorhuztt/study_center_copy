#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/18 10:07
# -----------------------------------------
import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.passion.object_page.passion_common import PassionCommonEle
from app.passion.object_page.passion_sql_handle import PassionSQLHandle
from conf.decorator import teststep


class FillBlankGame(PassionCommonEle):

    @teststep
    def wait_check_fill_blank_page(self):
        """填空题页面检查点"""
        locator = (By.CSS_SELECTOR, '.bq-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def blank_content(self):
        """填空题文本"""
        ele = self.driver.find_element_by_css_selector('.bq-wrap')
        return ele.text

    @teststep
    def blank_input(self):
        """填空输入框"""
        ele = self.driver.find_elements_by_css_selector('.blank-input')
        return ele

    @teststep
    def blank_result(self):
        """输入栏结果"""
        ele = self.driver.find_elements_by_css_selector('.blank-result')
        return ele

    @teststep
    def section_blank_explain(self):
        """小节练习填空提交答案解析"""
        ele = self.driver.find_element_by_css_selector('.explain')
        return ele.text

    @teststep
    def check_wrong_bank_interval(self, bank_count, wrong_index):
        if bank_count == 1:
            cal_wrong_index = [0, 1, 2]
        elif bank_count == 2:
            cal_wrong_index = [0, 2, 3]
        elif bank_count == 3:
            cal_wrong_index = [0, 3, 4]
        elif bank_count == 4:
            cal_wrong_index = [0, 3, 5]
        else:
            cal_wrong_index = [0, 3, 6]

        print('计算错题间隔：', cal_wrong_index)
        print('实际错题间隔：', wrong_index)
        if wrong_index != cal_wrong_index:
            self.base_assert.except_error('错题再练间隔不正确')

    @teststep
    def fill_blank_process(self, counter=None, do_right=False, right_answer=None):
        """填空做对操作"""
        input_answer = []
        for i, x in enumerate(self.blank_input()):
            x.click()
            if do_right:
                input_answer.append(right_answer[i])
                x.send_keys(right_answer[i].lower() + Keys.ENTER)
            else:
                if counter == 2:
                    if i == 0:
                        x.send_keys('=' + Keys.ENTER)
                        input_answer.append('=')
                    else:
                        input_answer.append(right_answer[i])
                        x.send_keys(right_answer[i].lower() + Keys.ENTER)
                else:
                    random_str = random.choice(string.ascii_lowercase)
                    input_answer.append(random_str)
                    x.send_keys(random_str + Keys.ENTER)
            time.sleep(0.5)
        return input_answer


    @teststep
    def fill_blank_operate(self, all_do_right, bank_count=0, is_half_exit=False, answer_info=None,
                           interval_counter=None, wrong_note=None, wrong_counter=None, wrong_bank_info=None,
                           do_one=False):
        """填空题处理过程
            :param wrong_bank_info: 填空错题信息
            :param do_one: 是否只做一道题
            :param answer_info: 正确答案
            :param bank_count 单选总个数
            :param wrong_counter 错题错误次数
            :param interval_counter 间隔统计列表
            :param wrong_note 错题本记录
            :param is_half_exit 是否中途退出
            :param all_do_right 是否做全对
        """


        print('========= 填空游戏 =========\n')
        index, wrong_bank_id, exit_id = 0, 0, 0
        wrong_index = []
        while self.wait_check_fill_blank_page():
            bank_id = self.bank_id()
            if answer_info:
                right_answer = answer_info[bank_id]
            else:
                right_answer = PassionSQLHandle().get_ques_right_answer(bank_id)
            print('题目id：', bank_id)
            print(self.blank_content())
            print('正确答案：', right_answer)
            if not all_do_right:
                if index == 0:
                    if wrong_bank_info:
                        wrong_bank_id = list(wrong_bank_info.keys())[0]
                    else:
                        wrong_bank_info[bank_id] = []
                        wrong_bank_id = bank_id

                if is_half_exit:
                    if index == 1:
                        exit_id = bank_id
                        self.exit_icon().click()
                        time.sleep(2)
                        break

                if bank_count < 2:
                    interval_counter.append(('填空', bank_id))
                    input_answer = self.fill_blank_process(do_right=True, right_answer=right_answer)
                else:
                    if bank_id != wrong_bank_id or wrong_counter[0] >= 2:
                        if bank_id == wrong_bank_id:
                            wrong_note[bank_id] = (right_answer, 'tk')
                            interval_counter.append(('填空', bank_id))
                            mine_input_answer = wrong_bank_info[bank_id]
                            for i, x in enumerate(self.blank_input()):
                                if mine_input_answer[i].lower() != right_answer[i].lower():
                                    if x.text:
                                        self.base_assert.except_error('本填空未做对，但是再次进入此题填空不为空')
                                    x.click()
                                    x.send_keys(right_answer[i])
                                else:
                                    if x.text.lower() != right_answer[i].lower():
                                        self.base_assert.except_error('本填空已做对， 但是再次进入填空上文本不是正确答案')
                            self.next_btn().click()
                            wrong_index.append(index)
                            input_answer = right_answer
                        else:
                            interval_counter.append(('填空', bank_id))
                            input_answer = self.fill_blank_process(do_right=True, right_answer=right_answer)
                    else:
                        wrong_counter[0] += 1
                        interval_counter.append(('填空', bank_id))
                        input_answer = self.fill_blank_process(counter=wrong_counter[0], right_answer=right_answer)
                        wrong_bank_info[bank_id] = input_answer
                        wrong_index.append(index)
            else:
                input_answer = self.fill_blank_process(do_right=True, right_answer=right_answer)
            print('我的答案：', input_answer)
            time.sleep(1)
            result_mine_answer = [x.text.split()[0] for x in self.blank_result()]
            print('结果页我的答案：', result_mine_answer)
            if [x for x, y in zip(input_answer, result_mine_answer) if x.lower() != y.lower()]:
                self.base_assert.except_error('输入答案与页面展示答案不一致')
            self.next_btn().click()
            time.sleep(1)
            index += 1
            print('-'*30, '\n')
            if do_one:
                break
        return exit_id





