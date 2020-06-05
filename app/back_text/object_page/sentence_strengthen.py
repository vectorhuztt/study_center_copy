#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/21 15:32
# -----------------------------------------
import random
import string
import time

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class SentenceStrengthen(GameCommonElePage):
    # ===================== 强化炼句  ==========================
    @teststep
    def wait_check_sentence_strengthen_page(self):
        """"""
        locator = (By.CSS_SELECTOR, 'qhlj-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def sentence_strengthen_container_no_index(self):
        """强化炼句父级容器元素"""
        ele = self.driver.find_element_by_css_selector('.qhlj-container')
        return ele

    @teststep
    def sentence_strengthen_container_with_index(self, index):
        ele = self.driver.find_element_by_css_selector('div[class ~="qhlj-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def sentence_explain(self, container_ele):
        """句子解释"""
        ele = container_ele.find_element_by_class_name('explain')
        return ele.text

    @teststep
    def begin_or_final_sentence(self, container_ele):
        """整体的句子"""
        ele = container_ele.find_elements_by_css_selector('.custom-init span span')
        return [x.text.strip() for x in ele]

    @teststep
    def sentence_spell_input_wraps(self, container_ele):
        """句子强化输入栏"""
        ele = container_ele.find_elements_by_css_selector('.txt')
        return ele


    @teststep
    def right_answer(self, container_ele):
        """强化炼句的正确答案"""
        ele = container_ele.find_element_by_css_selector('.right-answer')
        return ele.text.split('：')[1][:-1]

    @teststep
    def result_page_answer(self, container_ele):
        """结果页我的答案"""
        ele = container_ele.find_elements_by_css_selector('.custom-init span span')
        return ' '.join([x.text for x in ele if x.text != ''])


    @teststeps
    def sentence_strengthen_do_wrong_operate(self, game_container,  bank_list):
        for i, y in enumerate(self.sentence_spell_input_wraps(game_container)):
            random_str = ''.join(random.sample(string.ascii_lowercase, random.randint(3, 5)))
            y.click()
            if len(bank_list) == 0 and i == 0:  # 漏做一个空，验证是否可以提交
                y.send_keys(" " + Keys.ENTER)
            else:  # 随机输入字母
                y.send_keys(random_str + Keys.ENTER)
            time.sleep(0.5)
        time.sleep(2)

        if len(bank_list) == 0:
            random_str = ''.join(random.sample(string.ascii_lowercase, random.randint(3, 5)))
            first_input = self.sentence_spell_input_wraps(game_container)[0]
            first_input.click()
            first_input.send_keys(random_str + Keys.ENTER)


    @teststeps
    def sentence_strength_game_process(self):
        """强化炼句游戏过程"""
        print('======== 强化炼句 ========\n')
        start_time = round(time.time())
        right_bank, bank_list  = [], []
        index, wrong_count, wrong_bank_id = 0, 0, 0
        bank_count = self.bank_count()
        while self.wait_check_container_page():
            mine_answer = 0
            game_container = self.sentence_strengthen_container_no_index()
            self.commit_btn_judge()
            explain = self.sentence_explain(game_container)
            print('题目：', explain)
            bank_id = self.bank_id()
            before_sentence = self.begin_or_final_sentence(game_container)
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_sentence = [x['word'] for x in bank_data_info['fix']]
            input_answer = [x for x, y in zip(right_sentence, before_sentence) if x != y]
            print('填写之前的句子：', ' '.join(before_sentence))
            print('应填单词：', input_answer)

            if bank_id in right_bank:
                print('★★★ 此题已做正确， 但是再次出现')

            if index == 0:
                wrong_bank_id = bank_id

            if bank_id != wrong_bank_id or wrong_count >= 2:       # 题目做对过程
                input_wraps = self.sentence_spell_input_wraps(game_container)
                for i, y in enumerate(input_wraps):
                    y.click()
                    y.send_keys(input_answer[i])
                    if i == len(input_wraps) - 1:
                        mine_answer = ' '.join(self.begin_or_final_sentence(game_container))
                right_bank.append(bank_id)
                do_right = True
                time.sleep(2)
                if self.wait_check_sentence_strengthen_page():
                    if self.bank_id() == bank_id:
                        self.base_assert.except_error("答题成功以后， 停顿两秒时间未自动跳转到下一题")
            else:
                self.sentence_strengthen_do_wrong_operate(game_container, bank_list)
                time.sleep(1)
                mine_answer = ' '.join(self.begin_or_final_sentence(game_container))
                wrong_count += 1
                do_right = False
            print('我的答案：', mine_answer)
            index += 1
            bank_list.append(bank_id)
            if not do_right:
                print('页面正确答案：', self.right_answer(game_container))
                self.commit_btn().click()
                time.sleep(2)
            print('-' * 30, '\n')
        time.sleep(3)
        print(bank_list)
        used_time = round(time.time()) - start_time
        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        return used_time

    @teststeps
    def sentence_strength_exam_process(self, do_type, wrong_id_list, check_answer, result_index):
        """强化炼句试卷过程"""
        if do_type != 2:
            game_container = self.sentence_strengthen_container_no_index()
            explain = self.sentence_explain(game_container)
            print('题目：', explain)
            bank_id = self.bank_id()
            print('题目id：', bank_id)
            before_sentence = self.begin_or_final_sentence(game_container)
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_sentence = [x['word'] for x in bank_data_info['fix']]
            input_answer = [x for x, y in zip(right_sentence, before_sentence) if x != y]
            print('填写之前的句子：', ' '.join(before_sentence))
            print('正确答案', ' '.join(right_sentence))
            print('需填写单词：', input_answer)

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                for i, y in enumerate(self.sentence_spell_input_wraps(game_container)):
                    y.click()
                    y.send_keys(input_answer[i])
                    time.sleep(0.5)
            else:
                for i, y in enumerate(self.sentence_spell_input_wraps(game_container)):
                    y.click()
                    y.send_keys(''.join(random.sample(string.ascii_lowercase, 3)))
                    time.sleep(0.5)
                wrong_id_list.append(bank_id)
            mine_answer = ' '.join(self.begin_or_final_sentence(game_container))
        else:
            mine_answer = check_answer
            game_container = self.sentence_strengthen_container_with_index(result_index)
            result_index_content = self.get_result_index_content(game_container)
            result_explain = self.sentence_explain(game_container)
            result_page_answer = self.result_page_answer(game_container)
            result_right_answer = self.right_answer(game_container)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            print('句子解释：', result_explain)
            print('页面我的答案：', result_page_answer)
            print('结果页正确答案：',result_right_answer)
            if check_answer != result_page_answer:
                self.base_assert.except_error("页面答案与我的答案不一致 " + check_answer)

        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer