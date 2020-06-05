#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/5 13:25
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class ClozeText(GameCommonElePage):
    @teststep
    def wait_check_cloze_page(self):
        """完型填空页面检查点"""
        locator = (By.CSS_SELECTOR, '.wxtk-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def cloze_container_no_index(self):
        """完形填空父级容器元素"""
        ele = self.driver.find_element_by_css_selector('.wxtk-container')
        return ele

    @teststep
    def cloze_container_with_index(self, index):
        """完形填空父级容器元素"""
        ele = self.driver.find_element_by_css_selector('div[class ~="wxtk-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def cloze_text(self, container_ele):
        """完形填空文章"""
        ele = container_ele.find_element_by_css_selector('.article-wrap .article')
        return ele.text

    @teststep
    def quest_list(self, container_ele):
        ele = container_ele.find_elements_by_css_selector('.list li')
        return ele

    @teststep
    def question(self, ques_ele):
        """完形填空问题"""
        ele = ques_ele.find_element_by_css_selector('.title')
        return ele.text

    @teststep
    def options(self, ques_ele):
        """完形填空选项"""
        ele = ques_ele.find_elements_by_css_selector('.text')
        return ele

    @teststep
    def opt_letter(self, ques_ele):
        """完形填空选项字母"""
        ele = ques_ele.find_elements_by_css_selector('.letter')
        return ele

    @teststep
    def article_blank_wrap(self, container_ele):
        """文章"""
        ele = container_ele.find_elements_by_css_selector('.content .blank-wrap')
        return ele

    @teststep
    def article_result_mine_answer(self, blank_wrap):
        """完形填空页面我的答案"""
        ele = blank_wrap.find_element_by_css_selector('.blank-result span:not([style $="display: none;"]):not([class $="bracketed"])')
        return ele.text

    @teststep
    def cloze_select_opt_operate(self, ques_ele, do_right=False, right_answer=None):
        """完形填空选择选项操作"""
        select_answer = ()
        if do_right:
            for i, x in enumerate(self.opt_letter(ques_ele)):
                if x.text.lower() == right_answer:
                    select_opt_text = self.options(ques_ele)[i].text
                    select_answer = (x.text, select_opt_text)
                    x.click()
                    time.sleep(0.5)
                    break
        else:
            for i, x in enumerate(self.opt_letter(ques_ele)):
                if x.text.lower() != right_answer:
                    select_opt_text = self.options(ques_ele)[i].text
                    select_answer = (x.text, select_opt_text)
                    x.click()
                    time.sleep(0.5)
                    break
        return select_answer

    @teststeps
    def cloze_result_check_operate(self, mine_answer, fq, game_type=0, game_container=None):
        """完形填空结果校验处理
            :param game_container 题目容器元素
            :param mine_answer 我的答案
            :param fq 做题轮次
            :param game_type 0：阅读理解 1：完形填空
        """
        print('======= 提交后结果校验 ======== \n')
        for i, mine_ans in enumerate(mine_answer):
            mine_ans_text = mine_ans[1]
            mine_ans_letter = mine_ans[0]
            print('我的答案：', mine_ans_text)
            ques_ele = self.quest_list(game_container)[i]
            print('问题：', self.question(ques_ele))
            ques_letters = self.opt_letter(ques_ele)
            if game_type:
                article_blank_warp = self.article_blank_wrap(game_container)[i]
                article_mine_answer = self.article_result_mine_answer(article_blank_warp)
                print('结果页我的答案：', article_mine_answer)
                if mine_ans_text != article_mine_answer.strip():
                    self.base_assert.except_error('结果页面我的答案与选择的答案不一致')
            for letter in ques_letters:
                if letter.text == mine_ans_letter:
                    if (fq == 1 and i in [0, 1]) or fq == 2:
                        if 'success' not in letter.get_attribute('class'):
                            self.base_assert.except_error('选项正确， 但是结果页面选项字母未标识为正确 ' + mine_ans_text)
                    else:
                        if 'error' not in letter.get_attribute('class'):
                            self.base_assert.except_error('选项错误， 但是结果页面选项字母未标识为错误 ' + mine_ans_text)
            print('-'*30, '\n')

    @teststeps
    def cloze_text_game_operate(self):
        """完型填空游戏过程"""
        start_time = round(time.time())
        right_answer = []
        while self.wait_check_cloze_page():
            for x in range(3):
                mine_answer = []
                game_container = self.cloze_container_no_index()
                self.commit_btn_judge()
                if x == 0:
                    print(self.cloze_text(game_container), '\n')
                    bank_id = self.bank_id()
                    bank_data_info = self.handle.get_multi_bank_answer(bank_id)
                    right_answer = [(x['answer'], x[x['answer']]) for x in bank_data_info]
                ques_list = self.quest_list(game_container)
                for i, y in enumerate(ques_list):
                    question = self.question(y)
                    print('问题：', question)
                    print('正确答案：', right_answer[i])
                    if (x == 1 and i in [0, 1]) or x == 2:
                        select_answer = self.cloze_select_opt_operate(y, do_right=True, right_answer=right_answer[i][0])
                    else:
                        select_answer = self.cloze_select_opt_operate(y, right_answer=right_answer[i][0])
                    mine_answer.append(select_answer)
                    print('我的答案：', select_answer, '\n')
                self.commit_btn_judge(status=True)
                self.commit_btn().click()
                time.sleep(1)
                self.cloze_result_check_operate(mine_answer, fq=x, game_type=1, game_container=self.cloze_container_no_index())
                self.commit_btn().click()
                time.sleep(2)
                if x != 2:
                    if not self.wait_check_cloze_page():
                        self.base_assert.except_error('页面存在错题， 点击提交后未重新开始游戏')
                else:
                    if self.wait_check_cloze_page():
                        self.base_assert.except_error('已做全对， 点击提交未提交成功')
                print('-'*30, '\n')
        used_time = round(time.time()) - start_time
        return used_time

    @teststeps
    def cloze_exam_operate(self, do_type, wrong_id_list, check_answer, result_index, do_count):
        """完形填空试卷过程处理"""
        mine_answer = []
        if do_type != 2:
            game_container = self.cloze_container_no_index()
            bank_id = self.bank_id()
            if do_type == 0:
                wrong_id_list.append(bank_id)
                print(self.cloze_text(game_container))

            bank_data_info = self.handle.get_multi_bank_answer(bank_id)
            right_answer = [(x['answer'], x[x['answer']]) for x in bank_data_info]
            ques_list = self.quest_list(game_container)
            for i, y in enumerate(ques_list):
                question = self.question(y)
                print('问题：', question)
                print('正确答案：', right_answer[i])
                if do_type:
                    select_ans = self.cloze_select_opt_operate(y, do_right=True, right_answer=right_answer[i][0])
                else:
                    select_ans = self.cloze_select_opt_operate(y, right_answer=right_answer[i][0])
                print('我的答案：', select_ans)
                mine_answer.append(select_ans)
                print('-'*30, '\n')
        else:
            mine_answer = check_answer
            game_container = self.cloze_container_with_index(result_index)
            result_index_content = self.get_result_index_content(game_container)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            else:
                if '未作答' not in result_index_content:
                    self.base_assert.except_error('本题未作答， 结果页题标未显示未作答')

            if do_count == 1:
                fq = 3 if int(result_index) in range(3) else 2
            else:
                fq = 2
            self.cloze_result_check_operate(check_answer, fq=fq, game_type=1, game_container=game_container)

        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer






