#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/28 15:38
# -----------------------------------------
import time
from selenium.webdriver.common.by import By
from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from conf.decorator import teststep


class WordHomePage(WordBookPublicElePage):
    @teststep
    def wait_check_dialog_wrap_page(self):
        """句子解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.ready')
        return self.wait.wait_check_element(locator)

    @teststep
    def book_name(self):
        """书籍名称"""
        locator = (By.CSS_SELECTOR, ".breadcrumb span")
        return self.wait.wait_find_element(locator).text

    @teststep
    def wordbook_tip_content(self):
        """单词本解释"""
        locator = (By.CLASS_NAME, "tip-line")
        return self.wait.wait_find_element(locator).text

    @teststep
    def unit_list(self):
        """单元名称列表"""
        locator = (By.CSS_SELECTOR, ".unit-name")
        return self.wait.wait_find_elements(locator)

    @teststep
    def status_list(self):
        """单元状态列表"""
        locator = (By.CSS_SELECTOR, ".status")
        return self.wait.wait_find_elements(locator)

    @teststep
    def click_study_word_tab(self):
        """点击单词学习模块"""
        locator = (By.CSS_SELECTOR, ".bdc-module .left")
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_review_word_tab(self):
        """点击复习模块"""
        locator = (By.CSS_SELECTOR, ".bdc-module .right div:last-child")
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_test_tab(self):
        """点击测试模块"""
        locator = (By.CSS_SELECTOR, ".bdc-module .right div:first-child")
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_exit_icon(self):
        """模块退出按钮"""
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .exit')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_error_book_btn(self):
        """本书易错词"""
        locator = (By.CSS_SELECTOR, '.bdc-btn .el-button:first-child')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_book_test_btn(self):
        """本书测试"""
        locator = (By.CSS_SELECTOR, '.bdc-btn .el-button:nth-child(2)')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_test_to_end_btn(self):
        """一测到底"""
        locator = (By.CSS_SELECTOR, '.bdc-btn .el-button:nth-child(3)')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def click_study_report_btn(self):
        """学习报告"""
        locator = (By.CSS_SELECTOR, '.bdc-btn .el-button:nth-child(4)')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def check_click_tab_tip_by_unit_status(self, unit_status_list):
        """根据单元状态检查点模块点击的提示"""
        not_complete_unit = [x for x in unit_status_list if x.text not in ['未完成', '100%']]
        if not_complete_unit:
            for x in unit_status_list:
                if x.text == '未完成':
                    x.click()  # 点击未完成的单元，查看是否弹出错误提示
                    time.sleep(2)
                    self.click_study_word_tab()
                    if self.wait_check_error_flash_page():
                        print(self.error_content())
                    else:
                        self.base_assert.except_error('已学一单元， 点击另一单元未提示不可同时学习两个单元')
                    time.sleep(2)

                    self.click_review_word_tab()
                    if self.wait_check_error_flash_page():
                        print(self.error_content())
                    else:
                        self.base_assert.except_error('正在学习一单元，点击另一单元的自主复习， 未提示暂无复习单词，请先进行“单词学习”！')
                    break





