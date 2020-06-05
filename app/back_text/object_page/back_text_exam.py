#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/11/4 15:41
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.back_text.object_page.cloze_text import ClozeText
from app.back_text.object_page.complete_text import CompleteText
from app.back_text.object_page.listen_choice import ListenChoice
from app.back_text.object_page.listen_sentence import ListenSentence
from app.back_text.object_page.listen_spell import ListenSpell
from app.back_text.object_page.read_understan_text import ReadUnderStandText
from app.back_text.object_page.restore_word import RestoreWord
from app.back_text.object_page.select_blank import SelectWordBlank
from app.back_text.object_page.sentence_reform import SentenceReform
from app.back_text.object_page.sentence_strengthen import SentenceStrengthen
from app.back_text.object_page.single_choice import SingleChoice
from app.back_text.object_page.word_choice import WordChoice
from app.back_text.object_page.word_spell import WordSpell
from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.ele_attr_check import EleAttrCheck


class BackTextExam(BasePage):

    @teststep
    def wait_check_exam_page(self):
        """试卷页面检查点"""
        locator = (By.CLASS_NAME, 'time')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_answer_card_page(self):
        """答题卡页面检查点"""
        locator = (By.CSS_SELECTOR, ".answer-card")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_bank_name(self, bank_name):
        locator = (By.XPATH, '//span[text()="{}"]'.format(bank_name))
        return self.get_wait_check_page_result(locator)


    @teststep
    def answer_card_btn(self):
        """查看答案"""
        ele = self.driver.find_element_by_css_selector('.icons .icon-card')
        return ele

    @teststep
    def pre_btn(self):
        """向前按钮"""
        ele = self.driver.find_element_by_css_selector(".icon-arrow-left")
        return ele

    @teststep
    def bank_tab_list(self):
        """游戏题型列表"""
        ele = self.driver.find_elements_by_css_selector(".detail .item")
        return ele

    @teststep
    def bank_type_name(self, bank_tab):
        """题型名称"""
        ele = bank_tab.find_element_by_css_selector('.tag .el-tag')
        return ele.text

    @teststep
    def bank_index_item(self, bank_tab):
        """大题选项"""
        ele = bank_tab.find_elements_by_css_selector(".number")
        return ele

    @teststep
    def exam_score(self):
        """试卷得分"""
        ele = self.driver.find_element_by_css_selector(".score")
        return int(ele.text)

    @teststep
    def foot_btn(self):
        """交卷按钮"""
        ele = self.driver.find_elements_by_css_selector('.footer-bar-wrap:not([style $="display: none;"]) .el-button')
        return ele

    @teststep
    def click_exit_btn(self):
        """退出按钮"""
        self.driver.find_element_by_css_selector('.el-dialog__wrapper:not([style $="display: none;"]) .game-control-bar .icon-exit').click()
        time.sleep(2)

    @teststep
    def exam_detail_bank_title(self):
        """获取试卷详情页面各个大题的标题"""
        ele = self.driver.find_elements_by_css_selector(".exam-detail .title")
        return ele

    @teststep
    def bank_do_type(self, do_right, bank_index):
        """获取题目做题形式 做对 做错 检查答案"""
        do_type = 1
        if do_right == 0:
            if bank_index in [1, 2, 3]:
                do_type = 0
        return do_type

    @teststeps
    def exam_operate(self, exam_result=None):
        """试卷操作"""
        if self.wait_check_exam_page():
            if EleAttrCheck().check_ele_is_enabled(self.pre_btn()):
                self.base_assert.except_error('试卷第一题页面，前一题按钮未置灰')
            self.answer_card_btn().click()
            if self.wait_check_answer_card_page():
                bank_type_list = self.bank_tab_list()
                exam_info = exam_result if exam_result else {}
                bank_count_list, wrong_id_list = [], []

                for i in range(len(bank_type_list)):
                    bank_tab = self.bank_tab_list()[i]
                    bank_name = self.bank_type_name(bank_tab)
                    try:
                        answer_info = exam_info[bank_name]
                    except KeyError:
                        exam_info[bank_name] = {}
                        answer_info = exam_info[bank_name]

                    do_right = 1 if wrong_id_list else 0
                    bank_numbers = self.bank_index_item(bank_tab)
                    bank_count_list.append(len(bank_numbers))
                    print('===== ' + bank_name + '=====\n')

                    for j in range(len(bank_numbers)):
                        bank_number = self.bank_index_item(self.bank_tab_list()[i])[j]
                        if exam_result:
                            do_type = 1
                        else:
                            do_type = self.bank_do_type(do_right, int(bank_number.text))
                        bank_number_content = bank_number.text
                        bank_number.click()
                        mine_answer = self.different_game_operate(bank_name, do_type, wrong_id_list)
                        answer_info[bank_number_content] = mine_answer
                        time.sleep(2)
                        self.answer_card_btn().click()
                        if self.wait_check_answer_card_page():
                            bank_tab_ele = self.bank_tab_list()[i]
                            if not EleAttrCheck().check_word_is_in_class('filled', self.bank_index_item(bank_tab_ele)[j]):
                                self.base_assert.except_error('该题已做完， 但是答题卡页面显示未做' + self.bank_index_item(bank_tab_ele)[j].get_attribute('class'))
                        time.sleep(1)
                print('试卷信息：', exam_info)
                self.foot_btn()[0].click()
                WordBookPublicElePage().alert_tab_operate()
                check_turns = 2 if exam_result else 1
                self.exam_result_page_operate(bank_count_list, wrong_id_list, exam_info, check_turns)
                if 'is-disabled' not in self.foot_btn()[0].get_attribute('class'):
                    self.foot_btn()[0].click()
                else:
                    self.exit_icon().click()
                time.sleep(2)
                return exam_info

    @teststep
    def exam_result_page_operate(self, bank_count_list, wrong_id_list, exam_info, check_turns):
        """试卷结果页面操作
            :param bank_count_list 每道大题包含的题数
            :param wrong_id_list 错题列表
            :param exam_info 试卷做题信息
            :param check_turns 查看答案的次数
        """
        if self.wait_check_answer_card_page():
            exam_score = self.exam_score()
            print('得分：', exam_score, '\n')
            total_bank_count = sum(bank_count_list)
            wrong_count = len(wrong_id_list)
            cal_score = round((total_bank_count - wrong_count) / total_bank_count * 100)
            if exam_score != cal_score:
                self.base_assert.except_error("试卷得分与计算得分不一致，页面得分 %d，计算得分 %d" % (exam_score, cal_score))
            bank_type_list = self.bank_tab_list()
            count = 0
            for i in range(len(bank_type_list)):
                result_tag_ele = self.bank_tab_list()[i]
                result_bank_name = self.bank_type_name(result_tag_ele)
                answer_info = exam_info[result_bank_name]
                result_bank_numbers = self.bank_index_item(result_tag_ele)
                for j in range(len(result_bank_numbers)):
                    if self.wait_check_answer_card_page():
                        result_bank_index = self.bank_index_item(self.bank_tab_list()[i])[j]
                        number_bank_index = int(result_bank_index.get_attribute('index'))
                        number_global_index = int(result_bank_index.get_attribute('global-index'))
                        if len(wrong_id_list):
                            if count in [0, 1, 2]:
                                if EleAttrCheck().check_word_is_in_class('success', result_bank_index):
                                    self.base_assert.except_error("本题已做错，但是结果页面未显示做对 " + result_bank_name + 'index: ' + result_bank_index.text)
                            else:
                                if EleAttrCheck().check_word_is_in_class('danger', result_bank_index):
                                    self.base_assert.except_error("本题已做对，但是结果页面未显示错 " + result_bank_name + 'index: ' + result_bank_index.text)
                        else:
                            if EleAttrCheck().check_word_is_in_class('danger', result_bank_index):
                                self.base_assert.except_error("本题已做对，但是结果页面未显示错 " + result_bank_name + 'index: ' + result_bank_index.text)

                        self.driver.execute_script("document.getElementsByClassName('item')[{}]."
                                                   "getElementsByClassName('number')[{}].click()".format(i, j))
                        # self.bank_index_item(self.bank_tab_list()[i])[j].click()
                        time.sleep(1)
                        mine_answer = answer_info[str(j + 1)]
                        if result_bank_name in ['单项选择', '单词听写']:
                            result_index = number_bank_index
                        else:
                            result_index = number_global_index
                        if mine_answer:
                            if '未作答' in self.exam_detail_bank_title()[count].text:
                                self.base_assert.except_error("本题已作答，但是结果页显示未作答")
                        else:
                            if '未作答' not in self.exam_detail_bank_title()[count].text:
                                self.base_assert.except_error("本题未作答，但是结果页显示已作答")
                        self.different_game_operate(result_bank_name, 2, wrong_id_list, do_count=check_turns,
                                                    check_answer=mine_answer, result_index=result_index)
                        self.foot_btn()[0].click()
                        count += 1
                        time.sleep(1)

    @teststeps
    def different_game_operate(self, bank_name, do_type, wrong_id_list, do_count=1,  check_answer=None, result_index=None):
        """不同游戏的操作过程
            :param result_index: 结果页container index
            :param bank_name: 大题名称
            :param do_type: 做题形式 0：做错 1：做对 2：检查答案
            :param wrong_id_list: 错题id列表
            :param do_count 试卷做题次数, 默认为1
            :param check_answer: 做试卷时的答案
        """
        mine_answer, game_mode = 0, 0
        if bank_name == '单项选择':
            mine_answer = SingleChoice().single_choice_exam_process(do_type, wrong_id_list, check_answer, result_index)

        elif bank_name == "还原单词":
            mine_answer = RestoreWord().word_restore_exam_operate(do_type, wrong_id_list, check_answer, result_index)

        elif bank_name == '句型转换':
            mine_answer = SentenceReform().sentence_reform_exam_process(do_type, wrong_id_list, check_answer, result_index)

        elif "强化炼句" in bank_name:
            mine_answer = SentenceStrengthen().sentence_strength_exam_process(do_type, wrong_id_list, check_answer, result_index)

        elif bank_name == "听音连句":
            mine_answer = ListenSentence().listen_sentence_exam_operate(do_type, wrong_id_list, check_answer, result_index)

        elif bank_name == '听音选词':
            mine_answer = WordChoice().word_choice_exam_operate(do_type,  wrong_id_list, check_answer, result_index)

        elif bank_name == "听音选译":
            mine_answer = WordChoice().word_choice_exam_operate(do_type,  wrong_id_list, check_answer, result_index)

        elif bank_name == '单词听写':
            mine_answer = ListenSpell().listen_spell_exam_operate(do_type, wrong_id_list, check_answer, result_index)

        elif bank_name == '阅读理解':
            mine_answer = ReadUnderStandText().read_understand_exam_operate(do_type, wrong_id_list, check_answer, result_index, do_count)

        elif bank_name == '选词填空':
            mine_answer = SelectWordBlank().select_word_blank_game_exam_operate(do_type, wrong_id_list, check_answer, result_index)

        elif bank_name == '补全文章':
            mine_answer = CompleteText().complete_article_exam_operate(do_type, wrong_id_list, check_answer, result_index, do_count)

        elif bank_name == '完形填空':
            mine_answer = ClozeText().cloze_exam_operate(do_type, wrong_id_list, check_answer, result_index, do_count)

        elif '单词拼写' in bank_name:
            mine_answer = WordSpell().word_spell_exam_operate(do_type, wrong_id_list, check_answer, result_index)

        elif "词汇选择" in bank_name:
            mine_answer = WordChoice().word_choice_exam_operate(do_type,  wrong_id_list, check_answer, result_index)

        elif bank_name == '听后选择':
            mine_answer = ListenChoice().listen_choice_exam_operate(do_type, wrong_id_list, check_answer, result_index, do_count)

        return mine_answer







