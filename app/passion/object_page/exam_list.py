import random
import time

from selenium.webdriver.common.by import By

from app.passion.object_page.fill_blank_game import FillBlankGame
from app.passion.object_page.home_page import PassionHomePage
from app.passion.object_page.passion_common import PassionCommonEle
from app.passion.object_page.passion_sql_handle import PassionSQLHandle
from app.passion.object_page.single_choice import SingleChoiceGame
from conf.decorator import teststep, teststeps


class ExamPage(PassionCommonEle):

    def __init__(self):
        self.home = PassionHomePage()

    @teststep
    def wait_check_exam_record_list_page(self):
        """试卷记录页面检查点"""
        locator = (By.XPATH, '//*[contains(text(),"真题目录")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_exam_page(self):
        locator = (By.CSS_SELECTOR, '.icon-card')
        return self.get_wait_check_page_result(locator)

    @teststep
    def exam_group_ele(self):
        """所有试卷记录"""
        ele = self.driver.find_elements_by_xpath('//*[contains(@class,"el-table__body-wrapper")]/table/tbody/tr')
        return ele

    @teststep
    def exam_name(self, exam_ele):
        """试卷名称"""
        ele = exam_ele.find_element_by_xpath('./td[1]/div')
        return ele.text

    @teststep
    def latest_exam_date(self, exam_ele):
        """最新的做题时间"""
        ele = exam_ele.find_element_by_xpath('./td[2]/div/span')
        return ele.text

    @teststep
    def exam_used_time(self, exam_ele):
        """耗时"""
        ele = exam_ele.find_element_by_xpath('./td[3]/div/span')
        return ele.text

    @teststep
    def exam_score(self, exam_ele):
        """成绩"""
        ele = exam_ele.find_element_by_xpath('./td[4]/div/span')
        return ele.text

    @teststep
    def start_exam_by_ele(self, exam_ele):
        """开始考试"""
        ele = exam_ele.find_element_by_xpath('./td[5]/div/button[1]')
        return ele

    @teststep
    def check_report(self, exam_ele):
        """查看报告"""
        ele = exam_ele.find_element_by_xpath('./td[5]/div/button[2]')
        return ele

    @teststep
    def page_num(self):
        """页码"""
        ele = self.driver.find_elements_by_xpath('//*[@class="el-pager"]/li')
        return ele

    @teststep
    def answer_card_icon(self):
        """查看答案卡图标"""
        ele = self.driver.find_element_by_css_selector('.icons .icon-card')
        return ele

    # ===== 答题卡页面 =====
    @teststep
    def wait_check_answer_card_page(self):
        """答题卡页面检查点"""
        locator = (By.CSS_SELECTOR, '.answer-card')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_result_explain(self, bank_ele):
        """结果页解析页面检查点"""
        try:
            explain = bank_ele.find_element_by_css_selector('.explain')
            return explain.text
        except:
            return False

    @teststep
    def exam_bank_num(self):
        """试卷题目索引"""
        ele = self.driver.find_elements_by_css_selector('.answer-card:not([style="display: none;"])  .detail .number')
        return ele

    @teststep
    def submit_btn(self):
        """交卷按钮"""
        ele = self.driver.find_element_by_css_selector('.button-wrap button')
        return ele

    # ===== 试卷结果页 =======、
    @teststep
    def wait_check_exam_detail_page(self):
        """试卷详情页页面检查点"""
        locator = (By.CSS_SELECTOR, '.exam-detail')
        return self.get_wait_check_page_result(locator)

    @teststep
    def exam_result_score(self):
        """试卷结果页答案"""
        ele = self.driver.find_element_by_css_selector('.answer-card .score')
        return int(ele.text)

    @teststep
    def select_bank_opt_letter(self):
        """试卷选择题页面选择字母"""
        ele = self.driver.find_elements_by_css_selector('.option .letter')
        return ele

    @teststep
    def bank_detail_box_ele(self, index):
        """结果页试卷题目的父级盒子元素"""
        ele = self.driver.find_element_by_css_selector('.exam-detail>div:nth-child({})'.format(index))
        return ele

    @teststep
    def result_bank_container(self, box_ele):
        """结果页"""
        ele = box_ele.find_elements_by_css_selector('div')
        container = ele[0].get_attribute('class')
        return container

    @teststep
    def result_select_ques(self, box_ele):
        """结果页选择题问题"""
        ele = box_ele.find_element_by_css_selector('.exercise-body .question')
        return ele.text

    @teststep
    def result_select_opt_text(self, box_ele):
        """选择题选项内容"""
        ele = box_ele.find_elements_by_css_selector('.exercise-body .option .text')
        return ele

    @teststep
    def result_select_opt_letter(self, box_ele):
        """选择题选项字母"""
        ele = box_ele.find_elements_by_css_selector('.exercise-body .option .letter')
        return ele

    @teststep
    def result_blank_content(self, box_ele):
        ele = box_ele.find_element_by_css_selector('.bq-wrap')
        return ele.text

    @teststep
    def result_blank_answer(self, box_ele, do_right):
        """结果页填空题我的答案"""
        if do_right:
            ele = box_ele.find_elements_by_css_selector('.blank-result .success')
        else:
            ele = box_ele.find_elements_by_css_selector('.blank-result .error')
        return [x.text.strip() for x in ele]

    @teststeps
    def exam_operate(self, do_right, half_exit, mine_answer_info):
        if self.wait_check_exam_page():
            self.answer_card_icon().click()
        if self.wait_check_answer_card_page():
            bank_numbers = self.exam_bank_num()
            for x in range(len(bank_numbers)):
                if half_exit:
                    if x == 1:
                        self.exit_icon().click()
                        time.sleep(1)
                        break

                is_blank = False
                bank_numbers[x].click()
                if self.wait_check_exam_page():
                    game_container = self.game_container()
                    bank_id = self.bank_id()
                    print('题目id：', bank_id)
                    right_answer = PassionSQLHandle().get_ques_right_answer(bank_id)
                    print('正确答案：', right_answer)
                    mine_answer = 0
                    if game_container == 'dx-container':
                        mine_answer = SingleChoiceGame().single_choice_do_process(do_right=do_right, right_answer=right_answer)
                    elif game_container == 'bq-container':
                        is_blank = True
                        mine_answer = FillBlankGame().fill_blank_process(counter=2, do_right=do_right, right_answer=right_answer)
                    print('我的答案：', mine_answer)
                    mine_answer_info[bank_id] = mine_answer
                    self.answer_card_icon().click()
                    time.sleep(2)
                if self.wait_check_answer_card_page():
                    if 'filled' not in self.exam_bank_num()[x].get_attribute('class'):
                        self.base_assert.except_error('该题已做完， 但是答题卡页面显示未完成')
                    if is_blank:
                        if not do_right:
                            if 'success' in self.exam_bank_num()[x].get_attribute('class'):
                                self.base_assert.except_error('该填空题未做全对， 但是结果页显示正确')

                print('-'*30, '\n')
            if not half_exit:
                self.submit_btn().click()
                self.alert_tip_operate()

    @teststep
    def check_answer_operate(self, do_right, mine_answer_info):
        if self.wait_check_answer_card_page():
            for x in self.exam_bank_num():
                number = x.text
                x.click()
                time.sleep(1)
                if self.wait_check_exam_detail_page():
                    bank_ele = self.bank_detail_box_ele(index=number)
                    bank_container = self.result_bank_container(bank_ele)
                    mine_answer = mine_answer_info[list(mine_answer_info.keys())[int(number) - 1]]
                    print('我的答案：', mine_answer)
                    if bank_container == 'dx-container':
                        print(self.result_select_ques(bank_ele))
                        opt_letters = self.result_select_opt_letter(bank_ele)
                        opt_text = self.result_select_opt_text(bank_ele)
                        for i, opt in enumerate(opt_text):
                            if opt.text == mine_answer:
                                print('选项字母内容：', opt_letters[i].text)
                                if do_right:
                                    if '对' not in opt_letters[i].text:
                                        self.base_assert.except_error('题目已做对，但是结果选项没有标识做对')
                                else:
                                    if '错' not in opt_letters[i].text:
                                        self.base_assert.except_error('题目已做错，但是结果选项没有标识做错')
                    elif bank_container == 'bq-container':
                        print(self.result_blank_content(bank_ele))
                        trans_mine_answer = [x.lower() for x in mine_answer]
                        trans_page_answer = [x.lower() for x in self.result_blank_answer(bank_ele, do_right)]
                        print('页面我的答案：', trans_page_answer)
                        if trans_mine_answer != trans_page_answer:
                            self.base_assert.except_error('结果页显示的答案于输入答案不一致')
                    result_explain = self.wait_check_result_explain(bank_ele)
                    if result_explain:
                        print(result_explain)
                self.submit_btn().click()
                time.sleep(1)
                print('-'*30, '\n')










