#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/16 16:40
# -----------------------------------------
from utils.sqldb import SqlDb


class PassionSql(SqlDb):

    def find_user_id(self, phone):
        """查询学生ID"""
        sql = 'SELECT id FROM `user` where phone = {} and user_type_id =2'.format(phone)
        return self.execute_sql_return_result(sql)

    def find_book_chapter_num(self, book_id):
        """查询书籍章节个数"""
        sql = "SELECT COUNT(`id`) FROM course_book_catalog WHERE book_id={} AND level = '1' AND deleted_at is NULL".format(book_id)
        return self.execute_sql_return_result(sql)

    def find_chapter_name_available_value_by_name(self, book_id, chapter_name, parent_id):
        """根据名称查询章节/小节是否已上架"""
        sql = "SELECT `id`, is_available FROM course_book_catalog WHERE book_id={} AND name='{}' " \
              "AND parent_id='{}' AND deleted_at is NULL".format(book_id, chapter_name, parent_id)
        return self.execute_sql_return_result(sql)

    def find_chapter_is_have_video(self, chapter_id):
        """获取章节是否有章节导学视频"""
        sql = "SELECT `id` FROM course_catalog_data WHERE catalog_id = '{}' ".format(chapter_id)
        return self.execute_sql_return_result(sql)

    def find_current_chapter_section_num(self, chapter_id):
        """查询当前章节的小节数"""
        sql = "SELECT `id`, is_available FROM course_book_catalog WHERE parent_id = {} AND deleted_at is NULL".format(chapter_id)
        return self.execute_sql_return_result(sql)

    def find_section_question_ids(self, book_id,  section_id):
        """查询小节的知识点"""
        sql = "SELECT question_count FROM assessment WHERE book_id='{}' AND catalog_id='{}' and " \
              "type_id=1 and deleted_at is NULL" .format(book_id, section_id)
        return self.execute_sql_return_result(sql)

    # ============== 删除学生会考记录 ================
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

    # ==================== 同步练习 ========================
    def find_select_and_blank_game_by_id(self, section_id):
        sql = "SELECT `game_id` FROM assessment_question WHERE catalog_id = {} and game_id in (203, 204) and " \
              "deleted_at is NULL order by `id`".format(section_id)
        return self.execute_sql_return_result(sql)

    def find_ques_answer_by_id(self, ques_id):
        """根据题目id查询答案"""
        sql = "SELECT game_id, content FROM assessment_question WHERE `id`='{}'".format(ques_id)
        return self.execute_sql_return_result(sql)