#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/6 8:15
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.cloze_text import ClozeText
from conf.decorator import teststep, teststeps


class ListenChoice(ClozeText):

    @teststep
    def wait_check_listen_choice_page(self):
        """听后选择"""
        locator = (By.CSS_SELECTOR, '.thxz-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_red_hint_page(self):
        """红色提示按钮"""
        locator = (By.CSS_SELECTOR, '.control-bar .danger-text')
        return self.get_wait_check_page_result(locator)

    @teststep
    def listen_container_no_index(self):
        """听后选择父级容器"""
        ele = self.driver.find_element_by_css_selector('.thxz-container')
        return ele

    @teststep
    def listen_container_with_index(self, index):
        """听后选择父级容器"""
        ele = self.driver.find_element_by_css_selector('div[class ~="thxz-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def exam_speaker_btn(self, container_ele):
        """试卷音频播方按钮"""
        ele = container_ele.find_element_by_css_selector('.player .speaker')
        return ele

    @teststeps
    def listen_choice_game_operate(self):
        """听后选择游戏过程"""
        start_time = round(time.time())
        right_answer = []
        while self.wait_check_listen_choice_page():
            for x in range(2):
                mine_answer = []
                game_container = self.listen_container_no_index()
                if x == 0:
                    bank_id = self.bank_id()
                    bank_data_info = self.handle.get_multi_bank_answer(bank_id)
                    right_answer = [(x['answer'], x[x['answer']]) for x in bank_data_info]
                self.commit_btn_judge(status=True)
                self.commit_btn().click()
                time.sleep(2)
                if self.wait_check_red_hint_page():
                    self.base_assert.except_error('点击听力播放按钮后， 红色提示未消失')
                self.commit_btn_judge()
                ques_list = self.quest_list(game_container)
                for i, y in enumerate(ques_list):
                    question = self.question(y)
                    print('问题:', question)
                    print('正确答案：', right_answer[i])
                    if x != 0:
                        select_answer = self.cloze_select_opt_operate(y, do_right=True, right_answer=right_answer[i][0])
                    else:
                        select_answer = self.cloze_select_opt_operate(y, right_answer=right_answer[i][0])
                    mine_answer.append(select_answer)
                    print('我的答案：', mine_answer, '\n')

                time.sleep(1)
                while True:
                    if 'disable' not in self.commit_btn().get_attribute('class'):
                        break
                    else:
                        time.sleep(2)
                self.commit_btn().click()
                time.sleep(1)
                self.cloze_result_check_operate(mine_answer, fq=x, game_type=0, game_container=self.listen_container_no_index())
                self.commit_btn().click()
                if x != 1:
                    if not self.wait_check_listen_choice_page():
                        self.base_assert.except_error('页面存在错题， 点击提交后未重新开始游戏')
                else:
                    if self.wait_check_listen_choice_page():
                        self.base_assert.except_error('已做全对， 点击提交未提交成功')
                print('-' * 30, '\n')
        used_time = round(time.time()) - start_time
        return used_time

    @teststeps
    def listen_choice_exam_operate(self, do_type, wrong_id_list, check_answer, result_index, do_count):
        """听后选择试卷过程"""
        mine_answer = []
        if do_type != 2:
            bank_id = self.bank_id()
            if do_type == 0:
                wrong_id_list.append(bank_id)
            bank_data_info = self.handle.get_multi_bank_answer(bank_id)
            right_answer = [(x['answer'], x[x['answer']]) for x in bank_data_info]
            game_container = self.listen_container_no_index()
            ques_list = self.quest_list(game_container)
            self.exam_speaker_btn(game_container).click()
            time.sleep(1)
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
            game_container = self.listen_container_with_index(result_index)
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
            self.cloze_result_check_operate(check_answer, fq=fq, game_type=0, game_container=game_container)

        print('我的答案：', mine_answer)
        print('-' * 30, '\n')
        return mine_answer