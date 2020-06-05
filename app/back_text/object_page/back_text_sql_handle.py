#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/17 17:33
# -----------------------------------------
import datetime
import json

from app.back_text.object_page.back_text_sql import BackTextSql
from app.common_ele.account import STUDENT_ACCOUNT
from conf.base_page import BasePage
from conf.decorator import teststep


class BackTextSqlHandle(BasePage):

    def __init__(self):
        self.mysql = BackTextSql()

    @teststep
    def get_stu_id(self):
        """获取学生id"""
        stu_id = self.mysql.find_user_id(STUDENT_ACCOUNT)
        if stu_id:
            return stu_id[0][0]
        else:
            return 0

    @teststep
    def update_module_date_operate(self):
        """更新做题时间"""
        student_id = self.get_stu_id()
        now = datetime.datetime.now()
        yesterday = now + datetime.timedelta(days=-1)
        update_date = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        self.mysql.update_student_module_date(update_date, student_id)

    @teststep
    def get_one_bank_answer(self, bank_id):
        """获取一题一个答案信息"""
        bank_info = self.mysql.find_one_bank_answer(bank_id)
        if bank_info:
            item_value = bank_info[0][0]
            reform_info = json.loads("""{}""".format(item_value))
            return reform_info
        else:
            return None

    @teststep
    def get_multi_bank_answer(self, bank_id):
        """获取一题多个答案信息"""
        bank_info = self.mysql.find_multi_bank_answer(bank_id)
        if bank_info:
            reform_info = [json.loads("""{}""".format(x[0])) for x in bank_info]
            return reform_info
        else:
            return None

    @teststep
    def clear_student_text_overview(self):
        """清除学生背课文进度"""
        student_id = self.get_stu_id()
        print('学生id: ', student_id)
        self.mysql.delete_student_model_overview(student_id)
        self.mysql.delete_student_unit_overview(student_id)