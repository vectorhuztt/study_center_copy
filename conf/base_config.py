# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/29 9:09
# -------------------------------------------


class GetVariable(object):
    # 线上
    # HOST = '172.17.201.200'
    # PASSWORD = '8B#T&Bel'

    # Dev
    HOST = '172.17.0.200'
    USER_NAME = 'director'
    PASSWORD = 'r0#pX8^V'
    DB = 'learning'

    # #Test
    # HOST = '172.17.0.23'
    # USER_NAME = 'LuminEe'
    # PASSWORD = 'mysql#0056'
    # DB = 'learning'

    REPORT_ROOT = 'storges/test_report'  # 测试报告存放路径
    SUIT_PATH = 'app'
    # CASE_PATH = 'app/passion/test_cases'
    CASE_INFO = [
        ('app/wordbook/test_cases', 'test_002*.py'),
        # ('app/back_text/test_cases', 'test_001*.py'),
        # ('app/passion/test_cases', 'test006*.py')
    ]

    # DEV
    BASE_URL = 'https://dev.passion.vanthink.cn/#/login'

    # TEST
    # BASE_URL = 'https://test.passion.vanthink.cn/#/login'


