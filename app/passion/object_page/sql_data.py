# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/15 9:56
# -------------------------------------------
from utils.sqldb import SqlDb


class Sql(SqlDb):

    def find_chapter_assessment_questions(self, book_id,  chapter_id):
        """查询章节考核的所有物问题"""
        sql = "SELECT question_ids FROM assessment WHERE book_id='{0}'  AND catalog_id='{1}'".format(book_id, chapter_id)
        return self.execute_sql_return_result(sql)

    def find_book_exam_question(self, exam_name, type_id=4):
        """查询书籍试卷问题id"""
        sql = "SELECT question_ids FROM assessment WHERE name='{0}'  AND type_id='{1}'".format(exam_name, type_id)
        return self.execute_sql_return_result(sql)

    def find_game_type_content(self, question_id):
        """查询问题对应的题型和内容"""
        sql = "SELECT game_id, content FROM assessment_question WHERE id in {}".format(question_id)
        return self.execute_sql_return_result(sql)

    def find_catalog_id_by_name(self, name, chapter_id):
        """根据名称查找小节id"""
        sql = "SELECT id FROM course_book_catalog WHERE name = '{}' and parent_id = {}".format(name, chapter_id)
        return self.execute_sql_return_result(sql)

    def find_section_question_ids(self, book_id, catalog_id):
        """查询小节练习的问题id"""
        sql = 'SELECT question_ids FROM assessment WHERE type_id=2 AND book_id={0} AND catalog_id={1}'\
            .format(book_id, catalog_id)
        return self.execute_sql_return_result(sql)

    def find_questions_by_exam_name(self, exam_name):
        """根据试卷名称查询试卷题目"""
        sql = 'SELECT question_ids FROM assessment WHERE `name` = "{}"'.format(exam_name)
        return self.execute_sql_return_result(sql)

    def find_question_id_by_content(self, question):
        """根据题目查询题目id"""
        sql = 'SELECT id FROM assessment_question WHERE content LIKE "%{}%"'.format(question)
        return self.execute_sql_return_result(sql)

    def find_user_id(self, phone):
        """查询学生ID"""
        sql = 'SELECT id FROM `user` where phone = {} and user_type_id =2'.format(phone)
        return self.execute_sql_return_result(sql)

    def delete_student_wrong_note(self, stu_id):
        """删除所有错题本"""
        sql = 'DELETE FROM assessment_student_wrong_note WHERE student_id = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_wrong_record(self, stu_id):
        """删除所有错题记录"""
        sql = 'DELETE FROM assessment_student_record_wrong WHERE student_id = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_assessment_record(self, stu_id):
        """删除所有测试记录"""
        sql = 'DELETE FROM assessment_student_record WHERE student_id = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_assessment_overview(self, stu_id):
        """删除overview表中学生记录"""
        sql = 'DELETE FROM assessment_student_overview WHERE student_id = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def find_section_item_count(self, section_name):
        """查询小节练习的知识点以及小节练习题数"""
        sql = 'SELECT assessment.question_count FROM assessment, course_book_catalog as cbc where' \
              ' assessment.catalog_id = cbc.id AND cbc.`name` = "{}"'.format(section_name)
        return self.execute_sql_return_result(sql)

    def find_exam_id(self, exam_name):
        """根据试卷名称查询id"""
        sql = 'SELECT id FROM assessment WHERE `name` = "{}"'.format(exam_name)
        return self.execute_sql_return_result(sql)

    def update_exam_date(self, start_time, end_time, stu_id, assessment_id):
        """更改试卷做题时间"""
        sql = "UPDATE assessment_student_record  SET start_time='{0}', end_time='{1}', created_at= '{1}'," \
              " updated_at = '{1}' WHERE assessment_id ={2} AND student_id={3}"\
            .format(start_time, end_time, stu_id, assessment_id)
        return self.execute_sql_only(sql)

    def get_all_exam(self, book_id):
        """查询所有试卷"""
        sql = 'SELECT count(name) FROM `assessment` WHERE `book_id` = "{}" AND `type_id`=4'.format(book_id)
        return self.execute_sql_return_result(sql)
