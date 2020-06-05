#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/24 11:55
# -----------------------------------------
import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from conf.decorator import teststep


class SentenceStrengthenPage(WordBookPublicElePage):

    @teststep
    def wait_check_sentence_strengthen_page(self):
        """强化炼句页面检查点"""
        locator = (By.CSS_SELECTOR, '.qhlj-container')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_sentence_enhance_answer_page(self):
        """强化炼句正确答案页面检查点"""
        locator = (By.CSS_SELECTOR, '.right-answer')
        return self.wait.wait_check_element(locator)

    @teststep
    def word_phrase_explain(self):
        """短语解释"""
        locator = (By.CSS_SELECTOR, '.play-content .explain')
        return self.wait.wait_find_element(locator).text

    @teststep
    def input_wrap(self):
        """短语输入栏"""
        locator = (By.CSS_SELECTOR, '.underline')
        return self.wait.wait_find_elements(locator)

    @teststep
    def page_words(self):
        """完成单词"""
        locator = (By.CSS_SELECTOR, '.custom-init span')
        ele = self.wait.wait_find_elements(locator)
        return [x.text.strip() for x in ele]

    @teststep
    def page_right_answer(self):
        """正确答案"""
        locator = (By.CSS_SELECTOR, '.right-answer')
        return self.wait.wait_find_element(locator).text

    @teststep
    def sentence_enhance_process(self, do_right=False, right_answer=None):
        """强化炼句做对做错操作"""
        if do_right:
            for i, x in enumerate(self.input_wrap()):
                x.click()
                x.send_keys(right_answer[i])
        else:
            for x in self.input_wrap():
                x.click()
                random_str = random.sample(string.ascii_letters, random.randint(1, 4))
                x.send_keys(''.join(random_str))

    @teststep
    def sentence_strengthen_game_operate(self, word_info, do_right, bank_index, wrong_index_info):
        """"强化炼句游戏过程"""
        print('======= 强化炼句 ======= \n')
        begin_time = round(time.time())
        index = 0
        right_word = []
        while self.wait_check_sentence_strengthen_page():
            right_count = len(right_word)
            self.commit_btn_judge()
            explain_id = self.game_container()[-1]
            phrase_explain = self.word_phrase_explain()
            print('题目索引：', bank_index[0])
            print('解释id：', explain_id)
            print('单词解释：', phrase_explain)
            right_answer = word_info[explain_id][0]
            print('正确答案：', right_answer)

            wrong_id = list(word_info.keys())[0]
            page_words = self.page_words()
            input_words = [x for x, y in zip(right_answer.split(), page_words) if x != y]
            print('需要输入单词：', input_words)

            if not do_right:
                # if index == 0 and len(word_info) > 1:
                #     wrong_index_info.append(bank_index[0])
                #     time.sleep(30)
                #     if self.game_container()[-1] == explain_id:
                #         self.base_assert.except_error('限制时间过后， 单词未发生变化')
                # else:
                if explain_id == wrong_id:
                    wrong_index_info.append(bank_index[0])
                    print('此单词错误次数：', len(wrong_index_info))
                    self.sentence_enhance_process()
                else:
                    self.sentence_enhance_process(do_right=True, right_answer=input_words)
                    right_word.append(explain_id)
            else:
                self.sentence_enhance_process(do_right=True, right_answer=input_words)
                right_word.append(explain_id)

            print('我的答案：', ' '.join(self.page_words()))
            self.commit_btn_judge(status=True)
            self.commit_btn().click()
            time.sleep(1)
            if len(right_word) == right_count:
                if not self.wait_check_sentence_enhance_answer_page():
                    self.base_assert.except_error('本题已做错， 页面未发现正确答案页面检查点')
                else:
                    print(self.page_right_answer())
                self.commit_btn().click()
            time.sleep(1)
            index += 1
            bank_index[0] += 1
            print('-'*30, '\n')
        spend_seconds = round(time.time()) - begin_time
        return spend_seconds



