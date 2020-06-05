# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/29 8:50
# -------------------------------------------
import multiprocessing
import threading
import time
from selenium import webdriver
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from conf.case_strategy import CaseStrategy
from conf.log import Log
from conf.report_path import ReportPath
from conf.run_cases import RunCases
from utils.sqldb import SqlDb


class Driver:
    def run_cases(self):
        arg_list = []
        for x in range(len(gv.CASE_INFO)):
            pro_name = gv.CASE_INFO[x][0].split('/')[1]
            cs = CaseStrategy()
            cases = cs.collect_cases(index=x, suite=True)
            arg_list.append((cases, pro_name))
            # arg_list.append((gv.CASE_INFO[x], pro_name))

        pool = multiprocessing.Pool(len(arg_list))
        for x in arg_list:
            pool.apply_async(Driver().start_driver, args=x)
        pool.close()
        pool.join()

    @staticmethod
    def start_driver(case_info, pro_name):
        opt = webdriver.ChromeOptions()
        opt.add_experimental_option(
            "prefs",
            {"profile.default_content_setting_values.media_stream_mic": 1})
        driver = webdriver.Chrome(chrome_options=opt)
        driver.maximize_window()
        driver.get(gv.BASE_URL)
        run = RunCases(pro_name)
        log = Log()
        log.set_logger(pro_name, run.get_path() + '\\' + 'client.log')
        log.i('测试项目：' + pro_name)
        log.i('测试工具：selenium')
        log.i('输出报告：' + str(run.get_path()) + '\n')

        base_page = BasePage()
        base_page.set_driver(driver)
        #
        path = ReportPath()
        path.set_path(run.get_path())  #
        sql = SqlDb()
        try:
            sql.start_db()
            time.sleep(3)
            run.create_report(case_info)
            driver.quit()
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            print(e)
            driver.quit()
        sql.close_db()