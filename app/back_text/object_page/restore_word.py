#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/9 17:31
# -----------------------------------------
import random
import string
import time

from pykeyboard import PyKeyboard
from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class RestoreWord(GameCommonElePage):

    @teststep
    def wait_check_word_restore_page(self):
        """还原单词页面检查点"""
        locator = (By.CSS_SELECTOR, '.hydc-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def word_restore_container_no_index(self):
        ele = self.driver.find_element_by_css_selector('.hydc-container')
        return ele

    @teststep
    def word_restore_container_with_index(self, index):
        ele = self.driver.find_element_by_css_selector('div[class ~="hydc-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def explain(self, container_ele):
        """单词解释"""
        ele = container_ele.find_element_by_css_selector('.main .explain')
        return ele.text

    @teststep
    def right_answer(self, container_ele):
        """结果页还原单词答案"""
        ele = container_ele.find_element_by_css_selector('.main .answer')
        return ele.text

    @teststep
    def finish_restored_word(self, container_ele):
        """结果页还原完的答案"""
        ele = container_ele.find_elements_by_css_selector('.main .word-wrap li')
        return ''.join([x.text.strip() for x in ele])

    @teststep
    def bottom_wait_words(self, container_ele):
        """获取下方待选字母文本"""
        wait_words = container_ele.find_elements_by_css_selector('.main .answer-wrap li:not([class="hide"])')
        return wait_words

    @teststep
    def input_warp(self, container_ele):
        """还原单词输入栏"""
        ele = container_ele.find_elements_by_css_selector('.main .word-wrap li')
        return ele

    @teststep
    def restore_do_right_operate(self, game_container, answer_word, alpha_index):
        """还原单词正确操作"""
        index = alpha_index[0]
        wait_select_words = self.bottom_wait_words(game_container)
        for x in range(len(wait_select_words)):
            wait_alpha = wait_select_words[x].text.strip()
            alpha_length = len(wait_alpha)
            if index + alpha_length >= len(answer_word) - 1:
                answer_word += ' ' * alpha_length
            word_part = answer_word[index:index + alpha_length].strip()
            if wait_alpha and wait_alpha == word_part:
                wait_select_words[x].click()
                time.sleep(1)
                alpha_index[0] += alpha_length
                break

    @teststep
    def restore_do_wrong_operate(self, game_container,  answer_word):
        """还原单词错误操作"""
        for x in self.bottom_wait_words(game_container):
            if x.text != answer_word[0]:
                x.click()
                time.sleep(1)
                break

        for y in self.bottom_wait_words(game_container):
            y.click()
            time.sleep(0.5)

    @teststep
    def send_keys_replace_click_operate(self, game_container, answer_word):
        """输入单词替代点击操作"""
        random_str = random.choice(string.ascii_letters)
        print('随机字母：', random_str)
        key = PyKeyboard()
        key.type_string(random_str)
        time.sleep(1)
        if random_str.lower() in self.finish_restored_word(game_container):
            self.base_assert.except_error('键入非此单词中的字母， 页面显示可键入')
            bottom_words = self.bottom_wait_words(game_container)
            bottom_word_text = ''.join([x.text.lower().strip() for x in bottom_words])
            if random_str.lower() in bottom_word_text:
                self.base_assert.except_error('页面显示已经成功键入字母，但是下方待点字母依然存在此字母')
            self.input_warp(game_container)[0].click()
            if random_str.lower() in self.finish_restored_word(game_container):
                self.base_assert.except_error('点击已经键入的字母，字母未撤回')

        count = 0
        for x in self.bottom_wait_words(game_container):
            if x.text.strip() != answer_word[0]:
                PyKeyboard().type_string(x.text.strip())
                time.sleep(0.5)
                if x.text.strip() not in self.finish_restored_word(game_container):
                    self.base_assert.except_error('键入此单词中的字母， 页面显示未键入')
                    bottom_words = self.bottom_wait_words(game_container)
                    bottom_word_text = ''.join([x.text.lower().strip() for x in bottom_words])
                    if random_str.lower() in bottom_word_text:
                        self.base_assert.except_error('页面显示已经成功键入字母，但是下方待点字母依然存在此字母')
                else:
                    self.input_warp(game_container)[0].click()
                    time.sleep(1)
                    if random_str.lower() in self.finish_restored_word(game_container):
                        self.base_assert.except_error('点击已经键入的字母，字母未撤回')
                PyKeyboard().type_string(x.text.strip())
                time.sleep(0.5)
                count += 1
                break
        for x in self.bottom_wait_words(game_container):
            PyKeyboard().type_string(x.text.strip())
            time.sleep(0.5)
            count += 1


    @teststeps
    def word_restore_operate(self):
        """还原单词操作"""
        print('======== 还原单词 ========\n')
        start_time = round(time.time())
        bank_list = []
        right_bank = []
        wrong_bank_id, index, wrong_count = 0, 0, 0
        bank_count = self.bank_count()

        while self.wait_check_container_page():
            self.commit_btn_judge()
            game_container = self.word_restore_container_no_index()
            print("解释：", self.explain(game_container))
            bottom_words = self.bottom_wait_words(game_container)
            bottom_word_text = ''.join([x.text.lower().strip() for x in bottom_words])
            print('还原前单词：', bottom_word_text)
            bank_id = self.bank_id()
            if bank_id in right_bank:
                print('本题已做对，却再次出现')
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info['word']
            print('正确答案：', right_answer)
            if index == 0:
                wrong_bank_id = bank_id

            if bank_id != wrong_bank_id or wrong_count >= 2:  # 单选做对
                alpha_index = [0]
                while right_answer.lower() != self.finish_restored_word(game_container).lower():
                    self.restore_do_right_operate(game_container, right_answer, alpha_index)
            else:
                if index == 0:
                    self.send_keys_replace_click_operate(game_container, right_answer)
                else:
                    self.restore_do_wrong_operate(game_container, right_answer)
                wrong_count += 1
            print('我的答案：', self.finish_restored_word(game_container))
            bank_list.append(bank_id)
            self.commit_btn_judge(True)
            self.commit_btn().click()
            index += 1
            self.commit_btn().click()
            time.sleep(1)
            print('-' * 20, '\n')
        used_time = round(time.time()) - start_time
        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        return used_time

    @teststeps
    def word_restore_exam_operate(self, do_type, wrong_id_list, check_answer, result_index):
        """还原单词游戏处理"""
        if do_type != 2:
            game_container = self.word_restore_container_no_index()
            print("解释：", self.explain(game_container))
            bottom_words = self.bottom_wait_words(game_container)
            bottom_word_text = ''.join([x.text.lower().strip() for x in bottom_words])
            print('还原前单词：', bottom_word_text)
            bank_id = self.bank_id()
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info['word']
            print('正确答案：', right_answer)

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                alpha_index = [0]
                while right_answer.lower() != self.finish_restored_word(game_container).lower():
                    self.restore_do_right_operate(game_container, right_answer, alpha_index)
            else:
                self.restore_do_wrong_operate(game_container, right_answer)
                wrong_id_list.append(bank_id)
            mine_answer = self.finish_restored_word(game_container)
        else:
            mine_answer = check_answer
            game_container = self.word_restore_container_with_index(result_index)
            print('解释：', self.explain(game_container))
            print('正确答案：', self.right_answer(game_container))

            page_result_answer = self.finish_restored_word(game_container)
            print('页面已还原答案：', page_result_answer)

            if check_answer:
                if self.finish_restored_word(game_container) != check_answer:
                    self.base_assert.except_error("页面显示答案与我的答案不一致 页面为%s， 我的答案为%s" %(page_result_answer, check_answer))
        print('我的答案：', mine_answer)
        print('-'*30, '\n')
        return mine_answer


