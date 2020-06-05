#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/17 17:33
# -----------------------------------------
from utils.sqldb import SqlDb


class BackTextSql(SqlDb):

    def find_user_id(self, phone):
        """查询学生ID"""
        sql = 'SELECT id FROM `user` where phone = {} and user_type_id =2'.format(phone)
        return self.execute_sql_return_result(sql)

    def find_one_bank_answer(self, bank_id):
        """查询单一题目答案"""
        sql = 'SELECT item_value FROM `assessment_question_entity` WHERE `id` = "{}"'.format(bank_id)
        return self.execute_sql_return_result(sql)

    def find_multi_bank_answer(self, bank_id):
        """查询一题多个答案"""
        sql = 'SELECT item_value FROM `assessment_question_entity` WHERE `question_id` = "{}"'.format(bank_id, bank_id)
        return self.execute_sql_return_result(sql)

    def delete_student_model_overview(self, stu_id):
        """删除模块记录"""
        sql = 'DELETE FROM `assessment_student_overview` WHERE `student_id`={}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_unit_overview(self, stu_id):
        """删除单元进度"""
        sql = 'DELETE FROM `course_student_overview` WHERE `student_id`={}'.format(stu_id)
        return self.execute_sql_only(sql)

    def update_student_module_date(self, update_date, stu_id):
        """更改进度保存时间"""
        sql = 'UPDATE `assessment_student_overview` SET `updated_at` = "{}", `created_at`="{}" WHERE `student_id` = {}'\
            .format(update_date, update_date, stu_id)
        return self.execute_sql_only(sql)
