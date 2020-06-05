#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/18 8:50
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.passion.object_page.passion_common import PassionCommonEle
from conf.decorator import teststep


class CompleteTextGame(PassionCommonEle):

    @teststep
    def wait_check_complete_text_page(self):
        """补全文章游戏页面检查点"""
        locator = (By.CSS_SELECTOR, '.xt-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def bank_text(self):
        """题目文章"""
        ele = self.driver.find_element_by_css_selector('.text')
        return ele.text

    @teststep
    def opt_list(self):
        """选项列表"""
        ele = self.driver.find_element_by_css_selector('.options .el-row div:nth-child(2)')
        return ele

    @teststep
    def text_blank(self):
        """文章填空处"""
        ele = self.driver.find_elements_by_css_selector('.text  .focus .chooseing')
        return ele

    @teststep
    def result_blank(self):
        """提交后填空结果"""
        ele = self.driver.find_elements_by_css_selector('.text .focus .report')
        return ele

    @teststep
    def get_result_mine_answer(self, blank_list):
        mine_answer = []
        for x in blank_list:
            blank_text = x.text.strip()
            if '（' in blank_text:
                if '未作答' in blank_text:
                    mine_answer.append('')
                else:
                    mine_answer.append(blank_text.split('（')[1].replace('）', ''))
            else:
                mine_answer.append(blank_text)
        return mine_answer

    @teststep
    def complete_text_operate(self, right_answer, do_right=False):
        print('========= 补全文章 =========\n')
        if self.wait_check_complete_text_page():
            print(self.bank_text())
            if do_right:
                count = 0
                while count < len(right_answer):
                    for x in self.opt_list():
                        if x.text == right_answer[count]:
                            x.click()
                            count += 1
                            break
            else:
                self.next_btn().click()
                time.sleep(2)
            mine_answer = self.get_result_mine_answer(self.result_blank())
            print('我的答案：', mine_answer)
            if do_right:
                if mine_answer != right_answer:
                    self.base_assert.except_error('提交答案后， 页面答案与选择答案不一致')
            else:
                if len([x for x in mine_answer if x]):
                    self.base_assert.except_error('未选择任何答案， 提交过后页面存在未作答的填空')
            self.next_btn().click()
            print('-'*30, '\n')
            time.sleep(2)




