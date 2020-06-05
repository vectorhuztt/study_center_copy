#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/19 10:55
# -----------------------------------------
from app.passion.test_data.passion_config import STUDENT_ACCOUNT


class ForgetData:
    FORGET_PHONE = [
        'avytqv125128asnm',   # 非数字形式
        '13456789',     # 不足11位数字
        '64762327839',  # 非1开头
        '1213432423423',  # 超过11位数字
        '16467090923',    # 非库中数据
        STUDENT_ACCOUNT,  # 正常数据
    ]
