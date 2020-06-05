#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/19 10:05
# -----------------------------------------
import json

import urllib3
import requests

from conf.decorator import teststep


class Verify:

    @teststep
    def get_verify_code(self, phone, code_type="student_user_forget_password"):
        url = "https://dev.passion.vanthink.cn/api/auth/sms"
        r = requests.get(url, params={'student_phone': phone, 'code_type': code_type})
        return json.loads(r.text)['data']
