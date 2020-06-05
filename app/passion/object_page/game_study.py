#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/18 10:07
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.passion.object_page.complete_text import CompleteTextGame
from app.passion.object_page.fill_blank_game import FillBlankGame
from app.passion.object_page.flash_card import FlashGame
from app.passion.object_page.passion_common import PassionCommonEle
from app.passion.object_page.passion_sql_handle import PassionSQLHandle
from app.passion.object_page.single_choice import SingleChoiceGame
from conf.decorator import teststep, teststeps


class GameStudy(PassionCommonEle):
    """知识点识记"""
    def __init__(self):
        self.data = PassionSQLHandle()

    @teststep
    def wait_check_another_group_page(self):
        """再来一组页面检查点"""
        locator = (By.XPATH, '//p[contains(text(),"再来一组")]')
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_complete_knowledge_page(self):
        """完成知识点页面检查的点"""
        locator = (By.XPATH, '//p[contains(text(),"复习一遍")]')
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_complete_section_page(self):
        """小节练习完成页面检查点"""
        locator = (By.XPATH, '//p[contains(text(),"完成本节同步练习")]')
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_start_knowledge_page(self):
        """知识点开始页面检查点"""
        locator = (By.XPATH, '//p[contains(text(),"学习知识点")]')
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_start_section_page(self):
        """小节练习开始页面检查点"""
        locator = (By.XPATH, '//p[contains(text(),"完成本小节知识点")]')
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_complete_chapter_page(self):
        """小节练习开始页面检查点"""
        locator = (By.XPATH, '//p[contains(text(),"学完了本章知识点")]')
        return self.get_wait_check_page_result(locator, timeout=3)


    @teststeps
    def section_knowledge_operate(self, wrong_note, is_half_exit=False, do_right=False, is_order_study=False):  # 进入游戏过程
        right_answer, exit_text,  = 0, 0
        wrong_blank_list = {}
        blank_wrong_counter = [0]
        interval_counter = []
        while self.wait_check_hk_wrap_page():
            attr = self.game_container()
            if attr == 'zsd-container':  # 闪卡练习
                right_answer = FlashGame().flash_game_operate()

            elif attr == 'xt-container':  # 补全文章
                CompleteTextGame().complete_text_operate(right_answer)

            elif attr == 'bq-container':  # 填空
                bank_count = len(list(right_answer.keys()))
                FillBlankGame().fill_blank_operate(do_right, bank_count=bank_count, answer_info=right_answer,
                                                   interval_counter=interval_counter, wrong_note=wrong_note,
                                                   wrong_counter=blank_wrong_counter, wrong_bank_info=wrong_blank_list)

            if self.wait_check_another_group_page():
                if not is_order_study:
                    exit_text = self.start_text()
                print(self.start_text(), '\n')
                if is_half_exit:
                    self.exit_icon().click()
                    time.sleep(2)
                    break
                else:
                    self.click_start_button()
                    time.sleep(2)
                    self.section_knowledge_operate(wrong_note, is_half_exit=False, do_right=do_right,
                                                   is_order_study=is_order_study)

            if not is_order_study:
                if self.wait_check_complete_knowledge_page():
                    print(self.start_text(), '\n')
                    self.exit_icon().click()
                    time.sleep(2)
                    break
            else:
                if self.wait_check_start_section_page():
                    exit_text = self.start_text()
                    print('='*10 + "同步练习提示" + '='*10, '\n')
                    print(exit_text, '\n')
                    self.exit_icon().click()
                    time.sleep(2)
                    break
        print('小节退出提示：', exit_text, '\n')
        return exit_text

    @teststeps
    def section_sync_operate(self, wrong_note, is_half_exit=False, section_id=0, do_right=False, is_order_study=False):
        """同步练习操作"""
        dx_bank_count, tk_bank_count = 0, 0
        interval_counter = []
        dx_wrong_counter, tk_wrong_counter = [0], [0]
        wrong_bank_info, wrong_choice_info = {}, {}
        exit_id, exit_text = 0, 0
        if not is_order_study:
            dx_bank_count, tk_bank_count  = self.data.get_section_sync_ques(section_id)
            print('该小节第一组单选总题数：', dx_bank_count)
            print('该小节第一组填空总题数：', tk_bank_count, '\n')

        while self.wait_check_hk_wrap_page():
            attr = self.game_container()
            if attr == 'dx-container':
                exit_id = SingleChoiceGame().\
                    section_single_choice_operate(all_do_right=do_right, is_half_exit=is_half_exit,
                                                  interval_counter=interval_counter, bank_count=dx_bank_count,
                                                  wrong_counter=dx_wrong_counter, wrong_note=wrong_note,
                                                  wrong_choice_info=wrong_choice_info)

            elif attr == 'bq-container':
                exit_id = FillBlankGame().fill_blank_operate(all_do_right=do_right, is_half_exit=is_half_exit,
                                                             bank_count=tk_bank_count, interval_counter=interval_counter,
                                                             wrong_note=wrong_note, wrong_counter=tk_wrong_counter,
                                                             wrong_bank_info=wrong_bank_info)

            if self.wait_check_complete_section_page():  # 新的一组开始学习
                print(self.start_text())
                self.exit_icon().click()
                time.sleep(2)
                break

            if is_order_study:
                if self.wait_check_start_knowledge_page() or self.wait_check_complete_chapter_page():
                    exit_text = self.start_text()
                    print(exit_text, '\n')
                    self.exit_icon().click()
                    time.sleep(2)
                    break
        if not do_right:
            print(interval_counter)
            self.interval_counter_check(interval_counter, dx_bank_count, tk_bank_count)
        return exit_id, exit_text

    @teststep
    def interval_counter_check(self, interval_counter, select_count, blank_count):
        bank_type = [x[0] for x in interval_counter]
        bank_id = [x[1] for x in interval_counter]
        if select_count and blank_count:
            if select_count < 2:
                if blank_count > 1:
                    if bank_type != ['选择', '填空', '填空', '填空', '填空', '填空']:
                        self.base_assert.except_error('选择题数为1,填空题大于1,统计间隔与计算间隔不一致')
                elif blank_count == 1:
                    if bank_type != ['选择', '填空']:
                        self.base_assert.except_error('选择题数为1,填空题为1,统计间隔与计算间隔不一致')
            else:
                if blank_count == 1:
                    if bank_id[0] != bank_id[3]:
                        self.base_assert.except_error('错题间隔不正确')
                    if bank_type[2] != '填空':
                        self.base_assert.except_error('选择错题之间未发现填空题')
                else:
                    split_bank_id = bank_id[:7]
                    for i, x in enumerate(split_bank_id):
                        if i % 3 == 0:
                            if x != bank_id[0]:
                                self.base_assert.except_error('错题间隔有误， 该题应为{}， 实际为{}'.format(bank_id[0], x))
                        if i % 3 == 2:
                            if bank_type[i] != '填空':
                                self.base_assert.except_error('选择错题间隔中未夹杂填空题')





