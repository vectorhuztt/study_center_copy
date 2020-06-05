#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/20 17:12
# -----------------------------------------
import random
import re
import string
import time

from selenium.webdriver.common.by import By

from app.wordbook.objects_page.exam_page import ExamPage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from conf.decorator import teststep
from utils.dict_slice import DictSlice


class NewWordTestPage(ExamPage):
    slice = DictSlice()

    @teststep
    def wait_check_before_test_page(self):
        """开始学前测试页面检查点"""
        locator = (By.XPATH, '//*[contains(text(), "开始进行学前测试")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_after_test_page(self):
        """学后测试页面检查点"""
        locator = (By.XPATH, '//*[contains(text(), "进入学后验收阶段")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_pass_before_test_page(self):
        """学前测试通过页面"""
        locator = (By.XPATH, '//*[contains(text(), "单词你都掌握了")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def continue_study_btn(self):
        """学前测试通过页面，继续学习按钮"""
        locator = (By.XPATH, '//span[text()="继续学习"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def study_other_unit_btn(self):
        """学前测试通过页面， 学习其他单元按钮"""
        locator = (By.XPATH, '//span[text()="学习其他单元"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def wait_check_word_exam_page(self):
        """单词测试页面检查点"""
        locator = (By.CSS_SELECTOR, '.exam-wrap')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_score_page(self):
        """测试分数页面检查点"""
        locator = (By.CSS_SELECTOR, '.certificate .score')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_test_reporter_page(self):
        """学后测试结果页面检查点"""
        locator = (By.CSS_SELECTOR, '.certificate')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_right_answer_page(self, container):
        """学前学后测试正确答案页面检查点"""
        try:
            ele = container.find_element_by_css_selector('.answer')
            return True
        except:
            return False

    @teststep
    def wait_check_wrong_again_btn_page(self):
        """学后测试错题再练页面检查点"""
        locator = (By.XPATH, '//button/span[contains(text(),"错题再练")]')
        return self.wait.wait_check_element(locator)


    @teststep
    def start_test_btn(self):
        """开始测试"""
        locator = (By.CSS_SELECTOR, '.btn-control .el-button:nth-child(1)')
        return self.wait.wait_find_element(locator)

    @teststep
    def quit_test_btn(self):
        """放弃测试"""
        locator = (By.CSS_SELECTOR, '.btn-control .el-button:nth-child(2)')
        return self.wait.wait_find_element(locator)

    @teststep
    def page_words_count(self):
        """页面单词个数"""
        locator = (By.CSS_SELECTOR, '.ready .description')
        ele = self.wait.wait_find_element(locator)
        return re.findall(r'\d+', ele.text)

    @teststep
    def word_test_timer(self):
        """测试花费的时间"""
        locator = (By.CSS_SELECTOR, '.exam .timer')
        ele = self.wait.wait_find_element(locator)
        timer_number = re.findall(r'\d', ele.text)
        use_timer = (timer_number[0] * 10 + timer_number[1]) * 60 + (timer_number[2]*10 + timer_number[3])
        return use_timer

    @teststep
    def spell_game_container(self, index):
        """测试的父级容器"""
        locator = (By.CSS_SELECTOR, '.dcpx-container')
        ele = self.wait.wait_find_elements(locator)
        return ele[index]

    @teststep
    def word_test_explain(self, container_ele):
        """测试单词解释"""
        ele = container_ele.find_element_by_css_selector('.explain')
        return ele.text

    @teststep
    def text_input(self, container_ele):
        """测试单词输入栏"""
        ele = container_ele.find_element_by_css_selector('.text-input')
        return ele

    @teststep
    def submit_btn(self):
        """交卷按钮"""
        locator = (By.CSS_SELECTOR, '.control .el-button')
        return self.wait.wait_find_element(locator)

    @teststep
    def wrong_again_btn(self):
        """错题再练按钮"""
        locator = (By.XPATH, '//button/span[contains(text(),"错题再练")]')
        return self.wait.wait_find_element(locator)

    @teststep
    def answer_page_right_count(self):
        """结果页掌握单词数"""
        locator = (By.CSS_SELECTOR, '.exam .tips span')
        ele = self.wait.wait_find_element(locator)
        return int(ele.text)

    @teststep
    def result_score(self):
        """结果页分数"""
        locator = (By.CSS_SELECTOR, '.answer-card .score')
        ele = self.wait.wait_find_element(locator)
        return int(ele.text)

    @teststep
    def result_mine_answer(self, game_container):
        """测试结果页我的答案"""
        locator = (By.CSS_SELECTOR, '.user-answer .clearfix')
        ele = self.wait.wait_find_elements(locator)
        return ''.join([x.text for x in ele])

    @teststep
    def wrong_again_btn(self):
        """错题再练过程"""
        locator = (By.CSS_SELECTOR, '.exam .control .el-button:nth-child(1)')
        return self.wait.wait_find_element(locator)

    @teststep
    def report_content(self):
        """报告页面文本"""
        locator = (By.CSS_SELECTOR, '.certificate .main')
        return self.wait.wait_find_element(locator).text

    @teststep
    def report_name(self):
        """报告页面的用户名称"""
        locator = (By.CSS_SELECTOR, '.name-wrapper .name')
        return self.wait.wait_find_element(locator).text

    @teststep
    def report_test_book_name(self):
        """报告页面的书籍名称"""
        locator = (By.CSS_SELECTOR, '.certificate .title span')
        return self.wait.wait_find_element(locator).text

    @teststep
    def report_test_word_count(self):
        """报告页面掌握单词数"""
        locator = (By.CSS_SELECTOR, '.describe .word')
        ele = self.wait.wait_find_element(locator)
        return int(ele.text)

    @teststep
    def report_test_score(self):
        """报告页面测试分数"""
        locator = (By.CSS_SELECTOR, '.describe .score')
        ele = self.wait.wait_find_element(locator)
        return int(ele.text)

    @teststep
    def close_report_page(self):
        """关闭测试报告"""
        locator = (By.CSS_SELECTOR, '.certificate .close')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def check_word_study_tip_page(self, stu_id, book_id, unit_id, unit_status):
        """查询单元单词学习页面提示"""
        has_test = self.data.get_unit_has_test(stu_id, book_id, unit_id)
        if unit_status == '未完成':
            if has_test:
                if not self.wait_check_start_study_page():
                    self.base_assert.except_error('本单元已经做过学前测试， 点击单词学习未出现开始学习页面')
            else:
                if not self.wait_check_before_test_page():
                    self.base_assert.except_error('本单元未做过学前测试， 点击单词学习未出现学前测试页面')

        elif unit_status == '100%':
            before_test = self.data.get_unit_has_test(stu_id, book_id, unit_id, is_after=False)
            after_test = self.data.get_unit_has_test(stu_id, book_id, unit_id, is_after=True)
            before_test_score = before_test[1]
            if before_test_score == 100:
                if self.wait_check_after_test_page():
                    self.base_assert.except_error('学前测试为满分， 点击单词学习出现学后测试页面')
            else:
                if after_test:
                    if self.wait_check_after_test_page():
                        self.base_assert.except_error('已做过学后测试, 点击单词学习却依然出现学后测试页面')
                else:
                    if not self.wait_check_after_test_page():
                        self.base_assert.except_error('本单元学前测试不为满分， 且未做过学后测试， 点击开始学习未出现学后测试页面')

        elif unit_status == '已达标':
            if not has_test:
                self.base_assert.except_error('数据库查询本单元未做过学前测试， 但是单元状态为已达标')

            if not self.wait_check_start_study_page():
                self.base_assert.except_error('单元状态已达标， 点击开始学习未显示开始学习页面')
        else:
            if not self.wait_check_start_study_page():
                self.base_assert.except_error('单元状态不为100%， 点击单词学习未出现开始学习页面')
        self.exit_icon().click()

    @teststep
    def word_test_process(self, stu_id, check_ids, do_right=False, wrong_word_list=None):
        """学前学后测试主要流程"""
        test_word_info = {}
        mine_answer = {}
        right_word_info, wrong_word_info = [], []
        timer = []
        if self.wait_check_word_exam_page():
            for index in range(len(self.spell_word_game_container())):
                container = self.spell_word_game_container()[index]
                self.spell.normal_spell_input_wrap(container).click()
                explain_id = container.get_attribute('id')

                if int(explain_id) not in check_ids:
                    self.base_assert.except_error('该单词不在应做单词列表中')

                if wrong_word_list:
                    if explain_id not in wrong_word_list:
                        self.base_assert.except_error('本题已做对，错题再练时再次出现')

                right_answer = self.data.get_word_by_explain_id(explain_id)
                word_explain = self.word_test_explain(container)
                print('单词解释：', word_explain)
                print('正确答案：', right_answer)
                test_word_info[explain_id] = (right_answer, word_explain)
                if do_right:
                    self.spell.normal_spell_input_wrap(container).send_keys(right_answer)
                    input_answer = right_answer
                    right_word_info.append(explain_id)
                else:
                    if index in [0, 1]:
                        self.spell.normal_spell_input_wrap(container).send_keys(right_answer)
                        input_answer = right_answer
                        right_word_info.append(explain_id)
                    else:
                        random_str = ''.join(random.sample(string.ascii_letters, random.randint(2, 5)))
                        input_answer = random_str
                        self.spell.normal_spell_input_wrap(container).send_keys(random_str)
                        wrong_word_info.append(explain_id)
                mine_answer[explain_id] = input_answer
                print('我的答案：', input_answer)
                timer.append(self.word_test_timer())
                time.sleep(0.5)
                print('-'*30, '\n')

            before_word_fluency = {x: self.data.get_explain_fluency_by_explain_id(stu_id, x)
                                   for x in list(test_word_info.keys())}
            self.test_timer_check(timer)
            self.submit_btn().click()
            time.sleep(1)
            self.alert_tab_operate()
            wrong_word_fluency = {}
            right_word_fluency = {}
            if do_right:
                right_word_fluency.update(before_word_fluency)
            else:
                right_word_fluency.update(self.slice.dict_slice(before_word_fluency, end=2))
                wrong_word_fluency.update(self.slice.dict_slice(before_word_fluency, start=2))

            self.check_words_fluency_value(stu_id, wrong_word_fluency, f_is_change=False)
            self.check_words_fluency_value(stu_id, right_word_fluency, f_is_change=True, is_right=True)
        return mine_answer, right_word_info, wrong_word_info

    @teststep
    def word_before_test_pass_page_operate(self, unit_index,  is_study_other=False):
        """学前测试通过页面处理过程"""
        if not self.wait_check_pass_before_test_page():
            self.base_assert.except_error("测试做全对， 提交试卷后未进入通过测试页面")
        else:
            if is_study_other:
                self.study_other_unit_btn().click()
                if not self.wait_check_home_page():
                    self.base_assert.except_error('点击学习其他单元按钮后未返回主页面')
            else:
                self.continue_study_btn().click()
                if not self.wait_check_start_study_page():
                    self.base_assert.except_error('点击继续学习按钮后， 未发现开始学习页面')
                else:
                    self.exit_icon().click()

            if self.home.wait_check_home_page():
                unit_status = self.home.unit_list()[unit_index].text
                if unit_status != '100%':
                    self.base_assert.except_error('学前测试已做全对， 但是单元状态未变成已达标')
                self.home.click_study_word_tab()

    @teststep
    def word_before_test_fail_operate(self, mine_answer, right_count, is_before_test=False):
        """单词测试未做全对后的处理"""
        if self.wait_check_word_exam_page():
            for index in range(len(self.spell_word_game_container())):
                container = self.spell_word_game_container()[index]
                explain_id = container.get_attribute('id')
                mine_done_answer = mine_answer[explain_id]
                page_mine_answer = self.driver.execute_script('return document.getElementsByClassName("text-input")[{}]._value'.format(index))
                if page_mine_answer != mine_done_answer:
                    self.base_assert.except_error("页面我的的答案与我之前输入的不一致")
                if not self.wait_check_answer_word_page():
                    self.base_assert.except_error('页面未显示当前单词的正确答案')
            if is_before_test:
                page_right_count = self.answer_page_right_count()
                if page_right_count != right_count:
                    self.base_assert.except_error('页面掌握单词数与正确单词个数不一致')


    @teststep
    def test_report_page_operate(self, user_name, book_name, unit_name, word_count):
        """测试报告页面处理"""
        if self.wait_check_test_reporter_page():
            print(self.report_content())

            reporter_user_name = self.report_name()
            if reporter_user_name != user_name:
                self.base_assert.except_error('报告页面用户姓名与学生姓名不一致')

            check_book_name = '【{}—{}】'.format(book_name, unit_name)
            reporter_book_name = self.report_test_book_name()
            if reporter_book_name != check_book_name:
                self.base_assert.except_error('报告页面书籍名称与当前书籍名称不一致')

            reporter_word_count = self.report_test_word_count()
            if reporter_word_count != word_count:
                self.base_assert.except_error("页面掌握单词数与本单元单词数不一致")

            reporter_score = self.report_test_score()
            if reporter_score != 100:
                self.base_assert.except_error('分数不为100分')

            self.close_report_page()
            if not self.wait_check_home_page():
                self.base_assert.except_error('点级关闭测试报告页面， 未返回主页面')
            # else:
            #     unit_status = self.home.status_list()[unit_index].text
            #     if unit_status != '100%':
            #         self.base_assert.except_error('学前测试做全对， 但是单元状态不为100%')
            #     self.home.click_study_word_tab()
        else:
            self.base_assert.except_error('测试单词全做对， 未发现测试报告页面')
