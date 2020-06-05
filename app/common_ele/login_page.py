from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conf.base_page import BasePage
import time
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps


class LoginPage(BasePage):
    @teststep
    def wait_check_school_login_page(self):
        """学校登录页面检查点"""
        locator = (By.XPATH, '//*[contains(text(),"学校登录：")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_all_elements_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_student_login_page(self):
        """学校登录页面检查点"""
        locator = (By.XPATH, '//*[contains(text(),"学生登录：")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_all_elements_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_forget_pass_page(self):
        """学校登录页面检查点"""
        locator = (By.XPATH, '//*[contains(text(),"忘记密码：")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_all_elements_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_error_tip_page(self):
        """学校登录页面检查点"""
        locator = (By.CLASS_NAME, 'el-message__content')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_all_elements_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_into_home_page(self):
        """学校登录页面检查点"""
        locator = (By.CSS_SELECTOR, 'el-message__content')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_all_elements_located(locator))
            return True
        except:
            return False


    @teststep
    def input_ele(self):
        """学校标识码"""
        ele = self.driver.find_elements_by_css_selector(".admin-form .el-input__inner")
        return ele

    @teststep
    def form_btn(self):
        """管理员页面确定按钮"""
        ele = self.driver.find_elements_by_css_selector(".admin-form .el-button")
        return ele

    @teststep
    def forget_pass_btn(self):
        """忘记密码"""
        ele = self.driver.find_elements_by_css_selector('.back-school span')
        return ele[0]

    @teststep
    def back_school_btn(self):
        """返回学校登陆"""
        ele = self.driver.find_elements_by_css_selector('.back-school span')
        return ele[1]

    @teststep
    def forget_form_input(self):
        """忘记密码页面输入栏"""
        ele = self.driver.find_elements_by_css_selector('.forget-form .el-input input')
        return ele

    @teststep
    def error_tip_content(self):
        """错误提示信息"""
        ele = self.driver.find_element_by_class_name('el-message__content')
        return ele.text

    @teststep
    def get_verify_code_btn(self):
        """获取验证码"""
        ele = self.driver.find_element_by_css_selector('.verify-btn')
        return ele

    @teststep
    def forget_confirm_btn(self):
        """忘记密码页面确定按钮"""
        ele = self.driver.find_element_by_css_selector('.forget-form .btn-login')
        return ele

    @teststep
    def back_student_login_btn(self):
        """返回学生登录按钮"""
        ele = self.driver.find_element_by_class_name('back')
        return ele

    @teststep
    def clear_input(self, input_ele):
        """清除输入栏"""
        for x in range(input_ele.text):
            input_ele.send_keys(Keys.BACKSPACE)


    @teststep
    def school_login_operate(self, account, password):
        """学校登陆操作"""
        if self.driver.current_url == gv.BASE_URL:
            admin_account = self.input_ele()[0]
            admin_password = self.input_ele()[1]
            admin_account.click()
            admin_account.send_keys(account)  # 输入学校账号
            admin_password.click()
            admin_password.send_keys(password)  # 输入学校密码
            self.form_btn()[0].click()
            time.sleep(3)
        else:
            if 'https://dev.passion.vanthink.cn/#/learning-center/en/course' not in self.driver.current_url:
                self.driver.refresh()

    @teststeps
    def stu_login_operate(self, account, password):
        """学生登陆操作"""
        if self.wait_check_student_login_page():
            print(len(self.input_ele()))
            stu_account = self.input_ele()[2]
            stu_password = self.input_ele()[3]
            stu_account.click()
            stu_account.send_keys(account)  # 输入学生账号
            stu_password.click()
            stu_password.send_keys(password)  # 输入学生密码
            self.form_btn()[1].click()
            time.sleep(5)


    @teststeps
    def back_school_operate(self):
        """返回学校登录页面操作"""
        if self.wait_check_student_login_page():
            self.back_school_btn().click()
            if not self.wait_check_school_login_page():
                print('★★★ 未返回学校登录页面')
            else:
                self.school_login_operate()

    @teststeps
    def login_status(self, school_account, school_password, student_account, student_password):
        """登录"""
        if self.wait_check_school_login_page():
            self.school_login_operate(school_account, school_password,)
            # self.back_school_operate()
            # self.forget_password_operate()
            self.stu_login_operate(student_account, student_password)
        else:
            self.driver.refresh()
            time.sleep(4)