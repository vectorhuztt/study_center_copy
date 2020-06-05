#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/3 15:01
# -----------------------------------------
import datetime
import json
import os
import re
import time
from app.wordbook.objects_page.flash_card_page import FlashWordPage
from app.wordbook.objects_page.restore_word_page import RestoreWordPage
from app.wordbook.objects_page.sentence_strengthen import SentenceStrengthenPage
from app.wordbook.objects_page.word_choice import VocabSelectPage
from app.wordbook.objects_page.wordbook_common_ele import WordBookPublicElePage
from app.wordbook.objects_page.wordbook_home_page import WordHomePage
from app.wordbook.objects_page.spell_word_page import SpellWordPage
from app.wordbook.objects_page.wordbook_sql_handle import WordBookSqlHandle
from conf.decorator import teststep, teststeps
from utils.dict_slice import DictSlice


class NewWordGameOperatePage(WordBookPublicElePage):

    def __init__(self):
        self.data = WordBookSqlHandle()
        self.home = WordHomePage()
        self.slice = DictSlice()

    @teststeps
    def new_word_study_process(self, stu_id, book_id, *, all_word_info, fl_change,  do_right=False,
                               study_time_info=None, group_count=None, book_type="enhanced"):
        """单词学习过程"""
        time_msg = study_time_info if study_time_info else {'结束时间': '', '大题用时': {}, '总用时': 0}
        begin_time = round(time.time())
        group_fluency, group_word_info = {}, {}
        before_word_fluency, before_phrase_fluency = {}, {}
        word_info, phrase_info = {}, {}
        all_bank_index = [0]
        wrong_word_index = {x: [] for x in ['还原单词', '听音选词', '汉译英', '单词拼写']}
        wrong_phrase_index = {x: [] for x in ['英译汉', '强化炼句']}
        bank_time = time_msg['大题用时'] = {x: 0 for x in ['闪卡练习', '还原单词', '词汇选择', '单词拼写', '强化炼句']}
        spell_skip_word = []
        while self.wait_check_container_page():
            game_container, game_mode, explain_id = self.game_container()
            # 每5个一组,可以同时存在单词和短语， 先做单词后短语，
            # 单词在1-3之间的做题索引各不相同，具体规律如下
            if not do_right:
                if 0 < len(word_info) < 4:
                    if all_bank_index[0] == 19 + 4 * (len(word_info) - 1):
                        all_bank_index[0] = 0
                if len(word_info) == 4:
                    if all_bank_index[0] == 33:
                        all_bank_index[0] = 0

            if game_container == 'sk-container':  # 闪卡类游戏
                if book_type == 'enhanced':
                    spend_time = FlashWordPage().speak_flash_card_operate(group_word_info)
                else:
                    spend_time = FlashWordPage().\
                        normal_flash_card_operate(stu_id, book_id, word_info=group_word_info, is_enhanced=False)
                bank_time['闪卡练习'] += spend_time

                if len(group_word_info) != group_count:
                    self.base_assert.except_error('当前组内单词数与应练单词数不一致， 组内单词数为%d, '
                                                  '应学单词数为%d' %(len(group_word_info), group_count))
                # 通过闪卡游戏获取单词数和短语数，并同时获取对应的做题之前的F值
                word_info = {x: group_word_info[x] for x in group_word_info if group_word_info[x][2] == '单词'}
                phrase_info = {x: group_word_info[x] for x in group_word_info if group_word_info[x][2] == '短语'}
                before_word_fluency = {x: self.data.get_explain_fluency_by_explain_id(stu_id, x)
                                       for x in list(word_info.keys())}
                before_phrase_fluency = {x: self.data.get_explain_fluency_by_explain_id(stu_id, x)
                                         for x in list(phrase_info.keys())}

            elif game_container == 'chxz-container':  # 词汇选择游戏
                index_info = []
                study_words = {}
                if game_mode == '2':
                    index_info = wrong_word_index['汉译英']
                    study_words = word_info
                elif game_mode == '3':
                    index_info = wrong_word_index['听音选词']
                    study_words = word_info
                elif game_mode == '1':
                    index_info = wrong_phrase_index['英译汉']
                    study_words = phrase_info

                spend_time = VocabSelectPage().\
                    vocab_select_operate(study_words, do_right, game_mode, all_bank_index, wrong_index_info=index_info)
                bank_time['词汇选择'] += spend_time
                print('词汇选择-mode{}错题间隔：'.format(game_mode), index_info)

            elif game_container == 'dcpx-container':  # 单词拼写游戏
                wrong_index_info = wrong_word_index['单词拼写']
                if book_type == 'enhanced':
                    spend_time = SpellWordPage().\
                        spell_with_copy_operate(word_info, stu_id, do_right, all_bank_index, spell_skip_word,
                                                wrong_index_info=wrong_index_info)
                else:
                    spend_time = SpellWordPage().\
                        random_spell_game_operate(word_info, do_right, all_bank_index, wrong_index_info)
                bank_time['单词拼写'] += spend_time
                print('单词拼写错题间隔：', wrong_index_info)

            elif game_container == 'qhlj-container':  # 短语的强化炼句游戏
                spend_time = SentenceStrengthenPage().\
                    sentence_strengthen_game_operate(phrase_info, do_right, all_bank_index,
                                                     wrong_index_info=wrong_phrase_index['强化炼句'])
                bank_time['强化炼句'] += spend_time
                print('强化炼句错题间隔：', wrong_phrase_index['强化炼句'])

            elif game_container == 'hydc-container':  # 还原单词游戏
                spend_time = RestoreWordPage().restore_word_operate(word_info, do_right, all_bank_index,
                                                                    wrong_index_info=wrong_word_index['还原单词'])
                bank_time['还原单词'] += spend_time
                print('还原单词错题间隔列表：', wrong_word_index['还原单词'])

        used_time = round(time.time()) - begin_time
        end_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        time_msg['结束时间'] = end_time
        time_msg['总用时'] += used_time
        print(time_msg)

        # 检验错题间隔是否正确
        if not do_right:
            if len(word_info):
                self.check_new_word_wrong_interval(len(word_info), len(phrase_info), wrong_word_index, book_type)
            if len(phrase_info):
                self.check_new_word_wrong_interval(len(word_info), len(phrase_info),  wrong_phrase_index,
                                                   is_phrase=True, book_type=book_type)

        # 校验已完成单词的F值变化
        self.check_new_word_fluency_operate(stu_id, book_id, before_word_fluency, before_phrase_fluency, fl_change)

        # 再来一组的处理过程
        all_word_info.update(group_word_info)
        if self.wait_check_finish_page():
            finish_content = self.finish_content()
            print(finish_content)
            if self.finish_first_btn().text == "再来一组":
                content_num = re.findall(r'\d+', self.content_desc())
                rest_word_count = int(content_num[0]) - int(content_num[-1])
                next_group_count = 5 if rest_word_count >= 5 else rest_word_count
                self.finish_first_btn().click()
                time.sleep(1)
                self.new_word_study_process(stu_id, book_id, all_word_info=all_word_info, fl_change=fl_change,
                                            do_right=do_right, study_time_info=time_msg,
                                            group_count=next_group_count, book_type=book_type)
            else:
                self.exit_icon().click()

    @teststep
    def check_new_word_fluency_operate(self, stu_id, book_id, before_word_fluency, before_phrase_fluency, fl_change):
        """
        新词F值查看主要步骤
        :param stu_id: 学生id
        :param book_id: 图书id
        :param before_word_fluency:  学前单词熟练度
        :param before_phrase_fluency: 学前短语熟练度
        :param fl_change:  是否发生F值变化
        :return:
        """
        wrong_word_fluency = {}
        right_word_fluency = {}
        if before_word_fluency:
            end_index = 1 if len(before_word_fluency) == 1 else 2
            wrong_word_fluency.update(self.slice.dict_slice(before_word_fluency, end=end_index))
            right_word_fluency.update(self.slice.dict_slice(before_word_fluency, start=end_index))

        if len(before_phrase_fluency):
            wrong_word_fluency.update(self.slice.dict_slice(before_phrase_fluency, end=1))
            right_word_fluency.update(self.slice.dict_slice(before_phrase_fluency, start=1))

        self.check_words_fluency_value(stu_id, wrong_word_fluency, f_is_change=fl_change)
        self.check_words_fluency_value(stu_id, right_word_fluency, f_is_change=fl_change, is_right=True)

        # 将错题写入错题记录文件
        if wrong_word_fluency:
            pro_path = os.path.abspath('.')

            with open(pro_path + '\\app\\wordbook\\test_data\\wrong.json', 'r') as f:
                note_dict = json.load(f)
            explain_id_list = list(wrong_word_fluency.keys())
            word_id_list = [WordBookSqlHandle().get_word_id_by_explain_id(stu_id, x) for x in explain_id_list]
            already_study_word_info = {x: WordBookSqlHandle().get_student_explain_list_by_word_id(stu_id, book_id, x)
                                       for x in word_id_list}
            note_dict.update(already_study_word_info)
            with open(pro_path + '\\app\\wordbook\\test_data\\wrong.json', 'w') as f:
                f.write(json.dumps(note_dict, ensure_ascii=False))
                f.close()

    @teststep
    def check_new_word_wrong_interval(self, word_count, phrase_count, wrong_index_info, book_type, is_phrase=False):
        """查看新词错题间隔操作"""
        if not is_phrase:
            listen_wrong_index = wrong_index_info['汉译英']
            if len(listen_wrong_index) != 5:
                self.base_assert.except_error('单词听音选词错题次数不为5！')
            else:
                if listen_wrong_index != [listen_wrong_index[0] + 2 * x for x in range(5)]:
                    self.base_assert.except_error('单词听音选词错误间隔不正确， 请核查')

            spell_index = wrong_index_info['单词拼写']
            if book_type == "enhanced":
                restore_wrong_index = wrong_index_info['听音选词']
                if len(restore_wrong_index) != 5:
                    self.base_assert.except_error('还原单词错题次数不为5！')
                if restore_wrong_index != [0, 2, 4, 6, 8]:
                    self.base_assert.except_error('还原单词错题间隔不正确，请查实')

                choice_wrong_index = wrong_index_info['还原单词']
                if len(choice_wrong_index) != 5:
                    self.base_assert.except_error('单词汉译英错题次数不为5！')
                if choice_wrong_index != [choice_wrong_index + 2 * x for x in range(5)]:
                    self.base_assert.except_error('单词汉译英错题间隔不正确， 请核查')

                if len(spell_index) != 4:
                    self.base_assert.except_error('单词拼写错题次数不为4！')
                if spell_index != [spell_index[0] + 2 * x  for x in range(4)]:
                    self.base_assert.except_error('单词拼写错误间隔不正确， 请核查')
            else:
                if len(spell_index) != 5:
                    self.base_assert.except_error('单词拼写错题次数不为5！')
                if spell_index != [spell_index[0] + 2 * x for x in range(5)]:
                    self.base_assert.except_error('单词拼写错误间隔不正确， 请核查')

        else:
            choice_index = wrong_index_info['英译汉']
            if choice_index != [0, 2, 4, 6, 8]:
                self.base_assert.except_error('短语英译汉错题间隔不正确，请核查')

            if word_count:
                if phrase_count == 1:
                    check_index_list = [7, 9, 10, 11, 12]
                else:
                    start_index = 7 + phrase_count
                    check_index_list = [start_index + 2*x for x in range(phrase_count)]
                    check_index_list.extend([check_index_list[-1] + (x+1) for x in range(5-len(check_index_list))])
            else:
                check_index_list = [2 * phrase_count - 1 + 2 * x for x in range(5)]
            sentence_enhance_index = wrong_index_info['强化炼句']
            print('计算强化炼句错题间隔:', check_index_list)
            if sentence_enhance_index != check_index_list:
                self.base_assert.except_error('短语强化炼句错误间隔不正确， 请核查')









