#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/10 10:02
# -----------------------------------------
import datetime
import time
from selenium.webdriver.common.by import By

from app.back_text.object_page.back_text_exam import BackTextExam
from app.back_text.object_page.cloze_text import ClozeText
from app.back_text.object_page.complete_text import CompleteText
from app.back_text.object_page.listen_choice import ListenChoice
from app.back_text.object_page.listen_sentence import ListenSentence
from app.back_text.object_page.listen_text import ListenText
from app.back_text.object_page.read_understan_text import ReadUnderStandText
from app.back_text.object_page.restore_word import RestoreWord
from app.back_text.object_page.select_blank import SelectWordBlank
from app.back_text.object_page.sentence_reform import SentenceReform
from app.back_text.object_page.sentence_strengthen import SentenceStrengthen
from app.back_text.object_page.single_choice import SingleChoice
from app.back_text.object_page.follow_speak import FollowSpeaking
from app.back_text.object_page.wk_game import WKGame
from app.back_text.object_page.common_ele import GameCommonElePage
from app.back_text.object_page.flash_card import FlashCard
from app.back_text.object_page.listen_spell import ListenSpell
from app.back_text.object_page.word_choice import WordChoice
from app.back_text.object_page.word_spell import WordSpell
from conf.decorator import teststep, teststeps


class BackTextPage(GameCommonElePage):

    @teststep
    def wait_check_back_text_page(self):
        """背课文页面检查点"""
        locator = (By.CLASS_NAME, "breadcrumb")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_error_tip_page(self):
        """错误信息提示"""
        locator = (By.CLASS_NAME, "el-message__content")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_tip_box_page(self):
        """弹窗信息页面检查点"""
        locator = (By.CLASS_NAME, "el-message-box__content")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_module_page(self):
        """模块夜面检查点"""
        locator = (By.CSS_SELECTOR, ".module")
        return self.get_wait_check_page_result(locator)


    @teststep
    def wait_check_bank_tip_page(self):
        """题型提示页面检查点"""
        locator = (By.CLASS_NAME, "ready")
        return self.get_wait_check_page_result(locator)

    @teststep
    def into_english_course(self):
        """进入课程"""
        ele = self.driver.find_elements_by_css_selector('.renew')
        ele[0].click()

    @teststep
    def unit_name_list(self):
        """单元名称列表"""
        ele = self.driver.find_elements_by_class_name('unit-name')
        return ele

    @teststep
    def unit_status(self):
        """ 单元学习状态"""
        ele = self.driver.find_elements_by_class_name('status')
        return ele

    @teststep
    def module_list(self):
        """练习列表"""
        ele = self.driver.find_elements_by_class_name('module-name')
        return ele

    @teststep
    def module_study_btn(self, module_ele):
        """根据练习名称获取新学按钮"""
        ele = module_ele.find_elements_by_xpath('./following-sibling::div/button')
        return ele[0]

    @teststep
    def module_review_btn(self, module_ele):
        """根据练习名称获取复习按钮"""
        ele = module_ele.find_elements_by_xpath('./following-sibling::div/button')
        return ele[1]

    @teststep
    def ready_text(self):
        """即将开始学习"""
        ele = self.driver.find_element_by_css_selector('.ready h2')
        return ele.text

    @teststep
    def start_study_btn(self):
        """开始学习"""
        ele = self.driver.find_element_by_css_selector('.ready .el-button')
        return ele


    @teststep
    def alert_tip_content(self):
        """弹窗信息提示"""
        ele = self.driver.find_element_by_class_name('el-message-box__content')
        return ele.text

    @teststep
    def tip_confirm_btn(self):
        """弹框提示确定按钮"""
        ele = self.driver.find_element_by_css_selector('.el-message-box__btns .el-button')
        return ele

    @teststep
    def ready_exit_btn(self):
        """开始页面退出按钮"""
        ele = self.driver.find_element_by_css_selector('.exit .icon-exit')
        return ele

    @teststeps
    def alert_tip_operate(self):
        if self.wait_check_tip_box_page():
            print("弹框提示内容：", self.alert_tip_content(), '\n')
            self.tip_confirm_btn().click()
            time.sleep(2)


    @teststep
    def check_second_enter_bank(self, unit_index=0):
        """二次进入新学"""
        if self.wait_check_module_page():
            time.sleep(1)
            self.unit_name_list()[unit_index].click()
            time.sleep(2)
            self.module_study_btn(self.module_list()[0]).click()
            time.sleep(2)
            if self.wait_check_bank_tip_page():
                self.start_study_btn().click()
                time.sleep(2)
                if 'jxzh_container' not in self.game_container_mode()[0]:
                    self.base_assert.except_error('中途退出，再次进入的大题不是上次退出的大题')
                else:
                    print('\n中途退出校验成功')
                    self.game_exit_btn().click()
                    time.sleep(2)
        else:
            self.base_assert.except_error("中途退出，再次进入没有出现题型提示页面")

    @teststeps
    def game_operate(self, half_exit=False):
        """游戏全过程
           提示内容包含测试，则转至试卷功能
           其他游戏则直接进入游戏过程
        """
        start_time = round(time.time())
        time_msg = {"结束时间": '', '大题时间': {}, '总用时': 0}
        bank_time = time_msg['大题时间']
        if self.wait_check_bank_tip_page():
            ready_text = self.ready_text()
            print(ready_text, '\n')
            self.start_study_btn().click()
            time.sleep(3)
            if '有练有测' in ready_text:
                exam_info = BackTextExam().exam_operate()
                BackTextExam().exam_operate(exam_info)
            else:
                while self.wait_check_container_page():
                    game_container, mode = self.game_container_mode()
                    if 'dx-container' in game_container:
                        bank_time['单项选择'] = SingleChoice().single_choice_game_process()

                    elif 'jxzh-container' in game_container:
                        bank_time['句型转换'] = SentenceReform().sentence_reform_game_process()

                    elif 'qhlj-container' in game_container:
                        bank_time['强化炼句'] = SentenceStrengthen().sentence_strength_game_process()

                    elif 'tylj-container' in game_container:
                        bank_time['听音连句'] = ListenSentence().listen_sentence_game_process()

                    elif 'bqwz-container' in game_container:
                        bank_time['补全文章'] = CompleteText().complete_text_game_process()

                    elif 'xctk-container' in game_container:
                        bank_time['选词填空'] = SelectWordBlank().select_word_blank_game_operate()

                    elif 'med-container' in game_container:
                        bank_time['磨耳朵'] = ListenText().listening_text_game_process()

                    elif 'ky-container' in game_container:
                        bank_time['口语跟读'] = FollowSpeaking().speaking_game_process()

                    elif 'wk-container' in game_container:
                        bank_time['微课'] = WKGame().wk_game_operate()

                    elif 'dctx-container' in game_container:
                        bank_time['单词听写'] = ListenSpell().listen_spell_operate()

                    elif 'chxz-container' in game_container:
                        bank_time['词汇选择'] = WordChoice().word_choice_game_operate()

                    elif 'sk-container' in game_container:
                        if mode == '1':
                            bank_time['闪卡学习'] = FlashCard().flash_normal_operate()
                        elif mode == '2':
                            bank_time['闪卡抄写'] = FlashCard().flash_copy_operate()

                    elif 'hydc-container' in game_container:
                        bank_time['还原单词'] = RestoreWord().word_restore_operate()

                    elif 'dcpx-container' in game_container:
                        bank_time['单词默写'] = WordSpell().word_spell_game_operate()

                    elif 'wxtk-container' in game_container:
                        bank_time['完形填空'] = ClozeText().cloze_text_game_operate()

                    elif 'ydlj-container' in game_container:
                        bank_time['阅读理解'] = ReadUnderStandText().read_understand_game_operate()

                    elif 'thxz-container' in game_container:
                        bank_time['听后选择'] = ListenChoice().listen_choice_game_operate()
                    else:
                        break
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        used_time = round(time.time()) - start_time
        time_msg['结束时间'] = end_time
        time_msg['总用时'] = used_time
        print('本次做题用时：', time_msg)
