#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/10 9:58
# -----------------------------------------
import random
import string
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class WordSpell(GameCommonElePage):
    @teststep
    def wait_check_spell_word_page(self):
        """单词拼写页面检查点"""
        locator = (By.CSS_SELECTOR, '.dcpx-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def spell_container_no_index(self):
        """单词拼写父级容器元素"""
        ele = self.driver.find_element_by_css_selector('.dcpx-container')
        return ele

    @teststep
    def spell_container_with_index(self, index):
        """单词拼写父级容器元素"""
        ele = self.driver.find_element_by_css_selector('div[class ~="dcpx-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def explain(self, container_ele):
        """单词解释"""
        ele = container_ele.find_element_by_css_selector('.explain')
        return ele.text

    @teststep
    def normal_spell_input_wrap(self, container_ele):
        """单词拼写输入栏"""
        ele = container_ele.find_element_by_css_selector('.main .text-input')
        return ele

    @teststep
    def random_spell_input_warp(self, container_ele):
        """随机拼写输入栏"""
        ele = container_ele.find_elements_by_css_selector('.text-wrapper .letter-input')
        return ele

    @teststep
    def random_spell_final_word(self, container_ele):
        """随机拼写最终答案"""
        ele = container_ele.find_elements_by_css_selector('.main .text')
        mine_answer = []
        for x in ele:
            if x.text:
                mine_answer.append(x.text)
            else:
                input_text = x.find_element_by_css_selector('.letter-input').get_attribute('value')
                mine_answer.append(input_text)
        return ''.join(mine_answer)


    @teststep
    def normal_spell_mine_answer(self, container_ele):
        """结果页我的答案"""
        ele = container_ele.find_elements_by_css_selector('.user-answer .clearfix')
        return ''.join([x.text for x in ele])

    @teststep
    def right_answer(self, container_ele):
        """结果页正确答案"""
        ele = container_ele.find_element_by_css_selector('.answer')
        return ele.text

    @teststep
    def random_spell_show_words(self, container_ele):
        """展示的单词"""
        ele = container_ele.find_elements_by_css_selector('.text-wrapper .text')
        words = []
        for x in ele:
            if not x.text:
                words.append('_')
            else:
                words.append(x.text)
        return words


    @teststep
    def word_spell_do_process(self, game_container, game_mode, do_right=False, right_answer=None):
        """单词拼写游戏做题做对做做错过程
            :param right_answer: 正确答案
            :param do_right: 是否做对
            :param game_mode 单词拼写不同模式 1：随机拼写 2 默写
            :param game_container: 父级容器
        """
        mine_answer = 0
        if game_mode in ['1', '3']:
            input_warp = self.random_spell_input_warp(game_container)
            if do_right:
                for i in range(len(input_warp)):
                    input_warp[i].click()
                    input_warp[i].send_keys(right_answer[i])
                    time.sleep(0.5)
            else:
                input_words = []
                for x in range(len(input_warp)):
                    input_warp[x].click()
                    random_str = random.choice(string.ascii_letters)
                    input_words.append(random_str)
                    input_warp[x].send_keys(random_str)
                    time.sleep(0.5)
            mine_answer = self.random_spell_final_word(game_container)

        elif game_mode == '2':
            if do_right:
                self.normal_spell_input_wrap(game_container).send_keys(right_answer)
                mine_answer = right_answer
            else:
                random_str = ''.join(random.sample(string.ascii_lowercase, 3))
                mine_answer = random_str
                self.normal_spell_input_wrap(game_container).send_keys(random_str)
        return mine_answer

    @teststeps
    def word_spell_game_operate(self):
        """单词拼写游戏过程"""
        print('======== 单项拼写 ========\n')
        start_time = round(time.time())
        bank_list = []
        right_bank = []
        wrong_bank_id, index, wrong_count = 0, 0, 0
        bank_count = self.bank_count()

        while self.wait_check_spell_word_page():
            self.commit_btn_judge()
            bank_id = self.bank_id()
            if bank_id in right_bank:
                print('本题已做对，却再次出现')
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info['word']
            game_container = self.spell_container_no_index()
            game_mode = game_container.get_attribute('mode')
            print("解释：", self.explain(game_container))
            print('正确答案：', right_answer)
            if index == 0:
                wrong_bank_id = bank_id

            if game_mode in ['1', '3']:
                words = self.random_spell_show_words(game_container)
                print('待填写单词:', words)
                wait_spell_alpha = [right_answer[i] for i, alpha in enumerate(list(''.join(words))) if alpha == '_']
                print('待填字母：', wait_spell_alpha)
                right_answer = wait_spell_alpha

            if bank_id != wrong_bank_id or wrong_count >= 2:  # 单选做对
                mine_answer = self.word_spell_do_process(game_container, game_mode, do_right=True, right_answer=right_answer)
            else:
                mine_answer = self.word_spell_do_process(game_container, game_mode)
                if 'disable' not in self.commit_btn().get_attribute('class'):
                    wrong_count += 1
            print('我的答案：', mine_answer)

            if 'disable' not in self.commit_btn().get_attribute('class'):
                bank_list.append(bank_id)
                self.commit_btn_judge(True)
                self.commit_btn().click()
                index += 1
                print('页面正确答案：', self.right_answer(game_container))
                self.commit_btn().click()
                time.sleep(1)
                print('-' * 20, '\n')
        used_time = round(time.time()) - start_time
        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        return used_time


    @teststeps
    def word_spell_exam_operate(self, do_type, wrong_id_list, check_answer, result_index):
        """单词拼写试卷过程"""
        if do_type != 2:
            bank_id = self.bank_id()
            game_container = self.spell_container_no_index()
            game_mode = game_container.get_attribute('mode')
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info['word']
            print("解释：", self.explain(game_container))
            print('正确答案：', right_answer)

            if game_mode in ['1', '3']:
                words = self.random_spell_show_words(game_container)
                print('待填写单词:', words)
                print('正确答案：', right_answer)
                wait_spell_alpha = [right_answer[i] for i, alpha in enumerate(list(''.join(words))) if alpha == '_']
                print('待填字母：', wait_spell_alpha)
                right_answer = wait_spell_alpha

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                mine_answer = self.word_spell_do_process(game_container, game_mode, do_right=True, right_answer=right_answer)
            else:
                mine_answer = self.word_spell_do_process(game_container, game_mode)
                wrong_id_list.append(bank_id)
        else:
            mine_answer = check_answer
            game_container = self.spell_container_with_index(result_index)
            game_mode = game_container.get_attribute('mode')
            print('解释：', self.explain(game_container))
            print('正确答案：', self.right_answer(game_container))
            result_index_content = self.get_result_index_content(game_container)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            else:
                if '未作答' not in result_index_content:
                    self.base_assert.except_error('本题未作答， 结果页题标未显示未作答')

            if game_mode == '3':
                page_result_answer = self.random_spell_final_word(game_container)
            else:
                page_result_answer = self.normal_spell_mine_answer(game_container)
            print('页面我的答案：', page_result_answer)

            if check_answer:
                if page_result_answer != check_answer:
                    self.base_assert.except_error("页面显示答案与我的答案不一致 页面为%s， 我的答案为%s" % (page_result_answer, check_answer))
        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer




