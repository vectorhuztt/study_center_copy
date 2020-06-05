#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/21 15:29
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class SentenceReform(GameCommonElePage):
    # =====================  句型转换 ==============================
    @teststep
    def wait_check_sentence_reform_page(self):
        """句型转换页面检查点"""
        locator = (By.CSS_SELECTOR, '.jxzh-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def sentence_reform_no_index(self):
        """句型转换父级容器元素 不带 index"""
        ele = self.driver.find_element_by_css_selector('.jxzh-container')
        return ele

    @teststep
    def sentence_reform_with_index(self, index):
        """句型转换父级容器元素 不带 index"""
        ele = self.driver.find_element_by_css_selector('div[class ~="jxzh-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def game_question(self, container_ele):
        """题目问题"""
        ele = container_ele.find_element_by_css_selector('.question')
        return ele.text

    @teststep
    def input_wrap(self, container_ele):
        """输入框"""
        ele = container_ele.find_elements_by_css_selector('.sentence-wrap li')
        return ele

    @teststep
    def sentence_reform_waiting_part(self, container_ele):
        """下方待点击的内容"""
        ele = container_ele.find_elements_by_css_selector('.answer-wrap li:not([class="hide"])')
        return ele

    @teststep
    def right_answer(self, container_ele):
        """正确答案"""
        ele = container_ele.find_element_by_css_selector('.answer')
        answer = ele.text.split('答案：')[1].split()
        return answer

    @teststep
    def mine_answer(self, container_ele):
        """结果页我的答案"""
        ele = container_ele.find_elements_by_css_selector('.sentence-wrap li span')
        return ' '.join([x.text.strip() for x in ele])


    @teststeps
    def sentence_reform_do_process(self, game_container, do_right=False, right_answer=None):
        """句型转换做多做错步骤"""
        if do_right:
            for j in right_answer:
                for part in self.sentence_reform_waiting_part(game_container):
                    if part.text.strip() == j:
                        part.click()
                        time.sleep(0.5)
                        break
        else:
            waiting_part = self.sentence_reform_waiting_part(game_container)
            for y in waiting_part:
                if y.text.strip() != right_answer[0]:
                    y.click()
                    time.sleep(0.5)
                    break

            count = 0
            while count < len(waiting_part) - 1:
                self.sentence_reform_waiting_part(game_container)[0].click()
                time.sleep(0.5)
                count += 1
            time.sleep(3)

    @teststeps
    def sentence_reform_game_process(self, is_exit=False):
        """句型转换游戏过程"""
        print('======== 句型转换 ========\n')
        start_time = round(time.time())
        right_bank, bank_list  = [], []
        index, wrong_count, wrong_bank_id = 0, 0, 0
        bank_count = self.bank_count()
        while self.wait_check_container_page():
            self.commit_btn_judge()
            game_container = self.sentence_reform_no_index()
            bank_id = self.bank_id()
            question = self.game_question(game_container)
            print('问题：', question)
            if bank_id in right_bank:
                print('★★★ 此题已做正确， 但是再次出现')
            if index == 0:
                wrong_bank_id = bank_id

            self.driver.execute_script("document.getElementsByClassName('answer')[0].style.display='block'")
            time.sleep(1)
            right_answer = self.right_answer(game_container)
            print("正确答案：", right_answer)

            if is_exit and index == 2:
                self.game_exit_btn().click()
                time.sleep(2)
                break

            if bank_id != wrong_bank_id or wrong_count >= 2:
                self.sentence_reform_do_process(game_container, do_right=True, right_answer=right_answer)
                right_bank.append(bank_id)
            else:
                self.sentence_reform_do_process(game_container, right_answer=right_answer)
                if wrong_count == 0:
                    self.clear_btn().click()
                    time.sleep(2)
                    if len([x for x in self.input_wrap(game_container) if x.text]):
                        print('★★★ 点击清空后, 填入栏未清空')
                    self.sentence_reform_do_process(game_container, right_answer=right_answer)
                wrong_count += 1

            index += 1
            bank_list.append(bank_id)
            time.sleep(1)
            mine_answer = self.mine_answer(game_container)
            print('我的答案：', mine_answer)

            self.commit_btn().click()
            time.sleep(1)
            self.commit_btn().click()
            time.sleep(1)
            print('-' * 20, '\n')

        print(bank_list)
        used_time = round(time.time()) - start_time
        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        return used_time


    @teststeps
    def sentence_reform_exam_process(self, do_type, wrong_id_list, check_answer, result_index):
        """句型转换试卷过程"""
        if do_type != 2:
            game_container = self.sentence_reform_no_index()
            question = self.game_question(game_container)
            bank_id = self.bank_id()
            print('问题：', question)
            self.driver.execute_script("document.getElementsByClassName('answer')[0].style.display='block'")
            time.sleep(1)
            right_answer = self.right_answer(game_container)
            print("正确答案：", right_answer)

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                self.sentence_reform_do_process(game_container, do_right=True, right_answer=right_answer)
            else:
                self.sentence_reform_do_process(game_container, right_answer=right_answer)
                wrong_id_list.append(bank_id)

            mine_answer = ' '.join([x.text for x in self.input_wrap(game_container)])
        else:
            mine_answer = check_answer
            game_container = self.sentence_reform_with_index(result_index)
            result_question = self.game_question(game_container)
            result_page_answer = self.mine_answer(game_container)
            result_right_answer = self.right_answer(game_container)

            if check_answer:
                if '未作答' in result_question:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            print('问题：', result_question)
            print('结果页我的答案：', result_page_answer)
            print("结果页正确答案：",result_right_answer)
            if check_answer != result_page_answer:
                self.base_assert.except_error("我的答案与页面答案不一致" + check_answer)

        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer