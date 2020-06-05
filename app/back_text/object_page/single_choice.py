#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/21 15:37
# -----------------------------------------
import time
from selenium.webdriver.common.by import By
from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps
from utils.ele_attr_check import EleAttrCheck


class SingleChoice(GameCommonElePage):
    @teststep
    def wait_check_single_choice_page(self):
        """单项选择页面检查点"""
        locator = (By.CSS_SELECTOR, '.dx-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_choice_explain_page(self):
        """背课文页面检查点"""
        locator = (By.CSS_SELECTOR, ".explain-content")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_choice_speaker_page(self):
        locator = (By.CSS_SELECTOR, ".audio-player")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_text_explain_page(self):
        """文字解析页面检查点"""
        locator = (By.CSS_SELECTOR, ".explain-content pre")
        return self.get_wait_check_page_result(locator)

    @teststep
    def single_choice_container(self, index=0):
        """单选父级容器元素 不带index"""
        container = self.driver.find_elements_by_css_selector('.dx-container')
        return container[index]

    @teststep
    def question(self, container_ele):
        """选项问题"""
        ele = container_ele.find_element_by_css_selector('.question')
        return ele.text

    @teststep
    def opt_letter(self, container_ele):
        """选项"""
        ele = container_ele.find_elements_by_css_selector('.letter')
        return ele

    @teststep
    def opt_content(self, container_ele):
        """选项内容"""
        ele = container_ele.find_elements_by_css_selector('.radio-wrapper  .text')
        return ele

    @teststep
    def play_voice_btn(self, container_ele):
        """语音解析按钮"""
        ele = container_ele.find_element_by_css_selector('.audio-player .icon-components')
        return ele

    @teststep
    def analysis_content(self, container_ele):
        """文本解析内容"""
        ele = container_ele.find_element_by_css_selector('.explain-content pre')
        return ele.text

    @teststep
    def single_choice_select_opt_operate(self, game_container,  do_right=False, right_answer=None,):
        """单项选择选择选项操作"""
        select_answer = 0
        for opt in self.opt_content(game_container):
            if do_right:
                if opt.text == right_answer:  # 判断选项是否等于正确选项
                    select_answer = opt.text
                    opt.click()
                    time.sleep(0.5)
                    break
            else:
                if opt.text != right_answer:
                    select_answer = opt.text
                    opt.click()
                    time.sleep(0.5)
                    break
        return select_answer

    @teststeps
    def single_choice_text_explain_operate(self, game_container):
        """单项选择解析处理"""
        if self.wait_check_choice_explain_page():
            if self.wait_check_choice_speaker_page():
                print('有语音解析')
                self.play_voice_btn(game_container).click()
                time.sleep(3)
            else:
                print('没有语音解析')
            if self.wait_check_text_explain_page():
                analysis_text = self.analysis_content(game_container)
                print('存在文字解析,解析文本：', analysis_text)
            else:
                print('没有文本解析')
        else:
            print('无解析')

    @teststeps
    def single_choice_game_process(self):
        """单项选择游戏过程"""
        print('======== 单项选择 ========\n')
        start_time = round(time.time())
        bank_list = []
        right_bank = []
        wrong_bank_id, index, wrong_count = 0, 0, 0
        bank_count = self.bank_count()
        while self.wait_check_single_choice_page():
            self.commit_btn_judge()
            game_container = self.single_choice_container()
            print('问题：', self.question(game_container))
            bank_id = self.bank_id()
            if bank_id in right_bank:
                print('本题已做对，却再次出现')
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info[bank_data_info['answer']]
            print('正确选项：', right_answer)

            if index == 0:
                wrong_bank_id = bank_id

            if bank_id != wrong_bank_id or wrong_count >= 2:
                self.single_choice_select_opt_operate(game_container, do_right=True, right_answer=right_answer)
                right_bank.append(bank_id)
            else:
                self.single_choice_select_opt_operate(game_container, right_answer=right_answer)
                wrong_count += 1
            bank_list.append(bank_id)
            self.commit_btn_judge(True)
            self.commit_btn().click()
            self.single_choice_text_explain_operate(game_container)

            index += 1
            self.commit_btn().click()
            time.sleep(1)
            print('-' * 20, '\n')

        self.check_wrong_bank_interval(bank_count, bank_list, wrong_bank_id)
        used_time = round(time.time()) - start_time
        return used_time

    @teststeps
    def single_choice_exam_process(self, do_type, wrong_id_list, check_answer, result_index):
        """单项选择试卷过程"""
        if do_type != 2:
            game_container = self.single_choice_container()
            print('问题：', self.question(game_container))
            bank_id = self.bank_id()
            bank_data_info = self.handle.get_one_bank_answer(bank_id)
            right_answer = bank_data_info[bank_data_info['answer']]
            print('正确选项：', right_answer)

            if do_type:
                if bank_id in wrong_id_list:
                    self.base_assert.except_error('本题不在错题列表中， 但是出现错题再练 ' + bank_id)
                mine_answer = self.single_choice_select_opt_operate(game_container, do_right=True, right_answer=right_answer)
            else:
                mine_answer = self.single_choice_select_opt_operate(game_container, right_answer=right_answer)
                wrong_id_list.append(bank_id)
        else:
            mine_answer = check_answer
            game_container = self.single_choice_container(result_index)
            result_question = self.question(game_container)
            print('问题：', result_question)
            result_index_content = self.get_result_index_content(game_container)
            if check_answer:
                if '未作答' in result_index_content:
                    self.base_assert.except_error("题目已选择， 但是结果显示未作答")
            else:
                if '未作答' not in result_index_content:
                    self.base_assert.except_error('本题未作答， 结果页题标未显示未作答')

            for i, opt in enumerate(self.opt_content(game_container)):
                opt_letter = self.opt_letter(game_container)[i]
                if opt.text  == check_answer:
                    if not(EleAttrCheck().check_word_is_in_class('success', opt_letter) or \
                       EleAttrCheck().check_word_is_in_class('error', opt_letter)):
                        self.base_assert.except_error("选择选项在结果页面显示未被选中 " + str(result_index))
                if EleAttrCheck().check_word_is_in_class('success', opt_letter):
                    print('正确答案：', opt.text)
            print('解析：', self.analysis_content(game_container))
        print('我的答案：', mine_answer)
        print('-'*30, '\n')
        return mine_answer
