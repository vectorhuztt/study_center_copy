#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/9 16:25
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps
from utils.ele_attr_check import EleAttrCheck


class WordChoice(GameCommonElePage):

    @teststep
    def wait_check_word_choice_page(self):
        """词汇选择页面检查点"""
        locator = (By.CSS_SELECTOR, '.chxz-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def word_choice_container_no_index(self):
        """词汇选择父级容器元素 不带index"""
        ele = self.driver.find_element_by_css_selector('.chxz-container')
        return ele

    @teststep
    def word_choice_container_with_index(self, index):
        """词汇选择父级容器元素 带index"""
        ele = self.driver.find_element_by_css_selector('div[class ~="chxz-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def ques_title(self, container_ele):
        """单词解释"""
        ele = container_ele.find_element_by_css_selector('.title')
        return ele.text.strip()

    @teststep
    def options(self, container_ele):
        """词汇选项"""
        ele = container_ele.find_elements_by_css_selector('.options li')
        return ele

    @teststep
    def listen_select_answer(self, container_ele):
        """听音选词的答案"""
        ele = container_ele.find_element_by_css_selector(".font-xlarge")
        return ele.text

    @teststep
    def get_result_index(self, container_ele):
        """获取结果页题号文本"""
        ele = container_ele.find_element_by_xpath("//preceding-sibling::div[@class='title']")
        return ele.text


    @teststeps
    def word_choice_game_operate(self):
        print('======== 词汇选择 ========\n')
        start_time = round(time.time())
        bank_list = []
        right_bank = []
        wrong_bank_id, index, wrong_count = 0, 0, 0
        bank_count = self.bank_count()
        while self.wait_check_container_page():
            self.commit_btn_judge()
            bank_id = self.bank_id()
            game_container = self.word_choice_container_no_index()
            game_mode = game_container.get_attribute('mode')
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            if bank_id in right_bank:
                print('本题已做对，却再次出现')

            if game_mode == '1':
                right_answer = bank_data_info['explain'].encode('utf-8').decode('utf-8')
            else:
                right_answer = bank_data_info['word']

            print('解释：', self.ques_title(game_container))
            print('正确答案：', right_answer)

            if index == 0:
                wrong_bank_id = bank_id

            if bank_id != wrong_bank_id or wrong_count >= 2:  # 单选做对
                for x in self.options(game_container):
                    if x.text.strip() == right_answer:
                        print('我选择的：', x.text)
                        x.click()
                        break
            else:
                for x in self.options(game_container):
                    if x.text.strip() != right_answer:
                        print('我选择的：', x.text)
                        x.click()
                        break
                wrong_count += 1

            bank_list.append(bank_id)
            index += 1
            self.commit_btn_judge(True)
            self.commit_btn().click()
            time.sleep(1)
            print('-' * 20, '\n')
        used_time = round(time.time()) - start_time
        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        return used_time

    @teststeps
    def word_choice_exam_operate(self, do_type, wrong_id_list, check_answer, result_index):
        """词汇选择游戏试卷处理过程
            :param do_type:  做题形式 0:做错 1:做对 2:试卷结果核查
            :param wrong_id_list: 错题列表
            :param check_answer:  我的答案
            :param  result_index: 题目顺序
        """
        mine_answer = 0
        if do_type != 2:
            game_container = self.word_choice_container_no_index()
            game_mode = game_container.get_attribute('mode')
            bank_id = self.bank_id()
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            if game_mode in ['1', '4']:
                right_answer = bank_data_info['explain'].encode('utf-8').decode('utf-8')
            else:
                right_answer = bank_data_info['word']

            if game_mode in ['1', '2']:
                print('问题：', self.ques_title(game_container))
            else:
                print("问题：", right_answer)
            print('正确答案：', right_answer)

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                for x in self.options(game_container):
                    if right_answer in x.text.strip():
                        mine_answer = x.text
                        x.click()
                        break
            else:
                for x in self.options(game_container):
                    if right_answer not in x.text.strip():
                        mine_answer = x.text
                        x.click()
                        break
                wrong_id_list.append(bank_id)
        else:
            mine_answer = check_answer
            game_container = self.word_choice_container_with_index(result_index)
            result_question = self.ques_title(game_container)
            result_index_content = self.get_result_index(game_container)
            print('问题：', result_question)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")

            for x in self.options(game_container):
                if x.text == check_answer:
                    if not (EleAttrCheck().check_word_is_in_class('success', x) or \
                            EleAttrCheck().check_word_is_in_class('danger', x)):
                        self.base_assert.except_error("选择选项在结果页面显示未被选中 " + str(result_index))
        print('我的答案：', mine_answer)
        print("-"*30, '\n')
        return mine_answer





