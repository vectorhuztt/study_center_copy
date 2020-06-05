# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/18 11:21
# -------------------------------------------
import re

from app.passion.object_page.sql_data import Sql
from conf.base_page import BasePage
from conf.decorator import teststeps


class HandleAnswer(BasePage):
    def __init__(self):
        super().__init__()
        self.data = Sql()

    @teststeps
    def get_exam_answers(self, question_ids):
        """获取书籍对应的题型和答案"""
        question_id_list = [y for x in question_ids for y in x[0].split(',')]
        question_info = self.data.find_game_type_content(tuple(question_id_list))
        select_ques = [x[1] for x in question_info if x[0] == 203]
        blank_ques = [x[1] for x in question_info if x[0] == 204]
        data = {'选择': {}, '填空': {}}
        select_data = [x.encode('utf-8').decode('unicode_escape') for x in select_ques]
        blank_data = [x.encode('utf-8').decode('unicode_escape') for x in blank_ques]
        select_q_a = [{self.get_select_q_a(x)[0]: self.get_select_q_a(x)[1]} for x in select_data]
        blank_q_a = [{self.get_blank_q_a(x)[0]: self.get_blank_q_a(x)[1]} for x in blank_data]

        for x in select_q_a:
            for y in x:
                data['选择'][y] = x[y]

        for x in blank_q_a:
            for y in x:
                data['填空'][y] = x[y]

        return data

    @staticmethod
    def get_blank_q_a(x):
        x = x.replace('\n', '')
        question = re.findall(r'.*?"#q":"(.*?)",.*?', x)[0]
        reform_q = re.sub(r'\[\[(.*?)\]\]', '', question)
        reform_q = reform_q.replace('  ', ' ').replace('\t', ' ').replace('\n', '')
        reform_q = reform_q.replace('\\', '').strip()
        answers = re.findall(r'\[\[(.*?)\]\]', question)
        return reform_q, answers

    @staticmethod
    def get_select_q_a(x):
        question = re.findall(r'.*?"#q":"(.*?)",.*?', x)[0].strip()
        question = question.replace('\\', '')
        answer = re.findall(r'.*?"#a":"(.*?)",.*?', x)[0]
        return question, answer











