#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/16 16:35
# -----------------------------------------
import random
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.wk_game import WKGame
from app.common_ele.common_page import CommonElePage
from app.passion.object_page.passion_sql_handle import PassionSQLHandle
from conf.decorator import teststep


class ChapterPage(CommonElePage):

    def __init__(self):
        self.data = PassionSQLHandle()

    @teststep
    def wait_chapter_page(self):
        """章节目录页面检查点"""
        locator = (By.CSS_SELECTOR, '.chapter-list')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_chapter_video_page(self):
        """章节导学视频按钮页面检查点"""
        locator = (By.CSS_SELECTOR, '.video-entry')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_video_page(self):
        """视频页面检查点"""
        locator = (By.CSS_SELECTOR, '.player')
        return self.get_wait_check_page_result(locator)

    @teststep
    def chapter_list(self):
        """章节目录列表"""
        ele = self.driver.find_elements_by_css_selector('.chapter-list li')
        return ele

    @teststep
    def chapter_finish_status(self):
        """章节完成列表"""
        ele = self.driver.find_element_by_css_selector('.content .total div:nth-child(1) p:nth-child(1)')
        return ele.text.strip()

    @teststep
    def section_num(self):
        """小节个数"""
        ele = self.driver.find_element_by_css_selector('.total p:nth-child(1) span')
        return int(ele.text)

    @teststep
    def knowledge_num(self):
        """知识点个数"""
        ele = self.driver.find_element_by_css_selector('.total p:nth-child(2) span')
        return int(ele.text)

    @teststep
    def chapter_exam_score(self):
        """章考核分数"""
        ele = self.driver.find_element_by_css_selector('.total p:nth-child(3) span')
        return ele.text

    @teststep
    def order_study_btn(self):
        """顺序学习按钮"""
        ele = self.driver.find_element_by_css_selector('.content .right .el-button:nth-child(1)')
        return ele

    @teststep
    def chapter_exam_btn(self):
        """章节考试"""
        ele = self.driver.find_element_by_css_selector('.content .right .el-button:nth-child(2)')
        return ele

    @teststep
    def section_progress_list(self):
        """小节学习进度"""
        ele = self.driver.find_elements_by_css_selector('.progress')
        return [x.text.strip() for x in ele]

    @teststep
    def chapter_video_btn(self):
        """章节导学视频按钮"""
        ele = self.driver.find_element_by_css_selector('.icon-video')
        return ele

    @teststep
    def section_father_box_ele(self):
        """小节父级元素"""
        ele = self.driver.find_elements_by_css_selector('.section')
        return ele

    @teststep
    def section_progress(self, section_ele):
        """小节进度"""
        ele = section_ele.find_element_by_css_selector('.status')
        return ele.text.strip()

    @teststep
    def section_name(self, section_ele):
        """小节名称"""
        ele = section_ele.find_element_by_css_selector('p')
        return ele.text

    @teststep
    def section_knowledge_btn(self, section_ele):
        """知识点识记"""
        ele = section_ele.find_elements_by_css_selector('a')
        return ele[3]

    @teststep
    def section_sync_exercise(self, section_ele):
        """同步练习按钮"""
        ele = section_ele.find_elements_by_css_selector('a')
        return ele[2]

    @teststep
    def section_printer_icon(self, section_ele):
        """打印按钮"""
        ele = section_ele.find_element_by_css_selector('.icon-printer')
        return ele

    @teststep
    def more_section_sync_btn(self, section_ele):
        """更多同步练习按钮"""
        ele = section_ele.find_element_by_css_selector('.icon-list')
        return ele

    # ===== 章节目录页面元素和数据校验 =====
    @teststep
    def chapter_num_check(self, book_id, chapter_num):
        """主页页面章节个数校验"""
        db_chapter_num = self.data.get_book_chapter_num(book_id)
        if db_chapter_num != chapter_num:
            self.base_assert.except_error('主页页面章节个数与数据库查询个数不一致')

    @teststep
    def check_chapter_is_available(self, book_id):
        """判断章节状态是否正确"""
        active_chapter = []
        for x in self.chapter_list():
            chapter_info = self.data.get_chapter_id_and_available_value(book_id, x.text.strip())
            print(x.text, chapter_info)
            if chapter_info[1]:
                if 'disable' in x.get_attribute('class'):
                    self.base_assert.except_error('此章节为上架状态， 但是页面显示不可点击 ' + x.text)
                else:
                    active_chapter.append((x, chapter_info[0]))
            else:
                if 'active' in x.get_attribute('class'):
                    self.base_assert.except_error('此章节为下架状态, 但是页面显示可点击 ' + x.text)
        print('-'*30, '\n')
        return active_chapter

    @teststep
    def check_shelves_chapter_data(self, book_id, chapter_id):
        """对已上架的章节的导学、小节、知识点进行验证"""
        chapter_has_video = self.data.get_chapter_have_video(chapter_id)
        if chapter_has_video:
            if not self.wait_check_chapter_video_page():
                self.base_assert.except_error("查询得本章节具有章节导学视频， 但是页面没有导学显示")
            # else:
            #     self.chapter_video_btn().click()
            #     if not self.wait_check_video_page():
            #         self.base_assert.except_error('点击章节导学按钮， 未出现视频页面')
            #     else:
            #         WKGame().wk_game_operate()
        else:
            if self.wait_check_chapter_video_page():
                self.base_assert.except_error("查询得本章节不具有章节导学视频， 但是页面却显示")

        section_num = self.section_num()
        db_section_info = self.data.get_chapter_section_ids(chapter_id)
        active_section_id = [x[0] for x in db_section_info if x[1]]
        print('本章节所有小节id', db_section_info)
        print('本章节已上架小节id', active_section_id)
        print('页面小节数：', section_num)
        print('数据库查询小节数：', len(db_section_info))
        if len(db_section_info) != section_num:
            self.base_assert.except_error("查询到的小节数与页面展示的个数不一致，查询为 %d, 页面为 %d" % (len(db_section_info), section_num))

        knowledge_num = self.knowledge_num()
        db_knowledge_num = sum([self.data.get_section_knowledge_num_by_id(book_id, x) for x in active_section_id])
        print('页面知识点数：', knowledge_num)
        print('数据库查询知识点总数：', db_knowledge_num)
        if db_knowledge_num != knowledge_num:
            self.base_assert.except_error('查询到的知识点个数与页面显示个数不一致， 查询为%d, 页面为%d' % (db_knowledge_num, knowledge_num))
        print('-' * 30, '\n')
        return chapter_id

    @teststep
    def check_chapter_finish_status(self):
        """校验章节完成状态"""
        chapter_status = self.chapter_finish_status()
        section_progress_list = self.section_progress_list()
        # if '已完成' in chapter_status:
        #     if '100%' not in section_progress_list:
        #         self.base_assert.except_error("小节中不存在已完成状态，")
        pass

    @teststep
    def check_section_available_status(self, book_id, chapter_id):
        """校验小节知识点状态"""
        active_section_index = []
        section_list = self.section_father_box_ele()
        print('小节个数：', len(section_list))
        for i in range(len(section_list)):
            if self.wait_chapter_page():
                section_ele = self.section_father_box_ele()[i]
                section_name = self.section_name(section_ele)
                section_info = self.data.get_chapter_id_and_available_value(book_id, section_name, chapter_id)
                print(section_name, section_info)
                section_id = section_info[0]
                section_ava_value = section_info[1]
                sync_exercise_btn = self.section_sync_exercise(section_ele)
                more_exercise_btn = self.more_section_sync_btn(section_ele)
                for ele in [sync_exercise_btn, more_exercise_btn]:
                    if 'active' not in ele.get_attribute('class'):
                        sync_exercise_btn.click()
                        if self.wait_check_error_tip_page():
                            print(self.error_content())
                        else:
                            self.base_assert.except_error("小节未开始，点击按钮未提示请先完成小节练习/同步练习")
                        time.sleep(3)

                self.section_knowledge_btn(section_ele).click()
                if section_ava_value:
                    if self.wait_check_error_tip_page():
                        print(self.error_content())

                    if not self.wait_check_start_study_page():
                        self.base_assert.except_error("小节已上架，点击知识点识记未出现开始学习页面")
                    else:
                        active_section_index.append((i, section_id))
                        self.exit_icon().click()
                        time.sleep(3)
                else:
                    if self.wait_check_error_tip_page():
                        print(self.error_content())
                    else:
                        self.base_assert.except_error('小节已下架， 点击知识点识记未出现错误提示')
        print('-' * 30, '\n')
        return active_section_index




