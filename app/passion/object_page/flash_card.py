#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/17 16:36
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.passion.object_page.passion_common import PassionCommonEle
from conf.decorator import teststep


class FlashGame(PassionCommonEle):

    @teststep
    def wait_check_flash_card_page(self):
        """闪卡页面检查点"""
        locator = (By.CSS_SELECTOR, '.zsd-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def knowledge_text(self):
        """知识点文本"""
        ele = self.driver.find_element_by_css_selector('.bq-wrap')
        return ele.text

    @teststep
    def answer_content(self):
        """正确答案"""
        ele = self.driver.find_elements_by_css_selector('.answer')
        return ele

    @teststep
    def flash_game_operate(self):
        """闪卡游戏处理"""
        print('========= 闪卡游戏 =========\n')
        right_answer = {}
        while self.wait_check_flash_card_page():
            bank_id = self.bank_id()
            knowledge_text = self.knowledge_text()
            print(knowledge_text, '\n')
            answer_text = self.answer_content()
            right_answer[bank_id] = [x.text.strip() for x in answer_text]
            self.next_btn().click()
            time.sleep(2)
        print('正确答案：', right_answer)
        print('-'*30, '\n')
        return right_answer



