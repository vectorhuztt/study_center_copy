#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/25 9:02
# -----------------------------------------
import time
from selenium.webdriver import ActionChains

from conf.base_page import BasePage
from conf.decorator import teststep


class SelectCoursePage(BasePage):

    @teststep
    def select_course_btn(self):
        """选课按钮"""
        ele = self.driver.find_element_by_css_selector('.icon-book')
        return ele

    @teststep
    def course_type_list(self):
        """书籍种类列表"""
        ele = self.driver.find_elements_by_css_selector('.course-type .course-item')
        return ele

    @teststep
    def course_card_list(self):
        """获取书籍分类列表"""
        course_cards = self.driver.find_elements_by_css_selector('.card .card-content')
        return course_cards

    @teststep
    def book_list(self, course_card):
        """分类下的书籍列表"""
        book_list = course_card.find_elements_by_css_selector('.book')
        return book_list

    @teststep
    def start_study_btn(self):
        """开始学习按钮"""
        ele = self.driver.find_element_by_css_selector('.bottom .btn')
        return ele


    @teststep
    def select_course_operate(self, type_content, card_index=0, book_index=0):
        """选课的主要流程"""
        self.select_course_btn().click()
        time.sleep(2)
        for course in self.course_type_list():
            print(course.text)
            if type_content in course.text:
                course.click()
                time.sleep(2)
                course_card = self.course_card_list()[card_index]
                select_book = self.book_list(course_card)[book_index]
                ActionChains(self.driver).double_click(select_book).perform()
                break
        time.sleep(3)


