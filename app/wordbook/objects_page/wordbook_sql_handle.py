#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/9/4 8:59
# -----------------------------------------
from app.wordbook.objects_page.wordbook_sql import WordBookSql
from conf.decorator import teststep


class WordBookSqlHandle:

    def __init__(self):
        self.mysql = WordBookSql()


    @teststep
    def get_student_id(self, phone):
        """获取学生id"""
        result = self.mysql.find_student_id_by_phone(phone)
        return result[0][0]

    @teststep
    def get_user_name(self, stu_id):
        """根据id获取学生姓名"""
        result = self.mysql.find_student_name_by_id(stu_id)
        return result[0][0]

    @teststep
    def get_book_type(self, book_id, stu_id):
        """获取当前图书类型"""
        result = self.mysql.find_book_type(book_id, stu_id)
        return result[0][0]

    @teststep
    def get_word_id_by_word(self, word):
        """根据单词查询单词id"""
        result = self.mysql.find_word_by_word_id(word)
        return result[0][0] if len(result) else -1

    @teststep
    def get_word_by_word_id(self, word_id):
        """根据单词id获取单词"""
        result = self.mysql.find_word_by_word_id(word_id)
        return result[0][0]

    @teststep
    def get_word_by_explain_id(self, explain_id):
        """根据解释id获取单词"""
        result = self.mysql.find_word_by_explain_id(explain_id)
        return result[0][0]

    @teststep
    def get_unit_word_id_already(self, stu_id, unit_explain_id):
        """根据单词id查询解释id 已学"""
        result = self.mysql.find_unit_today_already_word(stu_id, unit_explain_id)
        return list(set([x[0] for x in result])) if result else []

    @teststep
    def get_unit_word_id_today(self, stu_id, unit_explain_id):
        """根据单词id查询解释id 今日学习"""
        result = self.mysql.find_unit_today_study_word_id(stu_id, unit_explain_id)
        return list(set([x[0] for x in result])) if result else []

    @teststep
    def get_unit_all_word_id(self, stu_id, unit_explain_id):
        """单元所有单词"""
        result = self.mysql.find_unit_all_words(stu_id, unit_explain_id)
        return list(set([x[0] for x in result])) if result else []

    @teststep
    def get_explain_ids_by_word_id_already(self, stu_id, book_id, word_id):
        """查询已学单词对应的单词解释id"""
        try:
            result = self.mysql.find_explain_id_by_word_id_already(stu_id, book_id, word_id)
            return [x[0] for x in result]
        except:
            return []

    @teststep
    def get_explain_ids_by_word_id_today(self, stu_id, book_id, word_id):
        """查询今日已学单词id对应的解释id"""
        try:
            result = self.mysql.find_explain_id_by_word_id_today(stu_id, book_id, word_id)
            return [x[0] for x in result]
        except:
            return []

    @teststep
    def get_explain_by_explain_id(self, explain_id):
        """根据解释id获取解释"""
        explain = self.mysql.find_explain_by_explain_id(explain_id)
        try:
            result = explain[0][0]
            return result
        except:
            return None

    @teststep
    def get_explain_fluency_by_explain_id(self, student_id, explain_id):
        """根据解释id查询对应的F值"""
        result = self.mysql.find_explain_fluency_by_explain_id(student_id, explain_id)
        return result[0][0] if result else 0

    @teststep
    def get_explain_fluency_by_word_id(self, stu_id, word_id):
        """根据单词id获取对应已学解释id及F值"""
        result = self.mysql.find_explain_fluency_by_word_id(stu_id, word_id)
        return {result[0][0]: result[0][1]} if result else {}

    @teststep
    def get_student_book_word_count(self, student_id, book_id):
        """获取学生当前书籍已背单词总数"""
        book_word_ids = self.mysql.find_student_book_word_count(student_id, book_id)
        return [x[0] for x in book_word_ids] if book_word_ids else []

    @teststep
    def get_word_id_by_explain_id(self, stu_id, explain_id):
        """根据解释id获取单词id"""
        result = self.mysql.find_word_id_by_explain_id(stu_id, explain_id)
        return result[0][0]

    @teststep
    def get_student_explain_list_by_word_id(self, stu_id, book_id, word_id, exam_type=2):
        """根据单词id获取所有的解释列表， 并以分号分割
            :param book_id:  书籍id
            :param exam_type: 试卷类型
            :param word_id: 单词id
            :param stu_id  学生id
        """
        if exam_type == 2:
            explain_id_list = self.get_explain_ids_by_word_id_already(stu_id, book_id, word_id)
        else:
            explain_id_list = self.get_explain_ids_by_word_id_today(stu_id, book_id, word_id)

        if len(explain_id_list):
            all_explain = ' '.join([self.get_explain_by_explain_id(x) for x in explain_id_list
                                    if self.get_explain_by_explain_id(x)]).split('；')
        else:
            all_explain = []
        return all_explain

    @teststep
    def update_student_word_date_to_review(self, stu_id, book_id):
        """更改学生信息去强制复习"""
        update_id_info = self.mysql.find_student_update_fluency_id(stu_id, book_id)
        fluency_ids = str([x[0] for x in update_id_info]).replace('[', '').replace(']', '')
        word_ids = [x[1] for x in update_id_info]
        self.mysql.update_student_fluency_one_eq_two(stu_id, book_id)
        self.mysql.update_student_word_fluency_date(fluency_ids)
        data_id = self.mysql.find_student_latest_book_id(stu_id, book_id)
        self.mysql.update_student_data_create_date(data_id[0][0])
        return word_ids


    @teststep
    def get_unit_has_test(self, stu_id, book_id, unit_id, is_after=False):
        """获取单元是否已经做过学前测试"""
        if is_after:
            unit_test_info = self.mysql.find_student_unit_has_after_test(stu_id, book_id, unit_id)
        else:
            unit_test_info = self.mysql.find_student_unit_has_before_test(stu_id, book_id, unit_id)
        print("学前学后测试信息：", unit_test_info)
        if len(unit_test_info):
            return unit_test_info[0]
        else:
            return False

    @teststep
    def get_unit_catalog_id(self, book_id, unit_name):
        """获取单元id"""
        unit_id = self.mysql.find_unit_label_id(book_id, unit_name)
        return unit_id[0][0]

    @teststep
    def get_unit_words_count(self, unit_id):
        """获取本单元所有单词数"""
        unit_words = self.mysql.find_unit_label_words_count(unit_id)
        return len(unit_words) if len(unit_words) else 0

    @teststep
    def get_unit_word_translations_ids(self, unit_id):
        """获取单元下所有的解释id"""
        translations = self.mysql.find_translation_id_by_unit_id(unit_id)
        if len(translations):
            return [x[0] for x in translations]
        else:
            return []

    @teststep
    def delete_student_unit_word_record(self, stu_id, book_id,  unit_id):
        """删除学生单词学习记录和单词测试记录"""
        unit_test_ids = self.mysql.find_student_unit_word_test_id(stu_id, book_id, unit_id)
        unit_translation_ids = str(self.get_unit_word_translations_ids(unit_id)).replace('[', '').replace(']', '')
        fluency_ids = self.mysql.find_fluency_id_by_translation_id(stu_id, unit_translation_ids)
        print('unit_test_ids:', unit_test_ids)
        print('unit_translations_ids: ', unit_translation_ids)
        print('fluency_ids:', fluency_ids, '\n')

        if len(unit_test_ids):
            for x in unit_test_ids:
                self.mysql.delete_student_word_test_wrong_record_by_test_id(stu_id, x[0])
                self.mysql.delete_student_word_test_record_by_id(x[0])

        if len(fluency_ids):
            reform_fluency_ids = str([x[0] for x in fluency_ids]).replace('[', '').replace(']', '')
            self.mysql.delete_fluency_record_by_id(reform_fluency_ids)
            self.mysql.delete_student_word_fluency_by_id(reform_fluency_ids)
        self.mysql.delete_student_unit_word_record(stu_id, unit_id)
        self.mysql.delete_student_book_wrong_record(stu_id, book_id)



