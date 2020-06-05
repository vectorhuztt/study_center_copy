# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/29 9:08
# -------------------------------------------
import HTMLTestReportCN2
import HTMLTestRunner
import time
import os, pytest
from conf.base_config import GetVariable as gv


class RunCases:
    def __init__(self, test_pro_name):
        report_path = os.path.abspath(gv.REPORT_ROOT)
        if not os.path.exists(report_path):
            os.makedirs(report_path)
        date_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.test_report_path = report_path + '\\' + test_pro_name + '\\' + date_time + '\\'
        if not os.path.exists(self.test_report_path):
            os.makedirs(self.test_report_path)

        self.file_name = self.test_report_path + 'TestReport_' + date_time + '.html'

    def get_path(self):
        return self.test_report_path

    def create_report(self, case_info):
        desc = '用例执行情况统计：'
        report_title = '测试用例执行报告'
        fp = open(self.file_name, 'wb')
        runner = HTMLTestReportCN2.HTMLTestRunner(
            stream=fp,
            title=report_title,
            description=desc)
        runner.run(case_info)
        fp.close()

