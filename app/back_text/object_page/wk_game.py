#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/9 13:35
# -----------------------------------------
import time
from pynput.keyboard import Controller, Key
from selenium.webdriver.common.by import By

from app.back_text.object_page.common_ele import GameCommonElePage
from conf.decorator import teststep, teststeps


class WKGame(GameCommonElePage):
    @teststep
    def wait_check_wk_game_page(self):
        locator = (By.CSS_SELECTOR, '.wk-container')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_play_btn_page(self):
        """视频播放按钮页面检查点"""
        locator = (By.CLASS_NAME, 'icon-components-triangle')
        return self.get_wait_check_page_result(locator)

    @teststep
    def video_player(self):
        """播放视频"""
        ele = self.driver.find_element_by_css_selector('.player video')
        return ele

    @teststep
    def play_btn(self):
        """视频播放按钮"""
        ele = self.driver.find_element_by_css_selector('.control .play')
        return ele

    @teststep
    def play_full_screen_btn(self):
        ele = self.driver.find_element_by_css_selector('.icon-components-zoom-in-frame')
        return ele

    @teststep
    def video_process(self):
        """视频长度"""
        ele = self.driver.find_element_by_css_selector('.line .bg')
        return ele

    @teststep
    def process_dot(self):
        """播放进度点"""
        ele = self.driver.find_element_by_css_selector('.dot')
        return ele

    @teststeps
    def wk_game_operate(self):
        print('======== 微课 ========\n')
        start_time = round(time.time())
        while self.wait_check_wk_game_page():
            small_image_size = self.video_player().size
            self.play_full_screen_btn().click()
            time.sleep(2)
            big_image_size = self.video_player().size
            keyboard = Controller()
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)

            time.sleep(2)
            print('初始视频大小：', small_image_size)
            print('放大视频大小：', big_image_size)
            if big_image_size['width'] < small_image_size['width']:
                self.base_assert.except_error('视频放大后长度未发生变化')
            else:
                print('视频放大长度校验成功')

            self.play_btn().click()
            time.sleep(3)

            while 'disabled' in self.commit_btn().get_attribute('class'):
                time.sleep(3)

            self.commit_btn().click()
        used_time = round(time.time()) - start_time
        return used_time



