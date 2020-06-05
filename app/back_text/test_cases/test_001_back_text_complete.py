#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/11 15:27
# -----------------------------------------
import time
import unittest

from ddt import ddt, data

from app.back_text.object_page.back_text_sql_handle import BackTextSqlHandle
from app.back_text.object_page.common_ele import GameCommonElePage
from app.common_ele.account import *
from app.back_text.object_page.back_text_page import BackTextPage
from app.common_ele.login_page import LoginPage
from app.common_ele.select_course import SelectCoursePage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.get_attr import GetAttribute

@ddt
class TestBackText(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.back_text = BackTextPage()
        cls.game = GameCommonElePage()
        BasePage().set_assert(cls.base_assert)
        cls.login.login_status(SCHOOL_CODE, SCHOOL_PASSWORD,
                               STUDENT_ACCOUNT, STU_PASSWORD)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(TestBackText, self).run(result)

    @testcase
    @data(*[x for x in range(1)])
    def test_back_text(self,  unit_index, tp=3):
        """测试背课文"""
        if self.home.wait_check_home_page():
            self.back_text.handle.clear_student_text_overview()
            self.back_text.driver.refresh()
            time.sleep(3)
            SelectCoursePage().select_course_operate('英语', card_index=1, book_index=4)

            if self.back_text.wait_check_back_text_page():
                self.back_text.unit_name_list()[unit_index].click()
                unit_status = self.back_text.unit_status()[unit_index].text
                time.sleep(1)

                if self.back_text.wait_check_module_page():
                    if '未完成' in unit_status:
                        practice_name = self.back_text.module_list()  # 获取模块列表
                        print('模块名称列表: ', [x.text for x in practice_name])
                        study_btn_class = [GetAttribute().get_class(self.back_text.module_study_btn(x)) for x in practice_name]  # 新学
                        review_btn_class = [GetAttribute().get_class(self.back_text.module_review_btn(x)) for x in practice_name]  # 复习
                        for index, btn_class in enumerate(zip(study_btn_class, review_btn_class)):
                            if index == 0:  # 判断第一模块新学、复习状态
                                if 'primary' not in btn_class[0]:
                                    self.base_assert.except_error('第一模块新学按钮未默认点亮')

                                if 'info' not in btn_class[1]:
                                    self.base_assert.except_error('第一模块复习按钮未置灰')
                            else:  # 判断其他模块新学、复习状态
                                if 'info' not in btn_class[0]:
                                    self.base_assert.except_error('非第一模块新学按钮未置灰')

                                if 'info' not in btn_class[1]:
                                    self.base_assert.except_error('非第一模块复习按钮未置灰')

                        self.back_text.module_review_btn(practice_name[0]).click()  # 点击第一个复习按钮
                        if self.back_text.wait_check_error_tip_page():
                            print(self.game.error_content())
                        else:
                            self.back_text.game_exit_btn().click()

                        time.sleep(3)
                        if len(practice_name) > 1:  # 若模块个数大于1 ，点击最后一个新学，
                            self.back_text.module_study_btn(practice_name[-1]).click()
                            if self.back_text.wait_check_error_tip_page():
                                print(self.game.error_content())
                            time.sleep(3)

                    module_ele = self.back_text.module_list()
                    module_index = 0
                    self.back_text.module_study_btn(module_ele[module_index]).click()  # 点击第一个新学
                    self.back_text.alert_tip_operate()

                    if tp == 1:  # 中途退出校验
                        self.check_half_exit_operate()

                    elif tp == 2:  # 跨单元验证进度是否保存
                        self.change_unit_exit_operate()

                    elif tp == 3:  # 完整的练习一个模块过程steps
                        self.check_complete_operate(unit_index, module_index)

    @teststeps
    def check_complete_operate(self, unit_index, module_index):
        """完整的完成模块练习"""
        self.back_text.game_operate()
        if self.back_text.wait_check_module_page():
            model_list = self.back_text.module_list()
            review_ele = self.back_text.module_review_btn(model_list[0])
            if 'primary' not in GetAttribute().get_class(review_ele):
                self.base_assert.except_error('模块新学已完成，但是复习未点亮')
            else:
                review_ele.click()
                if self.back_text.wait_check_error_tip_page():
                    print(self.back_text.error_content())
                else:
                    self.back_text.ready_exit_btn().click()
                    time.sleep(3)

            unit_status = self.back_text.unit_status()[unit_index].text
            if len(model_list) > module_index + 1:
                module_ele = self.back_text.module_list()[module_index + 1]
                module_study_btn = self.back_text.module_study_btn(module_ele)
                print("第二单元新学按钮class:", GetAttribute().get_class(module_study_btn))
                if 'primary' not in GetAttribute().get_class(module_study_btn):
                    self.base_assert.except_error("模块新学已完成，但是下一模块的新学按钮未点亮")
            else:
                if '已完成' not in unit_status:
                    self.base_assert.except_error("已完成模块的新学， 但是单元状态不是已完成（只有一个模块）")

    @teststeps
    def check_half_exit_operate(self):
        """中途退出"""
        print('中途退出操作')
        self.back_text.game_operate(half_exit=True)
        self.back_text.check_second_enter_bank()
        time.sleep(2)
        BackTextSqlHandle().update_module_date_operate()
        self.game.driver.refresh()
        time.sleep(3)
        self.back_text.module_study_btn(self.back_text.module_list()[0]).click()
        if not self.back_text.wait_check_tip_box_page():
            self.base_assert.except_error("做题时间已更改为昨天， 但是未提示重新练习")
        self.back_text.alert_tip_operate()
        self.game.game_exit_btn().click()
        print('更改时间，提示校验成功')

    @teststeps
    def change_unit_exit_operate(self):
        """跨单元退出"""
        print('单元1中途退出')
        self.back_text.game_operate(half_exit=True)
        if self.back_text.wait_check_module_page():
            print('进入单元2进行新学退出，并重新进入单元1，验证大题类型')
            self.back_text.unit_name_list()[1].click()
            time.sleep(2)
            self.back_text.module_study_btn(self.back_text.module_list()[0]).click()
            time.sleep(1)
            self.back_text.game_operate(half_exit=True)
            self.back_text.check_second_enter_bank()
            if self.back_text.wait_check_module_page():
                print('退出单元1， 重新进入单元2， 验证大题类型')
                self.back_text.check_second_enter_bank(unit_index=1)
