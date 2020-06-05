#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/5 16:28
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.cloze_text import ClozeText
from conf.decorator import teststep


class ReadUnderStandText(ClozeText):

    @teststep
    def wait_check_read_understand_page(self):
        """阅读理解页面检查点"""
        locator = (By.CSS_SELECTOR, '.ydlj-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def read_understand_container_no_index(self):
        """阅读理解父级容器元素"""
        ele = self.driver.find_element_by_css_selector('.ydlj-container')
        return ele

    @teststep
    def read_understand_container_with_index(self, index=0):
        """阅读理解父级容器元素"""
        ele = self.driver.find_element_by_css_selector('div[class ~="ydlj-container"][index="{}"]'.format(index))
        return ele

    @teststep
    def read_understand_text(self, container_ele):
        ele = container_ele.find_element_by_css_selector('.article-wrap .content')
        return ele.text

    @teststep
    def read_understand_game_operate(self):
        """阅读理解游戏过程处理"""
        start_time = round(time.time())
        right_answer = []
        while self.wait_check_read_understand_page():
            for x in range(3):
                mine_answer = []
                game_container = self.read_understand_container_no_index()
                self.commit_btn_judge()
                if x == 0:
                    print(self.read_understand_text(game_container))
                    bank_id = self.bank_id()
                    bank_data_info = self.handle.get_multi_bank_answer(bank_id)
                    right_answer = [(x['answer'], x[x['answer']]) for x in bank_data_info]
                ques_list = self.quest_list(game_container)
                for i, y in enumerate(ques_list):
                    question = self.question(y)
                    print('问题：', question)
                    print('正确答案：', right_answer[i])
                    if (x == 1 and i in [0, 1]) or x == 2:
                        select_answer = self.cloze_select_opt_operate(y, do_right=True, right_answer=right_answer[i][0])
                    else:
                        select_answer = self.cloze_select_opt_operate(y, right_answer=right_answer[i][0])
                    mine_answer.append(select_answer)
                    print('我的答案：', mine_answer, '\n')
                self.commit_btn_judge(status=True)
                self.commit_btn().click()
                time.sleep(1)
                self.cloze_result_check_operate(mine_answer, fq=x, game_container=self.read_understand_container_no_index())
                self.commit_btn().click()
                if x != 2:
                    if not self.wait_check_read_understand_page():
                        self.base_assert.except_error('页面存在错题， 点击提交后未重新开始游戏')
                else:
                    if self.wait_check_read_understand_page():
                        self.base_assert.except_error('已做全对， 点击提交未提交成功')
                print('-' * 30, '\n')
        used_time = round(time.time()) - start_time
        return used_time


    @teststep
    def read_understand_exam_operate(self, do_type, wrong_id_list, check_answer, result_index, do_count):
        """阅读理解试卷过程"""
        mine_answer = []
        if do_type != 2:
            bank_id = self.bank_id()
            game_container = self.read_understand_container_no_index()
            if do_type == 0:
                wrong_id_list.append(bank_id)
                print(self.cloze_text(game_container))
            bank_data_info = self.handle.get_multi_bank_answer(bank_id)
            right_answer = [x['answer'] for x in bank_data_info]

            ques_list = self.quest_list(game_container)
            for i, y in enumerate(ques_list):
                question = self.question(y)
                print('问题：', question)
                print('正确答案：', right_answer[i])
                if do_type:
                    select_ans = self.cloze_select_opt_operate(y, do_right=True, right_answer=right_answer[i])
                else:
                    select_ans = self.cloze_select_opt_operate(y, right_answer=right_answer[i])
                mine_answer.append(select_ans)
        else:
            mine_answer = check_answer
            game_container = self.read_understand_container_with_index(result_index)
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
