#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/16 16:40
# -----------------------------------------
import json
import re

from app.passion.object_page.passion_sql import PassionSql
from app.passion.test_data.passion_config import STUDENT_ACCOUNT
from conf.base_page import BasePage


class PassionSQLHandle(BasePage):

    def __init__(self):
        self.mysql = PassionSql()

    def get_book_chapter_num(self, book_id):
        """获取书籍章节数"""
        result = self.mysql.find_book_chapter_num(book_id)
        return result[0][0] if result else 0

    def get_chapter_id_and_available_value(self, book_id, name, parent_id=0):
        """获取章节id和是否上架状态"""
        result = self.mysql.find_chapter_name_available_value_by_name(book_id, name, parent_id)
        return result[0]

    def get_chapter_have_video(self, chapter_id):
        result = self.mysql.find_chapter_is_have_video(chapter_id)
        return 1 if len(result) else 0

    def get_chapter_section_ids(self, chapter_id):
        """获取章节小节id"""
        result = self.mysql.find_current_chapter_section_num(chapter_id)
        return result

    def get_section_knowledge_num_by_id(self, book_id,  section_id):
        """获取小节的知识点数"""
        result = self.mysql.find_section_question_ids(book_id, section_id)
        total_num = sum([x[0] for x in result])
        return total_num

    def delete_student_all_record(self):
        """删除学生所有会考做题信息"""
        stu_id = self.mysql.find_user_id(STUDENT_ACCOUNT)[0][0]
        self.mysql.delete_student_assessment_overview(stu_id)
        self.mysql.delete_student_assessment_record(stu_id)
        self.mysql.delete_student_wrong_record(stu_id)
        self.mysql.delete_student_wrong_note(stu_id)

    def get_section_sync_ques(self, section_id):
        """根据小节id获取选择与填空分组"""
        all_id = self.mysql.find_select_and_blank_game_by_id(section_id)
        ques_id_list = [x[0] for x in all_id]
        print('ques_id_list', ques_id_list)
        start, split_index  = 0, 0
        split_list = []
        for i, x in enumerate(ques_id_list):
            if i == 0:
                start = x
            else:
                if x == start:
                    start = x
                else:
                    split_list.append(ques_id_list[split_index:i])
                    start = x
                    split_index = i
        split_list.append(ques_id_list[split_index:len(ques_id_list)])
        print('split_list', split_list)
        first_select_count = len(split_list[0])
        if len(split_list) > 1:
            first_blank_count = len(split_list[1])
        else:
            first_blank_count = 0
            print('该小节同步练习不存在填空题')
        return first_select_count, first_blank_count


    def get_ques_right_answer(self, ques_id):
        """根据题目id获取正确答案"""
        ans_info = self.mysql.find_ques_answer_by_id(ques_id)
        game_type = ans_info[0][0]
        answer_content = ans_info[0][1]
        ref_content = json.loads(answer_content, encoding='utf-8')
        right_answer = 0
        if game_type == 203:
            right_answer = ref_content['#a']
        elif game_type == 204:
            right_answer = re.findall(r'.*?\[\[(.*?)\]\].*?', ref_content['#q'])
        return right_answer
