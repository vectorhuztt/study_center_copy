#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/29 8:58
# -----------------------------------------
import time
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep


class RestoreWordPage(WordBookPublicElePage):
    @teststep
    def wait_check_restore_word_page(self):
        locator = (By.CSS_SELECTOR, '.hydc-container')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def restore_word_explain(self):
        """单词解释"""
        locator = (By.CSS_SELECTOR, '.revert-wrap .explain')
        return self.wait.wait_find_element(locator).text

    @teststep
    def wait_select_word(self):
        """待选单词"""
        locator = (By.CSS_SELECTOR, '.main .answer-wrap li')
        return self.wait.wait_find_elements(locator)

    @teststep
    def finish_word(self):
        """完成单词"""
        locator = (By.CSS_SELECTOR, '.main .word-wrap li')
        ele = self.wait.wait_find_elements(locator)
        words = [x.text.strip() for x in ele]
        return ''.join(words)

    @teststep
    def clear_btn(self):
        """清除按钮"""
        locator = (By.CSS_SELECTOR, '.control-bar .icon-components-eraser')
        return self.wait.wait_find_element(locator)

    @teststep
    def get_wait_words_text(self):
        """获取下方待选字母文本"""
        text = ''.join([x.text.strip() for x in self.wait_select_word()])
        return text

    @teststep
    def restore_do_right_operate(self, answer_word):
        """还原单词正确操作"""
        index = 0
        while answer_word.strip() != self.finish_word():
            wait_select_words = self.wait_select_word()
            for x in range(len(wait_select_words)):
                wait_alpha = wait_select_words[x].text.strip()
                alpha_length = len(wait_alpha)
                if index + alpha_length >= len(answer_word) - 1:
                    answer_word += ' ' * alpha_length
                word_part = answer_word[index:index + alpha_length].strip()
                if wait_alpha and wait_alpha == word_part:
                    wait_select_words[x].click()
                    time.sleep(1)
                    index += alpha_length
                    break

    @teststep
    def restore_do_wrong_operate(self, answer_word):
        """还原单词错误操作"""
        wait_select_words = self.wait_select_word()
        select_index, count = 0, 0
        for x in range(len(wait_select_words)):
            alpha_length = len(wait_select_words[x].text.strip())
            word_part = answer_word[:alpha_length]
            if count == 0:
                if wait_select_words[x].text.strip() != word_part.strip():
                    select_index = x
                    wait_select_words[x].click()
                    count += 1
                    break

        rest_select_words = self.wait_select_word()
        print('下面待点字母：', [x.text for x in rest_select_words])
        for i, y in enumerate(rest_select_words):
            rest_select_words = self.wait_select_word()
            if i == select_index:
                continue
            else:
                rest_select_words[i].click()
                time.sleep(0.5)

    @teststep
    def restore_word_operate(self, word_info, do_right, bank_index, wrong_index_info):
        """还原单词游戏过程
        :param wrong_index_info: 错题编号收录信息
        :param bank_index:     题目编号
        :param do_right:      是否做全对
        :param word_info:    闪卡记录的正确答案信息
        """
        print('======= 还原单词 =======\n')
        print('是否做对：', do_right)
        begin_time = round(time.time())
        finish_word = []
        index = 0
        while self.wait_check_restore_word_page():
            wrong_count = len(wrong_index_info)
            self.click_speaker_icon()
            self.commit_btn_judge()
            word_explain_id = self.game_container()[-1]
            explain = self.restore_word_explain()
            print('题目索引：', bank_index[0])
            print('解释(单词)id：', word_explain_id)
            print('单词解释：', explain)
            answer_word = word_info[word_explain_id][0]
            print('还原前单词：', self.get_wait_words_text())
            print('记录答案：', answer_word)
            wrong_id = list(word_info.keys())[0]

            if word_explain_id in finish_word:
                self.base_assert.except_error('单词已做对， 但是再次出现 ' + word_explain_id)
            # 第一道做题后清空查看状态，并等待时间为0, 判断题目是否发生变化
            # 其余题目做错操作
            if not do_right:
                if index == 0 and len(word_info) > 1:
                    wrong_index_info.append(bank_index[0])
                    self.restore_do_wrong_operate(answer_word)
                    print('此单词错误次数：', len(wrong_index_info))
                    self.clear_btn().click()
                    time.sleep(1)
                    if self.finish_word():
                        self.base_assert.except_error('★★★ 点击清除按钮后，已选选项未清空')
                    self.restore_do_wrong_operate(answer_word)
                    # time.sleep(30)
                    # if self.game_container()[-1] == word_explain_id:
                    #     self.base_assert.except_error('限制时间过后， 单词未发生变化')
                else:
                    if word_explain_id == wrong_id:
                        wrong_index_info.append(bank_index[0])
                        print('此单词错误次数：', len(wrong_index_info))
                        self.restore_do_wrong_operate(answer_word)
                    else:
                        self.restore_do_right_operate(answer_word)
                        finish_word.append(word_explain_id)
            else:
                self.restore_do_right_operate(answer_word)
                finish_word.append(word_explain_id)

            self.commit_btn_judge(status=True)
            mine_answer = self.finish_word()
            print('我的答案：', mine_answer)
            if len(wrong_index_info) == wrong_count:
                if self.wait_check_answer_word_page():
                    print('正确答案：' + self.right_answer())
                else:
                    self.base_assert.except_error('点击提交未发现正确答案文本')
                self.commit_btn_judge(status=True)
                self.commit_btn().click()
            self.commit_btn().click()
            time.sleep(2)
            index += 1
            bank_index[0] += 1
            print('-'*30, '\n')
        spend_time = round(time.time()) - begin_time
        return spend_time


    @teststep
    def error_note_restore_word_operate(self, stu_id, book_id, wrong_id_list, second_wrong_words, wrong_count=None, do_right=False):
        """错题本中还原单词操作"""
        print('===== 错题本中的还原单词操作 =====\n')
        wrong_word_id, index = 0, 0
        while self.wait_check_restore_word_page():
            self.click_speaker_icon()
            self.commit_btn_judge()
            word_id = self.game_container()[-1]
            wrong_id_list.append(word_id)
            explain = self.restore_word_explain()
            answer_word = WordBookSqlHandle().get_word_by_word_id(word_id)
            print('单词id：', word_id)
            print('单词解释：', explain)
            print('正确答案：', answer_word)
            db_all_explain = WordBookSqlHandle().get_student_explain_list_by_word_id(stu_id, book_id, word_id)
            if explain.split('；') != db_all_explain:
                self.base_assert.except_error('题目解释不是已学解释合并')
            if not do_right:
                if index == 0:
                    wrong_word_id = word_id
                    second_wrong_words.append(wrong_word_id)

                if word_id in second_wrong_words:
                    self.restore_do_wrong_operate(answer_word)
                    self.commit_btn().click()
                    wrong_count[0] += 1
                else:
                    self.restore_do_right_operate(answer_word)
            else:
                self.restore_do_right_operate(answer_word)
            mine_answer = self.finish_word()
            print('我的答案：', mine_answer)
            self.commit_btn().click()
            time.sleep(2)
            index += 1
            print('-' * 30, '\n')
