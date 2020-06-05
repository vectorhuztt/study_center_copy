#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/21 15:34
# -----------------------------------------
import random
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.sentence_reform import SentenceReform
from conf.decorator import teststep, teststeps


class ListenSentence(SentenceReform):

    @teststep
    def listen_sentence_container_no_index(self):
        """结果页父级元素"""
        ele = self.driver.find_element_by_css_selector('.tylj-container')
        return ele

    @teststep
    def listen_sentence_container_with_index(self, index):
        """结果页父级元素"""
        ele = self.driver.find_element_by_css_selector('div[class ~="tylj-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def wait_check_listen_sentence_page(self):
        """听音连句页面检查点"""
        locator = (By.CSS_SELECTOR, '.tylj-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def waiting_words(self, container_ele):
        """待点击的单词部分"""
        ele = container_ele.find_elements_by_css_selector('.grid-list .bg')
        return [x for x in ele if x.text]

    @teststep
    def show_words(self, container_ele):
        """展示已点击的单词"""
        ele = container_ele.find_elements_by_css_selector('.sentence-wrap li')
        return ele

    @teststep
    def voice_play_btn(self, container_ele):
        """声音播放按钮"""
        ele = container_ele.find_element_by_class_name('speaker')
        return ele

    @teststep
    def listen_sentence_final_answer(self, container_ele):
        """听音连句最终结果"""
        ele = container_ele.find_elements_by_css_selector('.sentence-wrap .font-large')
        return ' '.join([x.text.strip() for x in ele])


    @teststep
    def mine_answer(self, container_ele):
        """结果页我的答案"""
        ele = container_ele.find_elements_by_css_selector('.sentence-wrap .font-large')
        return ' '.join([x.text.strip() for x in ele])

    @teststep
    def right_answer(self, container_ele):
        """结果页正确答案"""
        ele = container_ele.find_element_by_css_selector('.answer')
        return ele.text

    @teststep
    def result_input_ele(self, container_ele):
        """结果页输入栏"""
        ele = container_ele.find_elements_by_css_selector('.answer-wrap .grid-list .bg')
        return ele


    @teststep
    def listen_sentence_select_word_operate(self, game_container, right_answer, do_right=False):
        """听音连句选词步骤"""
        word_index = 0
        if do_right:
            while len(self.waiting_words(game_container)):
                for y in self.waiting_words(game_container):
                    if y.text == right_answer[word_index]:
                        y.click()
                        word_index += 1
                        time.sleep(0.5)
                        break
        else:
            while len(self.waiting_words(game_container)):
                if word_index == 0:
                    for x in self.waiting_words(game_container):
                        if x.text != right_answer[0]:
                            x.click()
                            word_index += 1
                            break
                    time.sleep(1)
                else:
                    for y in self.waiting_words(game_container):
                        y.click()
                        word_index += 1
                        time.sleep(0.25)


    @teststeps
    def listen_sentence_game_process(self):
        """听音连句游戏过程"""
        print('======== 听音连句 ========\n')
        start_time = round(time.time())
        right_bank, bank_list  = [], []
        index, wrong_count, wrong_bank_id = 0, 0, 0
        bank_count = self.bank_count()

        while self.wait_check_listen_sentence_page():
            self.commit_btn_judge()
            game_container = self.listen_sentence_container_no_index()
            bank_id = self.bank_id()
            waiting_part = self.waiting_words(game_container)
            begin_text = ' '.join([x.text for x in waiting_part])
            print('初始文本：', begin_text)
            self.driver.execute_script("document.getElementsByClassName('answer')[0].style.display='block'")
            right_answer = self.right_answer(game_container).split('答案：')[1].split()
            print('正确答案：', right_answer)

            if bank_id in right_bank:
                print('★★★ 此题已做正确， 但是再次出现')
            if index == 0:
                wrong_bank_id = bank_id

            if bank_id != wrong_bank_id or wrong_count >= 2:
                self.listen_sentence_select_word_operate(game_container, right_answer, do_right=True)
                right_bank.append(bank_id)
            else:
                self.listen_sentence_select_word_operate(game_container, right_answer, do_right=False)
                random_index = random.randint(0, len(self.show_words(game_container)) - 1)
                if index == 0:
                    self.show_words(game_container)[random_index].click()
                    time.sleep(1)
                    if self.waiting_words(game_container)[0].text == '':
                        print('★★★ 从填入栏点击，单词未返回候补区域')
                    else:
                        self.waiting_words(game_container)[0].click()
                        time.sleep(1)

                    self.clear_btn().click()
                    time.sleep(2)
                    if len([x for x in self.show_words(game_container) if x.text != '']):
                        print('★★★ 点击清空后, 填入栏未清空')
                    self.listen_sentence_select_word_operate(game_container, right_answer, do_right=False)
                wrong_count += 1
            mine_answer = self.listen_sentence_final_answer(game_container)
            print('我的答案：', mine_answer)
            index += 1
            bank_list.append(bank_id)
            time.sleep(0.5)
            self.commit_btn().click()
            time.sleep(1.5)
            self.commit_btn().click()
            time.sleep(1)
            print('-' * 30, '\n')
        print(bank_list)
        used_time = round(time.time()) - start_time
        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        return used_time

    @teststeps
    def listen_sentence_exam_operate(self, do_type, wrong_id_list, check_answer, result_index):
        """听音连句试卷操作"""
        if do_type != 2:
            bank_id = self.bank_id()
            game_container = self.listen_sentence_container_no_index()
            waiting_part = self.waiting_words(game_container)
            begin_text = ' '.join([x.text for x in waiting_part])
            print('初始文本：', begin_text)
            self.driver.execute_script("document.getElementsByClassName('answer')[0].style.display='block'")
            right_answer = self.right_answer(game_container).split('答案：')[1].split()
            print('正确答案：', right_answer)

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                self.listen_sentence_select_word_operate(game_container, right_answer, do_right=True)
            else:
                self.listen_sentence_select_word_operate(game_container, right_answer, do_right=False)
                wrong_id_list.append(bank_id)
            mine_answer = self.listen_sentence_final_answer(game_container)
        else:
            mine_answer = check_answer
            game_container = self.listen_sentence_container_with_index(result_index)
            print('正确答案：', self.right_answer(game_container))
            page_result_answer = self.mine_answer(game_container)
            print('页面我的答案：', page_result_answer)
            result_index_content = self.get_result_index_content(game_container)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            else:
                if '未作答' not in result_index_content:
                    self.base_assert.except_error('本题未作答， 结果页题标未显示未作答')

            if check_answer:
                if page_result_answer != check_answer:
                    self.base_assert.except_error("页面显示答案与我的答案不一致 页面为%s， 我的答案为%s" % (page_result_answer, check_answer))

            if len(self.waiting_words(game_container)):
                self.base_assert.except_error('结果页输入单词栏依然存在单词 ')

        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer
