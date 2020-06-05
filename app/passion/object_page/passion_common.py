#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/17 17:13
# -----------------------------------------
from selenium.webdriver.common.by import By

from app.common_ele.common_page import CommonElePage
from conf.decorator import teststep


class PassionCommonEle(CommonElePage):

    @teststep
    def wait_check_img_page(self):
        """图片页面 检查点"""
        locator = (By.CSS_SELECTOR, '.image-wrapper')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_hk_wrap_page(self):
        """游戏页面检查点"""
        locator = (By.CSS_SELECTOR, '.quizes-wrap')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_explain_page(self):
        """小节练习单选解析页面检查点"""
        locator = (By.CSS_SELECTOR, '.explain')
        return self.get_wait_check_page_result(locator)

    @teststep
    def game_container(self):
        """获取container"""
        ele = self.driver.find_element_by_css_selector(".hk-dialog-wrap div[class$='container']")
        return ele.get_attribute('class')

    @teststep
    def next_btn(self):
        """下一步按钮"""
        ele = self.driver.find_element_by_css_selector('.icon-arrow-right')
        return ele

    @teststep
    def small_image(self):
        """题目中的图片"""
        ele = self.driver.find_element_by_css_selector('.image-wrapper')
        return ele

    @teststep
    def zoom_in_icon(self):
        """图片放大按钮"""
        ele = self.driver.find_element_by_css_selector('.el-icon-zoom-in')
        return ele

    @teststep
    def big_img(self):
        """放大后的图片"""
        ele = self.driver.find_element_by_css_selector('div[style~="position:"] img:nth-child(1)')
        return ele

    @teststep
    def close_big_img_icon(self):
        """放大图片后关闭按钮"""
        ele = self.driver.find_element_by_css_selector('div[style~="position:"] img:nth-child(2)')
        return ele
