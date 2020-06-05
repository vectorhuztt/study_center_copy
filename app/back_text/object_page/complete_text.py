#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/21 15:40
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class CompleteText(GameCommonElePage):

    @teststep
    def wait_check_complete_text_page(self):
        """补全文章页面检查点"""
        locator = (By.CSS_SELECTOR, '.wrap-article .options')
        return self.get_wait_check_page_result(locator)

    @teststep
    def complete_article_container_no_index(self):
        """游戏页 - 补全文章父级容器元素"""
        ele = self.driver.find_element_by_css_selector('.bqwz-container')
        return ele

    @teststep
    def complete_article_container_with_index(self, index):
        """试卷详情 -补全文章父级容器元素 """
        ele = self.driver.find_element_by_css_selector('div[class ~="bqwz-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def complete_article(self, container_ele):
        """补全文章的文本内容"""
        ele = container_ele.find_element_by_css_selector('.article')
        return ele.text

    @teststep
    def no_selected_opt_list(self, container_ele):
        ele = container_ele.find_elements_by_css_selector('.options  .op-btn:not([class $="selected"])')
        return ele

    @teststep
    def opt_text(self, opt_ele):
        """选项内容"""
        ele = opt_ele.find_element_by_css_selector('.op')
        return ele.text.strip()

    @teststep
    def complete_warp(self, container_ele):
        """输入栏答案"""
        ele = container_ele.find_elements_by_css_selector('.blank .underline')
        return ele

    @teststep
    def result_mine_answer(self, container_ele):
        """结果页答案"""
        ele = container_ele.find_elements_by_css_selector('.result .blank .underline')
        result_answer_list = []
        for x in ele:
            if '(' not in x.text:
                result_answer_list.append(x.text)
            else:
                result_answer_list.append(x.text.split('(')[0])
        print('结果页我的答案：', result_answer_list)
        return result_answer_list

    @teststep
    def complete_article_select_opt_operate(self, game_container, do_right=False, right_answer=None):
        """补全文章选择选项过程"""
        mine_answer = []
        if do_right:
            for i in range(len(right_answer)):
                for opt in self.no_selected_opt_list(game_container):
                    opt_text = self.opt_text(opt)
                    if opt_text == right_answer[i]:
                        mine_answer.append(opt_text)
                        opt.click()
                        time.sleep(0.5)
                        break
        else:
            for i in range(len(right_answer)):
                if i == 0:
                    for x in self.no_selected_opt_list(game_container):
                        opt_text = self.opt_text(x)
                        if opt_text != right_answer[0]:
                            mine_answer.append(opt_text)
                            x.click()
                            time.sleep(5)
                            break
                else:
                    for opt in self.no_selected_opt_list(game_container):
                        mine_answer.append(self.opt_text(opt))
                        opt.click()
                        time.sleep(1)
        return mine_answer

    @teststep
    def complete_article_result_page_operate(self, fq, game_container, mine_answer):
        print('====== 补全文章结果校验 =======\n')
        for i, ans in enumerate(self.result_mine_answer(game_container)):
            if ans != mine_answer[i]:
                self.base_assert.except_error('结果页我的答案与我输入的不一致 ' + ans)

        for x in self.no_selected_opt_list(game_container):
            if fq == 1:
                if 'iswrong' not in x.get_attribute('class'):
                    self.base_assert.except_error('本题已选错，但是结果页显示做对' + self.opt_text(x))
            else:
                if 'iswrong' in x.get_attribute('class'):
                    self.base_assert.except_error('本题已选对，但是结果页显示做错' + self.opt_text(x))

    @teststeps
    def complete_text_game_process(self):
        """补全文章游戏过程"""
        print('======== 补全文章 ========\n')
        start_time = round(time.time())
        right_answer = []
        while self.wait_check_complete_text_page():
            for x in range(2):
                game_container = self.complete_article_container_no_index()
                self.commit_btn_judge()
                if x == 0:
                    print(self.complete_article(game_container))
                    bank_id = self.bank_id()
                    bank_data_info = self.handle.get_multi_bank_answer(bank_id)
                    right_answer = [x['answer'] for x in bank_data_info]
                    mine_answer = self.complete_article_select_opt_operate(game_container, right_answer=right_answer)
                else:
                    mine_answer = self.complete_article_select_opt_operate(game_container, do_right=True, right_answer=right_answer)
                print('我的答案：', mine_answer)
                self.commit_btn_judge(status=True)
                self.commit_btn().click()
                time.sleep(1)
                self.complete_article_result_page_operate(x+1, game_container, mine_answer)
                self.commit_btn().click()
                if x != 1:
                    if not self.wait_check_complete_text_page():
                        self.base_assert.except_error('文章中存在选错内容， 点击提交后未重新开始游戏')
                else:
                    if self.wait_check_complete_text_page():
                        self.base_assert.except_error('题目已全部做对， 点击提交后未提交成功')
            used_time = round(time.time()) - start_time
            return used_time


    @teststeps
    def complete_article_exam_operate(self, do_type, wrong_id_list, check_answer, result_index, do_count):
        """补全文章试卷"""
        if do_type != 2:
            game_container = self.complete_article_container_no_index()
            bank_id = self.bank_id()
            bank_data_info = self.handle.get_multi_bank_answer(bank_id)
            right_answer = [x['answer'] for x in bank_data_info]
            if do_type == 0:
                wrong_id_list.append(bank_id)
                print(self.complete_article(game_container))
                mine_answer = self.complete_article_select_opt_operate(game_container, right_answer=right_answer)
            else:
                mine_answer = self.complete_article_select_opt_operate(game_container, do_right=True, right_answer=right_answer)
        else:
            mine_answer = check_answer
            game_container = self.complete_article_container_with_index(result_index)
            result_index_content = self.get_result_index_content(game_container)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            else:
                if '未作答' not in result_index_content:
                    self.base_assert.except_error('本题未作答， 结果页题标未显示未作答')
            self.complete_article_result_page_operate(do_count, game_container, mine_answer)

        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer