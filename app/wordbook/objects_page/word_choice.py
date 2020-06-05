#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/29 9:18
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep


class VocabSelectPage(WordBookPublicElePage):

    def __init__(self):
        self.sql = WordBookSqlHandle()

    @teststep
    def wait_check_vocab_select_page(self):
        """听音选义页面检查点"""
        locator = (By.CSS_SELECTOR, '.chxz-container')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_select_wrong_page(self):
        locator = (By.CSS_SELECTOR, '.options .danger')
        return self.wait.wait_check_element(locator, timeout=3)

    @teststep
    def wait_check_word_explain_page(self):
        """听音选义页面检查点"""
        locator = (By.CSS_SELECTOR, '.title .explain')
        return self.wait.wait_check_element(locator, timeout=3)

    @teststep
    def click_voice_icon(self):
        """点击喇叭图标"""
        locator = (By.CSS_SELECTOR, '.control-bar .speaker')
        self.wait.wait_find_element(locator).click()

    @teststep
    def listen_word(self):
        """听读的单词"""
        locator = (By.CSS_SELECTOR, '.word')
        return self.wait.wait_find_element(locator).text

    @teststep
    def listen_explain(self):
        """听音选词的单词解释"""
        locator = (By.CSS_SELECTOR, '.title .explain')
        return self.wait.wait_find_element(locator).text

    @teststep
    def options(self):
        """选项"""
        locator = (By.CSS_SELECTOR, '.options li')
        return self.wait.wait_find_elements(locator)

    @teststep
    def question(self):
        """词汇选择问题"""
        locator = (By.CSS_SELECTOR, '.chxz-container .title')
        ele = self.wait.wait_find_element(locator)
        return ele.text.strip()

    @teststep
    def vocab_do_process(self, do_right=False, right_answer=None):
        mine_answer = 0
        for x in self.options():
            if do_right:
                if x.text == right_answer:
                    mine_answer = x.text
                    x.click()
                    break
            else:
                if x.text != right_answer:
                    mine_answer = x.text
                    x.click()
                    break
        time.sleep(3)
        print('我的答案：', mine_answer)


    @teststep
    def vocab_select_operate(self, word_info, do_right, game_mode, bank_index, wrong_index_info):
        """ 词汇选译游戏过程
        :param wrong_index_info: 错题索引收录信息
        :param bank_index: 所有题的索引信息
        :param do_right:  是否做全对
        :param word_info: 闪卡记录的正确答案信息
        :param game_mode: 游戏类型
        """
        if game_mode == '1':
            mode_type = '英译汉'
        elif game_mode == '2':
            mode_type = '汉译英'
        elif game_mode == '3':
            mode_type = "听音选词"
        else:
            mode_type = '听音选词'

        print('======= 词汇选择-{} ======= \n'.format(mode_type))
        begin_time = round(time.time())
        index = 0
        right_word = []
        while self.wait_check_vocab_select_page():
            wrong_count = len(wrong_index_info)
            game_container, mode, word_explain_id = self.game_container()
            if mode != game_mode:
                break
            print('题目索引：', bank_index[0])
            print('解释(单词)id：', word_explain_id)
            if game_mode in ['1', '2']:
                print('问题：', self.question())

            self.commit_btn_judge()
            if game_mode in ['2', '3']:
                right_answer = word_info[word_explain_id][0]
            else:
                right_answer = word_info[word_explain_id][1]
            print('正确答案：', right_answer)
            wrong_id = list(word_info.keys())[0]

            if word_explain_id in right_word:
                self.base_assert.except_error('单词已做对， 但是再次出现 ' + word_explain_id)

            if not do_right:
                # if index == 0 and len(word_info) > 1:
                #     time.sleep(30)
                #     if self.game_container()[-1] == word_explain_id:
                #         self.base_assert.except_error('限制时间过后， 单词未发生变化')
                # else:
                if word_explain_id == wrong_id:
                    wrong_index_info.append(bank_index[0])
                    print('此单词错误次数：', len(wrong_index_info))
                    self.vocab_do_process(right_answer=right_answer)
                    if len(wrong_index_info) == 5:
                        right_word.append(word_explain_id)
                else:
                    self.vocab_do_process(do_right=True, right_answer=right_answer)
                    right_word.append(word_explain_id)
            else:
                self.vocab_do_process(do_right=True, right_answer=right_answer)
                right_word.append(word_explain_id)

            if wrong_count != len(wrong_index_info):
                if game_mode == '3':
                    if not self.wait_check_word_explain_page():
                        self.base_assert.except_error('未发现单词解释')
                    else:
                        print('单词解释：', self.listen_explain())
                self.commit_btn_judge(status=True)
                self.commit_btn().click()
                time.sleep(3)
            index += 1
            bank_index[0] += 1
            print('-'*30, '\n')
        spend_seconds = round(time.time()) - begin_time
        return spend_seconds


