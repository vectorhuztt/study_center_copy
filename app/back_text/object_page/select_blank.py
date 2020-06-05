#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/4 16:16
# -----------------------------------------
import random
import re
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.back_text.object_page.complete_text import CompleteText
from conf.decorator import teststep, teststeps


class SelectWordBlank(CompleteText):

    @teststep
    def wait_check_hint_word_page(self):
        """提示词页面检查点"""
        locator = (By.CSS_SELECTOR, '.extras span')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_select_blank_page(self):
        """选词填空页面检查点"""
        locator = (By.CSS_SELECTOR, '.xctk-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def select_blank_container_no_index(self):
        """结果页父级容器元素"""
        ele = self.driver.find_element_by_css_selector('.xctk-container')
        return ele

    @teststep
    def select_blank_container_with_index(self, index):
        """结果页父级容器元素"""
        ele = self.driver.find_element_by_css_selector('div[class ~="xctk-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def hint_word(self, container_ele):
        """提示词"""
        ele = container_ele.find_element_by_css_selector('.extras span')
        return ele.text

    @teststep
    def blank_article(self, container_ele):
        """选词填空文章"""
        ele = container_ele.find_element_by_css_selector('.article-wrap')
        return ele.text

    @teststep
    def blank_wrap(self, container_ele):
        """选词填空填空"""
        ele = container_ele.find_elements_by_css_selector('.article-wrap .blank-wrap .blank-input')
        return ele

    @teststep
    def select_blank_do_process(self, game_container, fq, right_answer=None):
        mine_answer = []
        blank_wrap = self.blank_wrap(game_container)
        for i, wrap in enumerate(blank_wrap):
            wrap.click()
            if (fq == 1 and i in [0, 1]) or fq == 2:
                mine_answer.append(right_answer[i])
                wrap.send_keys(right_answer[i] + Keys.ENTER)
            else:
                random_str = ''.join(random.sample(string.ascii_lowercase, random.randint(2, 4)))
                mine_answer.append(random_str)
                wrap.send_keys(random_str + Keys.ENTER)
            time.sleep(0.5)
        return mine_answer

    @teststep
    def select_blank_result_operate(self, mine_answer, game_container):
        """选词填空结果页答案校验"""
        page_mine_answer = self.result_mine_answer(game_container)
        for i, ans in page_mine_answer:
            if ans != mine_answer[i]:
                self.base_assert.except_error('结果页我的答案与我输入的不一致 ' + ans)

    @teststeps
    def select_word_blank_game_operate(self):
        """选词填空游戏过程"""
        start_time = round(time.time())
        right_answer = []
        while self.wait_check_select_blank_page():
            for x in range(3):
                game_container = self.select_blank_container_no_index()
                self.commit_btn_judge()
                if x == 0:
                    bank_id = self.bank_id()
                    bank_data_info = self.handle.get_multi_bank_answer(bank_id)
                    right_answer = [x['answer'] for x in bank_data_info]
                    if self.wait_check_hint_word_page():
                        print('提示单词：', self.hint_word(game_container))
                        print(self.blank_article(game_container))
                mine_answer = self.select_blank_do_process(game_container, x, right_answer=right_answer)
                print('我的答案：', mine_answer)
                self.select_blank_result_operate(mine_answer, game_container)
                self.commit_btn().click()
                time.sleep(2)
                if x != 2:
                    if not self.wait_check_select_blank_page():
                        self.base_assert.except_error('页面存在做错单词， 点击提交后未重新开始游戏')
                else:
                    if self.wait_check_select_blank_page():
                        self.base_assert.except_error('已答对所有题， 点击提交后未提交成功')
        used_time = round(time.time()) - start_time
        return used_time

    @teststeps
    def select_word_blank_game_exam_operate(self, do_type, wrong_id_list, check_answer, result_index):
        """选词填空"""
        if do_type != 2:
            bank_id = self.bank_id()
            game_container = self.select_blank_container_no_index()
            if do_type == 0:
                wrong_id_list.append(bank_id)
                print(self.blank_article(game_container))
            bank_data_info = self.handle.get_multi_bank_answer(bank_id)
            right_answer = [x['answer'] for x in bank_data_info]
            print('正确答案列表：', right_answer)
            if do_type:
                mine_answer = self.select_blank_do_process(game_container, fq=2, right_answer=right_answer)
            else:
                mine_answer = self.select_blank_do_process(game_container, fq=3, right_answer=right_answer)
        else:
            mine_answer = check_answer
            game_container = self.select_blank_container_with_index(result_index)
            result_index_content = self.get_result_index_content(game_container)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            else:
                if '未作答' not in result_index_content:
                    self.base_assert.except_error('本题未作答， 结果页题标未显示未作答')
            self.select_blank_result_operate(mine_answer, game_container)
        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer















