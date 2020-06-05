#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/25 9:32
# -----------------------------------------
import re
import time

from selenium.webdriver.common.by import By
from app.back_text.object_page.back_text_sql_handle import BackTextSqlHandle
from app.common_ele.common_page import CommonElePage
from conf.decorator import teststep


class GameCommonElePage(CommonElePage):

    def __init__(self):
        self.handle = BackTextSqlHandle()

    @teststep
    def wait_check_container_page(self):
        """容器页面元素检查点"""
        locator = (By.CSS_SELECTOR, '.component-wrap div[class$= "container"]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def get_result_index_content(self, container_ele):
        """结果页题号内容"""
        ele = container_ele.find_element_by_xpath('//preceding-sibling::div[@class="title"]')
        return ele.text

    @teststep
    def bank_count(self):
        """题目个数"""
        ele = self.driver.find_element_by_css_selector('.van-dialog')
        return int(ele.get_attribute('data-exercise-count'))

    @teststep
    def game_container_mode(self):
        """游戏容器名称 和mode"""
        ele = self.driver.find_element_by_css_selector('.component-wrap div[class$= "container"]')
        container = ele.get_attribute('class')
        mode = ele.get_attribute('mode')
        return container, mode

    @teststep
    def game_exit_btn(self):
        """游戏上方退出按钮"""
        ele = self.driver.find_element_by_css_selector('.el-dialog__wrapper:not([style $="display: none;"]) .game-control-bar .icon-exit')
        return ele

    @teststep
    def exam_time(self, container_ele):
        """试卷已用时间"""
        ele = container_ele.find_element_by_css_selector('.time')
        time_num = [int(x) for x in re.findall(r'\d+', ele.text)]
        return (time_num[0]*10+time_num[1])*60 + (time_num[2]*10 + time_num[3])

    @teststep
    def exam_time_judge(self, timer):
        if len(timer) > 1:
            if any(timer[i + 1] > timer[i] for i in range(0, len(timer) - 1)):
                print('计时功能无误:', timer, '\n')
                return True
            else:
                self.base_assert.except_error('Error - 计时错误:' + str(timer) + '\n')
        else:  # 只有一道题
            print('只有一道题，时间为:', timer[0], '\n')
            return True

    @teststep
    def zoom_image_btn(self):
        ele = self.driver.find_element_by_css_selector('.icon-components-zoom-in')
        return ele

    @teststep
    def big_image(self):
        """放大图片"""
        ele = self.driver.find_element_by_css_selector('.big-imge img')
        return ele

    @teststep
    def check_image_zoom_size(self, small_image):
        small_image_size = small_image().size
        self.zoom_image_btn().click()
        time.sleep(1)
        big_image_size = self.big_image().size
        self.big_image().click()
        time.sleep(2)
        print('初始图片大小：', small_image_size)
        print('放大后图片大小：', big_image_size)

        if big_image_size['width'] < small_image_size['width']:
            self.base_assert.except_error('图片放大后长度未发生变化')

        if big_image_size["height"] < small_image_size["height"]:
            self.base_assert.except_error("图片放大后宽度未发生变化")

    @teststep
    def check_wrong_bank_interval(self, bank_count, bank_list, wrong_bank_id):
        """校验错题间隔"""
        wrong_index = [i for i, x in enumerate(bank_list) if x == str(wrong_bank_id)]
        if bank_count == 1:
            wrong_index_list = [0, 1, 2]
        elif bank_count == 2:
            wrong_index_list = [0, 2, 3]
        elif bank_count == 3:
            wrong_index_list = [0, 3, 4]
        elif bank_count == 4:
            wrong_index_list = [0, 3, 5]
        else:
            wrong_index_list = [0, 3, 6]

        if wrong_index_list != wrong_index:
            self.base_assert.except_error("❌❌❌ 错题的间隔不为2")
