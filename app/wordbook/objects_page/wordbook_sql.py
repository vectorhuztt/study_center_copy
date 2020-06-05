#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/3 17:26
# -----------------------------------------
from utils.sqldb import SqlDb


class WordBookSql(SqlDb):

    def find_student_id_by_phone(self, phone):
        """根据手机号查找学生id"""
        sql = 'SELECT `id` FROM user WHERE  phone ="{}" and user_type_id=2'.format(phone)
        return self.execute_sql_return_result(sql)

    def find_student_name_by_id(self, stu_id):
        """根据学生id获取学生姓名"""
        sql = 'SELECT name FROM user WHERE  `id` = "{}"'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_book_type(self, book_id, stu_id):
        sql = 'SELECT mode FROM course_user_book_record WHERE student_id = "{}" ' \
              'and book_id="{}" order by id desc limit 1'.format(stu_id, book_id)
        return self.execute_sql_return_result(sql)

    # ========== 通过不同方式获取单词id、解释id ===========
    def find_explain_by_explain_id(self, explain_id):
        """根据解释id获取解释内容"""
        sql = 'SELECT `translation` FROM wordbank_translation WHERE `id` = "{}" ORDER BY  `id`'.format(explain_id)
        return self.execute_sql_return_result(sql)

    def find_word_by_word_id(self, word_id):
        """根据单词查询单词id"""
        sql = "SELECT vocabulary FROM wordbank WHERE `id` = '{}'".format(word_id)
        return self.execute_sql_return_result(sql)

    def find_word_by_explain_id(self, explain_id):
        """根据解释id查询单词"""
        sql = "SELECT vocabulary FROM wordbank where `id` = (select wordbank_id from wordbank_translation where `id` = '{}')".format(explain_id)
        return self.execute_sql_return_result(sql)

    def find_one_explain_by_word_id(self, student_id, book_id, word_id):
        """根据学生id、书籍id、单词id 查询其中之一的解释"""
        sql = 'SELECT translation FROM wordbank_translation where id =(SELECT translation_id FROM' \
              ' word_student_fluency WHERE student_id={} and book_id={} and wordbank_id = {} and deleted_at ' \
              'is NULL limit 1) and deleted_at is NULL'\
            .format(student_id, book_id, word_id)
        return self.execute_sql_return_result(sql)

    def find_explain_id_by_word_id_already(self, student_id, book_id, word_id):
        """根据单词id查询学生已背单词下对应的所有解释id"""
        sql = 'SELECT translation_id FROM word_student_fluency WHERE student_id = "{}" and book_id="{}" ' \
              'and wordbank_id = "{}" and fluency_level >=1'.format(student_id, book_id, word_id)
        return self.execute_sql_return_result(sql)

    def find_explain_id_by_word_id_today(self, student_id, book_id, word_id):
        """根据单词id查询学生今日已背单词下对应的所有解释id"""
        sql = 'SELECT translation_id FROM word_student_fluency WHERE student_id = "{}" and book_id="{}" ' \
              'and wordbank_id = "{}" and fluency_level >=1 and DATEDIFF(last_finish_at,NOW()) = 0 '.format(student_id, book_id, word_id)
        return self.execute_sql_return_result(sql)

    def find_word_id_by_explain_id(self, stu_id, explain_id):
        """根据解释id获取已学单词id"""
        sql = "SELECT wordbank_id FROM word_student_fluency WHERE student_id ='{}' and translation_id ='{}'".format(stu_id, explain_id)
        return self.execute_sql_return_result(sql)

    # ============= 根据单词id、解释id 获取对应解释的F值 ==================
    def find_explain_fluency_by_explain_id(self, student_id, explain_id):
        """根据解释id查询学生已背单词的F值"""
        sql = 'SELECT fluency_level FROM word_student_fluency WHERE student_id="{0}" ' \
              'and translation_id="{1}"'.format(student_id, explain_id)
        return self.execute_sql_return_result(sql)

    def find_explain_fluency_by_word_id(self, student_id, word_id):
        """根据解释id查询学生已背单词的F值"""
        sql = 'SELECT translation_id, fluency_level FROM word_student_fluency WHERE student_id="{0}" ' \
              'and wordbank_id="{1}" and fluency_level >=1 and deleted_at is NULL'.format(student_id, word_id)
        return self.execute_sql_return_result(sql)

    def find_student_book_word_count(self, student_id, book_id):
        """查询学生本书已被单词个数"""
        sql = 'SELECT DISTINCT(wordbank_id) FROM word_student_fluency ' \
              'WHERE student_id={} and book_id = {} and deleted_at is NULL'.format(student_id, book_id)
        return self.execute_sql_return_result(sql)

    # =======  更改学生背单词时间, 使其出现强制练习 ========
    def find_student_update_fluency_id(self, stu_id, book_id):
        """获取要修改完成时间的fluency_id"""
        sql = 'SELECT `id`, wordbank_id FROM  word_student_fluency WHERE student_id = "{}" and book_id = "{}" ' \
              'ORDER BY last_finish_at desc limit 3'.format(stu_id, book_id)
        return self.execute_sql_return_result(sql)

    def update_student_fluency_one_eq_two(self, stu_id, book_id):
        """将F值等于1的单词更改为F值等于2"""
        sql = 'UPDATE word_student_fluency SET fluency_level=2 WHERE student_id="{}" and book_id ="{}" ' \
              'and fluency_level=1'.format(stu_id, book_id)
        return self.execute_sql_only(sql)

    def update_student_word_fluency_date(self, fluency_id):
        """更改学生单词完成时间"""
        sql = 'UPDATE word_student_fluency SET fluency_level = 1, last_finish_at = DATE_ADD(NOW(),INTERVAL -1 DAY) ' \
              'WHERE `id` in ({})'.format(fluency_id)
        return self.execute_sql_only(sql)

    def find_student_latest_book_id(self, stu_id, book_id):
        """查询学生最新的图书记录id"""
        sql = 'SELECT `id` FROM word_student_data WHERE student_id ={} and `key`= "book_id" and `value` = "{}" ' \
              'order by `id` desc limit 1'.format(stu_id, book_id)
        return self.execute_sql_return_result(sql)

    def update_student_data_create_date(self, data_id):
        """更改学生data表时间数据"""
        sql = 'UPDATE word_student_data SET created_at = DATE_ADD(NOW(),INTERVAL -1 DAY) WHERE `id`= {}'.format(data_id)
        return self.execute_sql_only(sql)

    # ======== 查询单元id和单元的单词、测试 ========
    def find_unit_label_id(self, book_id, unit_name):
        """根据单元名称查询id"""
        sql = "SELECT `id` FROM core_label WHERE parent_id = " \
              "(SELECT core_label_id from word_book_core_label_map WHERE book_id ='{}') and name = '{}'"\
            .format(book_id, unit_name)
        return self.execute_sql_return_result(sql)

    def find_student_unit_has_before_test(self, stu_id, book_id,  unit_id):
        """查询本单元是否已经做过学前测试"""
        sql = "SELECT `id`, accuracy FROM word_student_examination WHERE type='learn_before_test' " \
              "and student_id = {} and book_id = {} and catalog_id = {}".format(stu_id, book_id, unit_id)
        return self.execute_sql_return_result(sql)

    def find_student_unit_has_after_test(self, stu_id, book_id, unit_id):
        """查询本单元是否已经做过学前测试"""
        sql = "SELECT `id`, accuracy FROM word_student_examination WHERE type='learn_after_test' " \
              "and student_id = {} and book_id = {} and catalog_id = {}".format(stu_id, book_id, unit_id)
        return self.execute_sql_return_result(sql)

    def find_translation_id_by_unit_id(self, unit_id):
        """查询单元下的单词解释id"""
        sql = "SELECT translation_id FROM wordbank_translation_label WHERE label_id = '{}'".format(unit_id)
        return self.execute_sql_return_result(sql)

    def find_unit_label_words_count(self, unit_id):
        """查询单元下的去重的单词id"""
        sql = "SELECT DISTINCT(wordbank_id) FROM wordbank_translation_label WHERE label_id = '{}'".format(unit_id)
        return self.execute_sql_return_result(sql)

    # ========= 查询单元今日已学单词、已学单词、以及单元单词 =============
    def find_unit_today_study_word_id(self, stu_id, explain_id):
        """查询单元今日新学"""
        sql = "SELECT `wordbank_id` FROM word_student_fluency WHERE student_id = {} and  translation_id in ({}) and fluency_level = 1 " \
              "and DATEDIFF(NOW(), last_finish_at) = 0".format(stu_id, explain_id)
        return self.execute_sql_return_result(sql)

    def find_unit_today_already_word(self, stu_id, explain_id):
        """查询单元已学单词"""
        sql = "SELECT `wordbank_id` FROM word_student_fluency WHERE student_id = {} and  " \
              "translation_id in ({}) and fluency_level >= 1 ".format(stu_id, explain_id)
        return self.execute_sql_return_result(sql)

    def find_unit_all_words(self, stu_id, explain_id):
        sql = "SELECT `wordbank_id` FROM word_student_fluency WHERE student_id = {} and  " \
              "translation_id in ({})".format(stu_id, explain_id)
        return self.execute_sql_return_result(sql)

    # ========== 删除该学生单元的单词学习记录以及学前或者学后测试记录 ===========
    def find_fluency_id_by_translation_id(self, stu_id, translation_id):
        """根据解释id获取当前解释的fluency id"""
        sql = "SELECT `id` FROM word_student_fluency WHERE " \
              "student_id ={} AND translation_id in ({})".format(stu_id, translation_id)
        return self.execute_sql_return_result(sql)

    def delete_fluency_record_by_id(self, fluency_id):
        """根据学生的fluency id 删除fluency record"""
        sql = "DELETE FROM word_student_fluency_record WHERE student_fluency_id in ({})".format(fluency_id)
        return self.execute_sql_only(sql)

    def delete_student_word_fluency_by_id(self, fluency_ids):
        """删除学生单词"""
        sql = 'DELETE FROM `word_student_fluency` WHERE `id` in ({})'.format(fluency_ids)
        return self.execute_sql_only(sql)

    def delete_student_unit_word_record(self, stu_id, unit_id):
        """删除单元完成记录"""
        sql = "DELETE FROM `word_student_record` WHERE `student_id` = '{}' and object_id={}".format(stu_id, unit_id)
        return self.execute_sql_only(sql)

    def delete_student_book_wrong_record(self, stu_id, book_id):
        """删除学生错题记录"""
        sql = "DELETE FROM `word_student_wrong` WHERE `student_id` = '{}' and book_id={}".format(stu_id, book_id)
        return self.execute_sql_only(sql)

    def find_student_unit_word_test_id(self, stu_id, book_id, unit_id):
        """查询学生测试id"""
        sql = "SELECT `id` FROM  word_student_examination WHERE student_id ='{}' " \
              "and book_id='{}' and  catalog_id={}".format(stu_id, book_id, unit_id)
        return self.execute_sql_return_result(sql)

    def delete_student_word_test_wrong_record_by_test_id(self, stu_id, test_id):
        """删除学生单词测试错题记录"""
        sql = "DELETE FROM `word_student_examination_wrong` WHERE `student_id` = '{}' and examination_id='{}' ".format(stu_id, test_id)
        return self.execute_sql_only(sql)

    def delete_student_word_test_record_by_id(self, test_id):
        """根据测试id删除测试记录"""
        sql = "DELETE FROM `word_student_examination` WHERE `id` = '{}'".format(test_id)
        return self.execute_sql_only(sql)






