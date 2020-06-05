#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/4/28 9:23
# -----------------------------------------
import datetime, allure
import json

from app.passion.object_page.sql_data import Sql
from app.passion.test_data.passion_config import *
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class SqlHandle(BasePage):

    def __init__(self):
        self.mysql = Sql()

    @teststep
    def get_stu_id(self):
        """获取学生id"""
        stu_id = self.mysql.find_user_id(STUDENT_ACCOUNT)
        if stu_id:
            return stu_id[0][0]
        else:
            return 0

    @teststep
    def get_user_by_phone(self, phone):
        """根据手机号获取学生id"""
        stu_id = self.mysql.find_user_id(phone)
        if stu_id:
            return True
        else:
            return False

    @allure.step('删除学生会考记录')
    @teststeps
    def delete_student_all_record(self):
        """删除学生所有会考做题信息"""
        stu_id = self.get_stu_id()
        self.mysql.delete_student_assessment_overview(stu_id)
        self.mysql.delete_student_assessment_record(stu_id)
        self.mysql.delete_student_wrong_record(stu_id)
        self.mysql.delete_student_wrong_note(stu_id)

    @teststep
    def get_section_total_count(self, section_name):
        """获取小节总题数"""
        nums = self.mysql.find_section_item_count(section_name)
        count_list = [x[0] for x in nums]
        return sum(count_list)

    @teststep
    def update_exam_date_operate(self, exam_name):
        """更改试卷做题时间"""
        start_time = datetime.datetime.now() - datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(minutes=1)
        stu_id = self.get_stu_id()
        exam_id = self.mysql.find_exam_id(exam_name)[-1][0]
        self.mysql.update_exam_date(start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"),
                                    stu_id, exam_id)

