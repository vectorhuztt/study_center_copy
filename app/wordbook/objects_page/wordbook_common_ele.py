#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/28 17:12
# -----------------------------------------
import time
from selenium.webdriver.common.by import By
from app.common_ele.common_page import CommonElePage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep


class WordBookPublicElePage(CommonElePage):

    @teststep
    def wait_check_start_study_page(self):
        """句子解释页面检查点"""
        locator = (By.XPATH, '//span[text()="开始学习"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_error_tab_page(self):
        """错误提示页面检查点"""
        locator = (By.CSS_SELECTOR, '.el-message-box__content')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_error_flash_page(self):
        """错误提示页面检查点"""
        locator = (By.CSS_SELECTOR, '.el-message__content')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_finish_page(self):
        """句子解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.bdc-dialog-wrap .finished')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_answer_word_page(self):
        """正确答案页面检查点"""
        locator = (By.CSS_SELECTOR, '.main .answer')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_container_page(self):
        """游戏容器页面检查点"""
        locator = (By.CSS_SELECTOR, 'div[class $="container"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def game_container(self):
        """游戏container名称"""
        locator = (By.CSS_SELECTOR, '.component-wrap div[class $="container"]')
        ele = self.wait.wait_find_element(locator)
        container = ele.get_attribute('class')
        mode_value = ele.get_attribute('mode')
        explain_id = ele.get_attribute('id')
        mode = mode_value if mode_value else '-1'
        return container, mode, explain_id

    @teststep
    def word_explain(self):
        """单词解释"""
        locator = (By.CSS_SELECTOR, '.main .explain')
        return self.wait.wait_find_element(locator).text

    @teststep
    def right_answer(self):
        """正确答案"""
        locator = (By.CSS_SELECTOR, '.main .answer')
        return self.wait.wait_find_element(locator).text

    @teststep
    def definite_btn(self):
        """确定按钮"""
        locator = (By.XPATH, '//span[text()="确定"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def error_tab_content(self):
        """错误提示"""
        locator = (By.CSS_SELECTOR, '.el-message-box__content')
        return self.wait.wait_find_element(locator).text

    @teststep
    def click_confirm_btn(self):
        """点击确定按钮"""
        locator = (By.CSS_SELECTOR, '.el-message-box__btns .el-button:last-child')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_speaker_icon(self):
        """点击声音按钮"""
        locator = (By.CSS_SELECTOR, '.control-bar .speaker')
        self.wait.wait_find_element(locator).click()
        time.sleep(1)

    @teststep
    def finish_content(self):
        """一组结束页面内容"""
        locator = (By.CSS_SELECTOR, '.finished h2')
        return self.wait.wait_find_element(locator).text

    @teststep
    def more_one_group(self):
        """点击再来一组按钮 """
        locator = (By.CSS_SELECTOR, '.finished .btn-control .el-button')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def finish_first_btn(self):
        """点击开始复习按钮"""
        locator = (By.CSS_SELECTOR, '.finished .flex-wrap .btn-control .el-button:first-child')
        return self.wait.wait_find_element(locator)

    @teststep
    def alert_tab_operate(self):
        """提示页面处理"""
        if self.wait_check_error_tab_page():
            print(self.error_tab_content(), '\n')
            self.click_confirm_btn()
            time.sleep(2)

    @teststep
    def test_timer_check(self, timer):
        """测试时间校验"""
        return all([y > x for x, y in zip(timer[:-1], timer[1:])])

    @teststep
    def check_words_fluency_value(self, stu_id, before_fluency, f_is_change, is_right=False):
        """
            校验单词解释的F值是否正确
            :param stu_id  学生id
            :param before_fluency 做题之前单词F值列表
            :param is_right   是否做对
            :param f_is_change  F值是否变换
        """
        print('F值是否发生变化：', f_is_change)
        after_fluency = {x: WordBookSqlHandle().get_explain_fluency_by_explain_id(stu_id, x) for x in list(before_fluency.keys())}
        print('学前单词F值:', before_fluency)
        print('学后单词F值:', after_fluency)
        if f_is_change:
            add_value = 2 if is_right else 1
        else:
            add_value = 0

        check_fluency_info = {x: before_fluency[x] + add_value for x in list(before_fluency.keys())}
        if check_fluency_info != after_fluency:
            self.base_assert.except_error('单词的F值变化有误， 应为{}, 实际为{}'.format(check_fluency_info, after_fluency))





