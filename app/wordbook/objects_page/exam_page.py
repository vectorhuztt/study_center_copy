#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/5 15:11
# -----------------------------------------
import random, string, time
from selenium.webdriver.common.by import By

from app.back_text.object_page.listen_spell import ListenSpell
from app.back_text.object_page.word_choice import WordChoice
from app.back_text.object_page.word_spell import WordSpell
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep, teststeps


class ExamPage(WordBookPublicElePage):
    def __init__(self):
        self.home = WordHomePage()
        self.data = WordBookSqlHandle()
        self.vocab = WordChoice()
        self.listen_spell = ListenSpell()
        self.spell = WordSpell()

    @teststep
    def wait_check_exam_bank_type_page(self):
        """选择测试题型页面检查点"""
        locator = (By.CSS_SELECTOR, ".el-checkbox-group")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_exam_type_page(self):
        """选择测试题型页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, ".word-centent")
        return self.wait.wait_check_element(locator)


    @teststep
    def wait_check_answer_card_page(self):
        """答题卡页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, ".answer-card")
        return self.wait.wait_check_element(locator)

    @teststep
    def tab_content(self):
        """页面内容"""
        locator = (By.CSS_SELECTOR, ".word-centent")
        return self.wait.wait_find_element(locator).text

    @teststep
    def exam_labels(self):
        """今日已学单词个数"""
        locator = (By.CSS_SELECTOR, ".el-radio-group .el-radio")
        return self.wait.wait_find_elements(locator)

    @teststep
    def label_buttons(self):
        """测试类型按钮"""
        locator = (By.CSS_SELECTOR, ".btn-control .el-button")
        return self.wait.wait_find_elements(locator)

    @teststep
    def online_test_btn(self):
        """在线测试"""
        locator = (By.CSS_SELECTOR, ".btn-control .el-button:first-child")
        return self.wait.wait_find_element(locator)

    @teststep
    def unit_listening_btn(self):
        """单元听写"""
        locator = (By.CSS_SELECTOR, ".btn-control .el-button:nth-child(4)")
        return self.wait.wait_find_element(locator)

    @teststep
    def bank_type_checkbox(self):
        """题型选项"""
        locator = (By.CSS_SELECTOR, ".el-checkbox-group .el-checkbox")
        return self.wait.wait_find_elements(locator)

    @teststep
    def previous_btn(self):
        """上一题按钮"""
        locator = (By.CSS_SELECTOR, ".icons .icon-arrow-left")
        return self.wait.wait_find_element(locator)

    @teststep
    def check_detail_btn(self):
        """点击查看选题页面"""
        locator = (By.CSS_SELECTOR, ".icons .icon-card")
        self.wait.wait_find_element(locator).click()

    @teststep
    def answer_card_tip_content(self):
        """答题卡页面提示内容"""
        locator = (By.CSS_SELECTOR, ".answer-card h3")
        return self.wait.wait_find_element(locator).text

    @teststep
    def next_btn(self):
        """下一题按钮"""
        locator = (By.CSS_SELECTOR, ".icons .icon-arrow-right")
        return self.wait.wait_find_element(locator)

    @teststep
    def bank_number(self):
        """题号列表"""
        locator = (By.CSS_SELECTOR, ".detail .number")
        return self.wait.wait_find_elements(locator)

    @teststep
    def click_carry_out_btn(self):
        """点击交卷按钮"""
        locator = (By.CSS_SELECTOR, ".control .el-button")
        self.wait.wait_find_element(locator).click()

    @teststep
    def exam_name(self):
        """试卷名称"""
        locator = (By.CSS_SELECTOR, ".exam-title")
        return self.wait.wait_find_element(locator).text

    @teststep
    def score(self):
        """得分"""
        locator = (By.CSS_SELECTOR, ".score")
        ele = self.wait.wait_find_element(locator)
        return int(ele.text)

    @teststep
    def get_all_item(self):
        locator = (By.CSS_SELECTOR, ".table-body .item")
        return self.wait.wait_find_elements(locator)

    @teststep
    def word_index(self, item_ele):
        """单词索引"""
        ele = item_ele.find_element_by_css_selector('div:first-child')
        return ele.text

    @teststep
    def word_speaker(self, item_ele):
        """单词喇叭播放按钮"""
        ele = item_ele.find_element_by_css_selector('.text-wrap i')
        return ele

    @teststep
    def result_words(self, item_ele):
        """结果页单词"""
        ele = item_ele.find_element_by_css_selector('.text-wrap span')
        return ele.text

    @teststep
    def result_word_explain(self, item_ele):
        """单词解释"""
        ele = item_ele.find_element_by_css_selector('.el-tooltip span')
        return ele.text

    @teststep
    def word_game_type(self, item_ele):
        """单词所属游戏类型"""
        ele = item_ele.find_element_by_css_selector('div:nth-child(4)')
        return ele.text

    @teststep
    def vocab_select_icon(self, item_ele):
        """词汇选择正确和错误标识"""
        ele = item_ele.find_element_by_css_selector('div:nth-child(5)> i')
        return ele

    @teststep
    def spell_icon(self, item_ele):
        """单词拼写正确和错误标识"""
        ele = item_ele.find_element_by_css_selector('div:nth-child(5)> span')
        return ele

    @teststep
    def vocab_select_answer_word(self):
        """一测到底答案"""
        locator = (By.CSS_SELECTOR, '.word')
        return self.wait.wait_find_element(locator).text

    @teststep
    def listen_spell_game_containers(self):
        """单词听写父级容器"""
        locator = (By.CSS_SELECTOR, '.dctx-container')
        return self.wait.wait_find_elements(locator).text

    @teststep
    def vocab_select_game_container(self):
        """词汇选择父级容器"""
        locator = (By.CSS_SELECTOR, '.chxz-container')
        return self.wait.wait_find_elements(locator)

    @teststep
    def spell_word_game_container(self):
        """单词拼写父级容器"""
        locator = (By.CSS_SELECTOR, '.dcpx-container')
        return self.wait.wait_find_elements(locator)

    @teststep
    def vocab_select_game_operate(self, stu_id, book_id, db_words, do_right,  exam_type=2):
        """词汇选择游戏
            :param book_id: 书籍id
            :param db_words: 数据库查询单词数据
            :param do_right: 是否做对
            :param exam_type: 试卷类型, 新学， 已学
            :param stu_id 学生id
        """
        print('==== 词汇选择 ====\n')
        word_info = {}
        mine_answer_info = {}
        start_time = round(time.time())
        vocab_choice_containers = self.vocab_select_game_container()
        for index in range(len(vocab_choice_containers)):
            container = self.vocab_select_game_container()[index]
            word_id = container.get_attribute('id')
            if int(word_id) not in db_words:
                self.base_assert.except_error('该单词不在查询单词列表中')
            game_mode = container.get_attribute('mode')
            answer_word = self.data.get_word_by_word_id(word_id)
            explain_list = self.data.get_student_explain_list_by_word_id(stu_id, book_id, word_id)
            print('单词：', answer_word)
            print('单词id', word_id)
            print("解释列表：", explain_list)
            options = self.vocab.options(container)
            right_index = -1
            if game_mode in ['1', '4']:
                for i, x in enumerate(options):
                    if x.text.split('；') == explain_list:
                        print('正确答案：',  x.text)
                        word_info[word_id] = (answer_word, x.text)
                        right_index = i
                        break
                print('正确答案索引：', right_index)
                if right_index == -1:
                    self.base_assert.except_error('选项列表中不存在该单词所有解释合并列表集')
                    right_index = 0
            else:
                if game_mode == '2':
                    question = self.vocab.ques_title(container)
                    if question.split('；') != explain_list:
                        self.base_assert.except_error('单词解释不为该单词所有解释合并列表集')

                for i, y in enumerate(options):
                    opt_content = y.text.strip()
                    if opt_content == answer_word:
                        right_index = i
                        break

            if do_right:
                self.vocab.options(container)[right_index].click()
                mine_answer_info[answer_word] = answer_word
            else:
                for i, x in enumerate(options):
                    if i != right_index:
                        mine_answer_info[answer_word] = x.text
                        x.click()
                        break
            time.sleep(1)
            print('-' * 30, '\n')
        used_time = round(time.time()) - start_time
        return mine_answer_info, used_time


    @teststep
    def spell_game_operate(self, stu_id, book_id, db_words, do_right,  exam_type=2):
        """测试类单词拼写类游戏过程"""
        print('===== 单词拼写 =====\n')
        start_time = round(time.time())
        mine_answer_info = {}
        for index in range(len(self.spell_word_game_container())):
            container = self.spell_word_game_container()[index]
            word_id = container.get_attribute('id')
            answer_word = self.data.get_word_by_word_id(word_id)
            print('单词id：', word_id)
            print('正确单词：', answer_word)
            if int(word_id) not in db_words:
                self.base_assert.except_error('该单词不在查询单词列表中')
            explain = self.spell.explain(container)
            print('解释：', explain)
            explain_list = self.data.get_student_explain_list_by_word_id(stu_id, book_id, word_id)
            if explain.split('；') != explain_list:
                self.base_assert.except_error('该单词的解释不是该单词(已学单词)的所有解释的合并集')

            self.spell.normal_spell_input_wrap(container).click()
            if do_right:
                self.spell.normal_spell_input_wrap(container).send_keys(answer_word)
                input_answer = answer_word
            else:
                random_str = ''.join(random.sample(string.ascii_lowercase, 3))
                input_answer = random_str
                self.spell.normal_spell_input_wrap(container).send_keys(random_str)

            mine_answer_info[answer_word] = input_answer
            print('我输入的：', input_answer)
            time.sleep(1)
            print('-' * 30, '\n')
        used_time = round(time.time()) - start_time
        return mine_answer_info, used_time

    @teststep
    def listen_spell_game_operate(self, db_words, do_right,  exam_type=2):
        """单词听写过程"""
        print('===== 单词听写 =====\n')
        start_time = round(time.time())
        mine_answer = {}
        for index in range(len(self.listen_spell_game_containers())):
            container = self.listen_spell_game_containers()[index]
            word_id = container.get_attribute('id')
            answer_word = self.data.get_word_by_word_id(word_id)
            print('单词id：', word_id)
            print('正确单词：', answer_word)
            if int(word_id) not in db_words:
                self.base_assert.except_error('该单词不在查询单词列表中')

            self.spell.normal_spell_input_wrap(container).click()
            if do_right:
                self.spell.normal_spell_input_wrap(container).send_keys(answer_word)
                input_answer = answer_word
            else:
                random_str = ''.join(random.sample(string.ascii_lowercase, 3))
                input_answer = random_str
                self.spell.normal_spell_input_wrap(container).send_keys(random_str)
            mine_answer[answer_word] = input_answer
            print('我输入的：', input_answer)
            time.sleep(1)
            print('-' * 30, '\n')
        used_time = round(time.time()) - start_time
        return mine_answer, used_time



