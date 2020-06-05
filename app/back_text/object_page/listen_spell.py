#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/9 15:32
# -----------------------------------------
import random
import string
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class ListenSpell(GameCommonElePage):
    @teststep
    def wait_check_listen_spell_page(self):
        """单词听写页面检查点"""
        locator = (By.CSS_SELECTOR, '.dctx-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def listen_spell_container(self, index=0):
        """结果页父级容器元素"""
        ele = self.driver.find_elements_by_css_selector('.dctx-container')
        return ele[index]

    @teststep
    def input_text_wrap(self, container_ele):
        """听写输入栏"""
        ele = container_ele.find_element_by_css_selector('.main .text-input')
        return ele

    @teststep
    def right_answer(self, container_ele):
        """正确答案"""
        ele = container_ele.find_element_by_css_selector('.word')
        return ele.text

    @teststep
    def word_voice_btn(self, container_ele):
        """结果页单词喇叭"""
        ele = container_ele.find_element_by_css_selector('.main .text .speaker')
        return ele

    @teststep
    def listen_spell_process(self, game_container, do_right=False, right_answer=None):
        """听写单词做对错过程"""
        if do_right:
            self.input_text_wrap(game_container).send_keys(right_answer)
        else:
            random_str = ''.join(random.sample(string.ascii_lowercase, 3))
            self.input_text_wrap(game_container).send_keys(random_str)

    @teststeps
    def listen_spell_operate(self):
        """单词听写过程"""
        print('======== 单词听写 ========\n')
        start_time = round(time.time())
        bank_list = []
        right_bank = []
        wrong_bank_id, index, wrong_count = 0, 0, 0
        bank_count = self.bank_count()
        while self.wait_check_container_page():
            is_right = False
            self.commit_btn_judge()
            game_container = self.listen_spell_container()
            bank_id = self.bank_id()
            if bank_id in right_bank:
                print('本题已做对，却再次出现')
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info['word']
            print('正确答案：', right_answer)
            if index == 0:
                wrong_bank_id = bank_id

            if bank_id != wrong_bank_id or wrong_count >= 2:  # 单选做对
                self.listen_spell_process(game_container, do_right=True, right_answer=right_answer)
                is_right = True
            else:
                self.listen_spell_process(game_container)
                wrong_count += 1

            mine_answer = self.driver.execute_script('return document.getElementsByClassName("text-input")[0].value')
            print('我的答案：', mine_answer)
            bank_list.append(bank_id)
            if not is_right:
                self.commit_btn_judge(True)
                self.commit_btn().click()
                time.sleep(1)
                print('页面正确答案：', self.right_answer(game_container))
            self.commit_btn().click()
            index += 1
            time.sleep(2)
            print('-' * 20, '\n')
        used_time = round(time.time()) - start_time
        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        return used_time

    @teststeps
    def listen_spell_exam_operate(self, do_type, wrong_id_list, check_answer, result_index):
        """单词听写试卷过程"""
        if do_type != 2:
            bank_id = self.bank_id()
            game_container = self.listen_spell_container()
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info['word']
            print('正确答案：', right_answer)

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                self.listen_spell_process(game_container, do_right=True, right_answer=right_answer)
            else:
                self.listen_spell_process(game_container)
                wrong_id_list.append(bank_id)
            mine_answer = self.driver.execute_script('return document.getElementsByClassName("text-input")[0].value')
        else:
            mine_answer = check_answer
            game_container = self.listen_spell_container(result_index)
            print('正确答案：', self.right_answer(game_container))
            self.word_voice_btn(game_container).click()
            time.sleep(0.5)
            page_result_answer = self.driver.execute_script('return document.getElementsByClassName("dctx-container")[{}].'
                                                            'getElementsByClassName("text-input")[0].value'.format(result_index))
            print('页面我的答案：', page_result_answer)
            if check_answer:
                if page_result_answer != check_answer:
                    self.base_assert.except_error("页面显示答案与我的答案不一致 页面为%s， 我的答案为%s" % (page_result_answer, check_answer))
        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer