#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/25 15:02
# -----------------------------------------
import datetime
import json
import os
import time

from app.wordbook.objects_page.flash_card_page import FlashWordPage
from app.wordbook.objects_page.new_word_game_page import NewWordGameOperatePage
from app.wordbook.objects_page.sentence_strengthen import SentenceStrengthenPage
from app.wordbook.objects_page.spell_word_page import SpellWordPage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep


class ReciteWordPage(NewWordGameOperatePage):

    @teststep
    def recite_word_process(self, stu_id, book_id, start_content, do_right=False):
        """复习过程"""
        start_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        time_msg = {'结束时间': '', '大题用时': {}, '总用时': 0}
        begin_time = round(time.time())
        print('开始时间：', start_time)
        begin_fluency, recite_word_info = {}, {}
        wrong_index_info = {'单词拼写': [], '强化炼句': []}
        bank_time = time_msg['大题用时'] = {x: 0 for x in ['闪卡练习', '单词拼写', '强化炼句']}
        word_info, phrase_info = {}, {}
        before_fluency = {}
        skip_word_info = []
        all_bank_index = [0]
        while self.wait_check_container_page():
            game_container, game_mode, explain_id = self.game_container()
            if game_container == 'sk-container':  # 闪卡类游戏
                spend_time = FlashWordPage().normal_flash_card_operate(stu_id, book_id, recite_word_info)  # 闪卡录音游戏
                bank_time['闪卡练习'] += spend_time
                word_info = {x: recite_word_info[x] for x in recite_word_info if recite_word_info[x][2] == '单词'}
                phrase_info = {x: recite_word_info[x] for x in recite_word_info if recite_word_info[x][2] == '短语'}
                before_fluency = {x: self.data.get_explain_fluency_by_word_id(stu_id, x) for x in list(recite_word_info.keys())}

            elif game_container == 'qhlj-container':
                spend_time = SentenceStrengthenPage().sentence_strengthen_game_operate(phrase_info, do_right, all_bank_index,
                                                                                       wrong_index_info=wrong_index_info['强化炼句'])
                bank_time['强化炼句'] += spend_time

            elif game_container == 'dcpx-container':
                spend_time = SpellWordPage().spell_with_copy_operate(word_info, stu_id, do_right, all_bank_index, skip_word_info,
                                                                     wrong_index_info=wrong_index_info['单词拼写'], is_recite=True, book_id=book_id)
                bank_time['单词拼写'] += spend_time

        used_time = round(time.time()) - begin_time
        end_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        time_msg['结束时间'] = end_time
        time_msg['总用时'] = used_time
        print(time_msg)
        wrong_word_list = []
        if not do_right:
            if len(word_info):
                self.check_recite_wrong_interval(len(word_info), wrong_index_info)
                end_index = 1 if len(word_info) == 1 else 2
                wrong_word_list.extend(list(word_info.keys())[:end_index])

            if len(phrase_info):
                self.check_recite_wrong_interval(len(phrase_info), wrong_index_info)
                wrong_word_list.extend(list(word_info.keys())[0])

        if '开始本单元复习' in start_content:
            fl_change = False
        else:
            fl_change = True
        self.check_recite_word_fluency_operate(stu_id, book_id, before_fluency, wrong_word_list=wrong_word_list, fl_change=fl_change)
        return recite_word_info

    @teststep
    def check_recite_wrong_interval(self, phrase_count, wrong_index_info):
        """查看复习错题间隔"""
        spell_wrong_index = wrong_index_info['单词拼写']
        sentence_wrong_index = wrong_index_info['强化炼句']
        if spell_wrong_index:
            if spell_wrong_index != [0, 2, 4, 6]:
                self.base_assert.except_error('单词拼写错题间隔错误 {}'.format(spell_wrong_index))

        if sentence_wrong_index:
            if sentence_wrong_index != [2*phrase_count - 1 + 2*x for x in range(5)]:
                self.base_assert.except_error('强化炼句错题间隔错误 {}'.format(sentence_wrong_index))


    @teststep
    def check_recite_word_fluency_operate(self, stu_id, book_id, before_word_fluency, wrong_word_list=None, fl_change=False):
        """复习单词F值校验"""
        explain_fluency_info = {}
        for x in before_word_fluency:
            explain_info = before_word_fluency[x]
            explain_fluency_info.update(explain_info)
        self.check_words_fluency_value(stu_id, explain_fluency_info, f_is_change=fl_change)
        if wrong_word_list:
            pro_path = os.path.abspath('.')

            with open(pro_path + '\\app\\wordbook\\test_data\\wrong.json', 'r') as f:
                note_dict = json.load(f)
            already_study_word_info = {x: WordBookSqlHandle().get_student_explain_list_by_word_id(stu_id, book_id, x) for x in wrong_word_list}
            note_dict.update(already_study_word_info)
            with open(pro_path + '\\app\\wordbook\\test_data\\wrong.json', 'w') as f:
                f.write(json.dumps(note_dict, ensure_ascii=False))
                f.close()

