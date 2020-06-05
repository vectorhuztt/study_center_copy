#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/28 15:50
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf.base_page import BasePage
from conf.decorator import teststep
from utils.wait_element import WaitElement


class CommonElePage(BasePage):
    wait = WaitElement()

    @teststep
    def wait_check_home_page(self):
        """首页页面等待方法"""
        locator = (By.CSS_SELECTOR, '.icon-home')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_error_tip_page(self):
        """错误信息提示"""
        locator = (By.CLASS_NAME, "el-message__content")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_tip_box_page(self):
        """弹窗信息页面检查点"""
        locator = (By.CLASS_NAME, "el-message-box__content")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_start_study_page(self):
        """开始页面检查点"""
        locator = (By.CSS_SELECTOR, '.ready')
        return self.wait.wait_check_element(locator)

    @teststep
    def exit_icon(self):
        """退出按钮"""
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style$="display: none;"]) .icon-exit')
        return self.wait.wait_find_element(locator)

    @teststep
    def bank_id(self):
        """题目id"""
        locator = (By.CSS_SELECTOR, ".van-dialog")
        ele = self.wait.wait_find_element(locator)
        return ele.get_attribute('data-exercise-id')

    @teststep
    def clear_btn(self):
        """清除按钮"""
        locator = (By.CSS_SELECTOR, ".icon-components-eraser")
        return self.wait.wait_find_element(locator)

    @teststep
    def error_content(self):
        """错误提示内容"""
        locator = (By.CLASS_NAME, "el-message__content")
        return self.wait.wait_find_element(locator).text

    @teststep
    def tip_box_content(self):
        """弹框形式提示内容"""
        locator = (By.CLASS_NAME, "el-message-box__content")
        return self.wait.wait_find_element(locator).text

    @teststep
    def confirm_btn(self):
        """弹框提示确定按钮"""
        locator = (By.CSS_SELECTOR, ".el-message-box__btns .el-button--primary")
        return self.wait.wait_find_element(locator)

    @teststep
    def cancel_btn(self):
        """弹框提示取消按钮"""
        locator = (By.CSS_SELECTOR, ".el-message-box__btns .el-button:nth-child(1)")
        return self.wait.wait_find_element(locator)

    @teststep
    def start_text(self):
        """开始提示文本"""
        locator = (By.CSS_SELECTOR, ".ready")
        return self.wait.wait_find_element(locator).text

    @teststep
    def content_desc(self):
        """关于单词个数的描述"""
        locator = (By.CSS_SELECTOR, ".content .description")
        return self.wait.wait_find_element(locator).text

    @teststep
    def commit_btn(self):
        """下一步提交按钮"""
        locator = (By.CSS_SELECTOR, ".icon-components-arrow")
        return self.wait.wait_find_elements(locator)[-1]

    @teststep
    def click_start_button(self):
        """点击开始学习按钮"""
        locator = (By.CSS_SELECTOR, ".el-dialog__body .ready .el-button")
        self.wait.wait_find_element(locator).click()

    @teststep
    def alert_tip_operate(self):
        if self.wait_check_tip_box_page():
            print("弹框提示内容：", self.tip_box_content(), '\n')
            self.confirm_btn().click()
            time.sleep(2)

    @teststep
    def commit_btn_judge(self, status=False):
        """下一步按钮状态判断"""
        if not status:
            if 'disable' not in self.commit_btn().get_attribute('class'):
                self.base_assert.except_error('提交按钮默认未置灰')
        else:
            if 'disable' in self.commit_btn().get_attribute('class'):
                self.base_assert.except_error("答题已完成，但是提交按钮依然置灰")
