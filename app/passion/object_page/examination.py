import datetime
import json
import random
import re
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.passion.object_page.sql_data import Sql
from app.passion.object_page.entry_operation import EntryOperation
from app.passion.object_page.hadle_answer import HandleAnswer
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class OldExam(BasePage):

    def __init__(self):
        super().__init__()
        self.entry = EntryOperation()

    @teststep
    def wait_check_exam_page(self):
        """真题模考开始页面检查点"""
        locator = (By.XPATH, '//*[text()="真题模考"]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_exam_record_list_page(self):
        """试卷记录页面检查点"""
        locator = (By.XPATH, '//*[contains(text(),"真题目录")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_exam_result_page(self):
        """真题模考开始页面检查点"""
        locator = (By.CLASS_NAME, 'score')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_answer_card_page(self):
        """答题卡页面检查点"""
        locator = (By.XPATH, '//*[text()="答题卡"]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_submit_tip_page(self):
        """交卷提示页面"""
        locator = (By.XPATH, '//*[contains(text(),"确定要交卷吗")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_exam_result_detail_page(self):
        """试卷提交页面检查点"""
        locator = (By.CLASS_NAME, 'exam-detail')
        return self.get_wait_check_page_result(locator)

    @teststep
    def test_content(self):
        """模块内容"""
        ele = self.driver.find_element_by_class_name('ready')
        return "✅✅" + ele.text

    @teststep
    def exam_group_ele(self):
        """所有试卷记录"""
        ele = self.driver.find_elements_by_xpath('//*[contains(@class,"el-table__body-wrapper")]/table/tbody/tr')
        return ele

    @teststep
    def get_page_exam_num(self):
        """返回试卷索引数组"""
        return [i for i in range(len(self.exam_group_ele()))]

    @teststep
    def exam_name(self, exam_ele):
        """试卷名称"""
        ele = exam_ele.find_element_by_xpath('./td[1]/div')
        return ele.text

    @teststep
    def page_num(self):
        """页码"""
        ele = self.driver.find_elements_by_xpath('//*[@class="el-pager"]/li')
        return ele

    @teststep
    def latest_exam_date(self, exam_ele):
        """最新的做题时间"""
        ele = exam_ele.find_element_by_xpath('./td[2]/div/span')
        return ele.text

    @teststep
    def used_time(self, exam_ele):
        """耗时"""
        ele = exam_ele.find_element_by_xpath('./td[3]/div/span')
        return ele.text

    @teststep
    def exam_grade(self, exam_ele):
        """成绩"""
        ele = exam_ele.find_element_by_xpath('./td[4]/div/span')
        return ele.text

    @teststep
    def start_exam_by_ele(self, exam_ele):
        """开始考试"""
        ele = exam_ele.find_element_by_xpath('./td[5]/div/button[1]/span')
        print(ele.get_attribute('class'))
        print(ele.text)
        return ele

    @teststep
    def exam_record_list_exit_icon(self):
        """试卷记录页面退出按钮"""
        ele = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[5]/div/div/div/div[1]/div/div/div[1]/span/i')
        return ele

    @teststep
    def check_report(self, exam_ele):
        """查看报告"""
        ele = exam_ele.find_element_by_xpath('./td[5]/div/button[2]')
        return ele

    @teststep
    def check_report_span(self, exam_ele):
        ele = exam_ele.find_element_by_xpath('./td[5]/div/button[2]/span')
        print(ele.get_attribute('class'))
        print(ele.text)
        return ele


    @teststep
    def start_exam(self):
        """开始考试按钮"""
        ele = self.driver.find_element_by_xpath("//*[@class='ready']/div/button")
        return ele

    @teststep
    def exam_chapter_name(self):
        """章考核的章节名称"""
        ele = self.driver.find_element_by_xpath('//*[@class="ready"]/h1')
        return ele.text.split(' ')[1]

    @teststep
    def exam_title(self):
        ele = self.driver.find_element_by_xpath('//*[@class="ready"]/h2')
        return ele.text

    @teststep
    def blank_fall(self):
        """填空题题目"""
        ele = self.driver.find_elements_by_class_name("blank-wrap")
        return ele

    @teststep
    def choose_question(self):
        """选择题问题"""
        ele = self.driver.find_element_by_xpath("//*[@class='question']/span")
        return ele.text.strip()

    @teststep
    def choice_options(self):
        """选择题选项"""
        ele = self.driver.find_elements_by_class_name("text")
        return ele

    @teststep
    def container(self):
        ele = self.driver.find_element_by_xpath('//*[@class="hk-dialog-wrap"]/div/div')
        return ele.get_attribute('class')

    @teststep
    def choose_answer(self):
        """选择题答案"""
        ele = self.driver.find_elements_by_xpath("//*[@class='option']/div[2]")
        return ele

    @teststep
    def blank_question_span(self):
        """填空题干"""
        ele = self.driver.find_elements_by_xpath("//*[@class='bq-wrap']/span/span")
        return ''.join([x.text for x in ele]).replace('\n', '')

    @teststep
    def blank_input(self):
        """填空题的空白格"""
        ele = self.driver.find_elements_by_class_name('blank-input')
        return ele

    @teststep
    def pre_icon(self):
        """上一题图标"""
        ele = self.driver.find_element_by_class_name('icon-arrow-left')
        return ele

    @teststep
    def next_icon(self):
        """下一题图标"""
        ele = self.driver.find_element_by_class_name('icon-arrow-right')
        return ele

    @teststep
    def result_icon(self):
        """答题卡图标"""
        ele = self.driver.find_elements_by_class_name('icon-card')
        return ele[1]

    @teststep
    def number(self):
        """题号图标"""
        ele = self.driver.find_elements_by_xpath('//*[@class="detail"]/span')
        return ele

    @teststep
    def finish_up_button(self):
        """交卷按钮"""
        ele = self.driver.find_element_by_xpath('//*[@class="button-wrap"]/button')
        return ele

    @teststep
    def tip_content(self):
        """交卷提示信息"""
        ele = self.driver.find_element_by_class_name('el-message-box')
        return ele.text

    @teststep
    def confirm_btn(self):
        """确定按钮"""
        ele = self.driver.find_element_by_xpath('//*[@class="el-message-box__btns"]/button[2]')
        return ele

    @teststep
    def result_number(self):
        """结果页题数"""
        ele = self.driver.find_elements_by_xpath('//*[@class="hk-dialog-wrap"]/div[2]/div[2]/span')
        return ele

    @teststep
    def exam_score(self):
        """考试分数"""
        ele = self.driver.find_element_by_class_name('score')
        return ele.text

    @teststep
    def result_tag(self):
        """结果页提示"""
        ele = self.driver.find_element_by_class_name('tagline')
        return ele.text

    @teststep
    def exam_result_tip(self):
        """分数下方文字提示"""
        ele = self.driver.find_element_by_class_name('tagline')
        return ele.text

    @teststep
    def exam_result_exit_icon(self):
        """考试结果页退出图标"""
        ele = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[3]/div/div/'
                                                'div[1]/div/div/div[1]/span/i')

        return ele

    @teststep
    def back_btn(self):
        """返回按钮"""
        ele = self.driver.find_element_by_xpath('//*[text()="返回"]')
        return ele

    @teststep
    def get_bank_type_by_ques_num(self, index):
        """根据题号获取题目属性"""
        ele = self.driver.find_element_by_xpath('//*[text()="{}"]/../../..'.format(index))
        return ele.get_attribute('class')

    @teststep
    def get_dx_question_by_ques_num(self, index):
        """根据题号获取单选题单"""
        ele = self.driver.find_element_by_xpath('//*[text()="{}"]/following-sibling::span'.format(index))
        return ele.text

    @teststep
    def get_dx_options_by_ques_num(self, index):
        """根据题号获取 选项和选项内容"""
        opt_and_char_div = self.driver.find_element_by_xpath('//*[text()="{}"]/../following-sibling::div'.format(index))
        opt_text = opt_and_char_div.find_elements_by_class_name('text')
        return opt_text

    @teststep
    def get_opt_char_by_text_ele(self, text_ele):
        """根据选项内容获取选项"""
        ele = text_ele.find_element_by_xpath('./preceding-sibling::div/span')
        return ele.text

    @teststep
    def get_char_status_by_opt_text(self, opt):
        """根据选项内容获取选项的状态"""
        ele = self.driver.find_element_by_xpath('//*[text()="{}"]/preceding-sibling::div'.format(opt))
        return ele.get_attribute('class')

    @teststep
    def get_bq_question_by_ques_num(self, index):
        """根据题号获取填空问题"""
        ele = self.driver.find_elements_by_xpath('//*[text()="{}"]/following-sibling::span/span'.format(index))
        return ''.join([x.text for x in ele]).replace('\n', '')

    @teststep
    def get_bq_answer_by_ques_num(self, index):
        """根据题号获取填空答案"""
        ele = self.driver.find_elements_by_xpath('//*[text()="{}"]/following-sibling::span/div/p/span'.format(index))
        error_text = [e.text.lower().strip() for i, e in enumerate(ele) if i % 2 == 0]
        correct_text = [e.text.lower().strip() for i, e in enumerate(ele) if i % 2 != 0]
        return error_text, correct_text

    @teststep
    def get_explain_by_ques_num(self, index):
        """根据题号获取解释"""
        ele = self.driver.find_element_by_xpath('//*[text()="{}"]/../following-sibling::p'.format(index))
        return ele.text

    @teststep
    def find_ques_id(self, answers):
        """根据题干获取题目id"""
        # 获取题目的id
        bank_whole_text = self.blank_question_span()
        for x in answers:
            bank_whole_text = bank_whole_text.replace(" {} ".format(x), "[[{}]]".format(x))
        unicode_ques = bank_whole_text.encode('unicode-escape').decode('utf-8').replace(r'\u', '_u')
        question_id = Sql().find_question_id_by_content(unicode_ques)
        return str(question_id)

    @teststep
    def get_question_id(self):
        """获取题目的id"""
        ele = self.driver.find_element_by_xpath('//*[@class="van-dialog hk-dialog"]')
        return ele.get_attribute('data-exercise-id')

    @teststep
    def exam_process_exit_icon(self):
        """试卷做题过程退出按钮"""
        ele = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/span/i')
        return ele




    @teststeps
    def check_exam_info_operate(self, select_ele, wrong_index):
        """做完试题， 真题目录页面数据校验"""
        print('--- 校验目录页面数据 ---\n')
        if self.wait_check_exam_record_list_page():
            grade = self.exam_grade(select_ele)
            if len(wrong_index) == 0:
                if grade != '100':
                    print('★★★ 分数不正确，应为100', grade)
            else:
                if grade == '100' or grade == '-':
                    print('★★★ 分数不正确', grade)


            if self.latest_exam_date(select_ele) != datetime.datetime.now().strftime('%Y-%m-%d'):
                print('★★★ 做题时间不是今日日期')
            else:
                print('日期核实正确')

            if 'has-reports' not in self.check_report(select_ele).get_attribute('class'):
                print('★★★ 试卷已完成，但是查看报告未点亮')
            else:
                print('报告状态核实正确')

        print('-'*30, '\n')



    @teststeps
    def report_detail_operate(self, mine_answer, exam_record, exam_answers):
        """查看每道题的详情"""
        time.sleep(3)
        if self.wait_check_exam_result_page():
            print('====  报告详情页 ==== \n')
            # print("我的答案：", self.reform_json(mine_answer))
            # print('选择选项顺序：', self.reform_json(exam_record), '\n')
            dx_answers = exam_answers['选择']
            for i, x in enumerate(self.result_number()):
                x.click()
                time.sleep(1)
                if not self.wait_check_exam_result_detail_page():
                    print('★★★ 未进入结果详情页', x.text)
                else:
                    ques_index = str(i + 1) + '、'                                      # 获取题号
                    if self.get_bank_type_by_ques_num(ques_index) == 'dx-container':    # 根据题号获取祖父级元素属性，判断是否为选择题
                        dx_ques = self.get_dx_question_by_ques_num(ques_index)          # 获取选择题目
                        print('题目：', dx_ques)
                        try:
                            my_answer = mine_answer[dx_ques]                                # 我的答案
                            correct_answer = dx_answers[dx_ques]                            # 正确答案
                            option_list = exam_record[dx_ques]                              # 做题时选项顺序
                            dx_options = self.get_dx_options_by_ques_num(ques_index)        # 获取选项
                            if option_list != [x.text for x in dx_options]:                 # 判断选项是否一致
                                print('★★★ 查看报告中的选项顺序与做题时不一致！')

                            print('我的选项：', my_answer)
                            print('正确选项：', correct_answer)
                            for opt in dx_options:                                          # 判断选项的正对是不是【对】【错】
                                if opt.text == correct_answer:
                                    if self.get_opt_char_by_text_ele(opt) != '对':
                                        print('★★★ 选项正确，选标内容不是【对】')
                                else:
                                    if opt.text == my_answer:
                                        if self.get_opt_char_by_text_ele(opt) != '错':
                                            print('★★★ 选项不正确，选标内容不是【错】')
                                    else:
                                        if self.get_opt_char_by_text_ele(opt) != '-':
                                            print('★★★ 其余选项，选标内容不是【-】')
                        except:
                            print('★★★ 本题未选择')

                    else:                                                              # 填空题操作
                        bq_ques = self.get_bq_question_by_ques_num(ques_index)         # 填空题去除横线后的内容，key
                        print('问题：', bq_ques)
                        try:
                            my_answer = mine_answer[bq_ques]                               # 我的答案
                            error_answer = self.get_bq_answer_by_ques_num(ques_index)[0]   # 错误答案
                            correct_text = self.get_bq_answer_by_ques_num(ques_index)[1]   # 正确答案
                            print('我的答案：', my_answer)
                            print('页面错误答案：', error_answer)
                            print('页面正确答案：', correct_text)
                            done_answer = error_answer if all(error_answer) else correct_text
                            if my_answer != done_answer:
                                print('★★★ 填入的答案与页面展示的不一致')
                        except:
                            print('★★★ 本题未填空或者未完成')

                    print(self.get_explain_by_ques_num(ques_index))
                    print('-'*30, '\n')
                    time.sleep(1)
                    self.back_btn().click()
            self.exam_result_exit_icon().click()
            time.sleep(2)

    @teststep
    def exam_exit_operate(self, exam_type=1):
        """
        试卷做指定题退出
        :param exam_type: 做题类型 1:章节考核 2 真题模考
        """
        answer_info = {}
        print('试卷做指定题退出处理\n')
        print(self.test_content())

        url = self.driver.current_url
        book_id = re.findall(r'\d+', url)[0]
        if exam_type == 1:                                           # 获取章节考核答案
            chapter_name = self.exam_chapter_name()
            chapter_id = Sql().find_catalog_id_by_name(chapter_name, 0)
            question_ids = Sql().find_chapter_assessment_questions(book_id, chapter_id[0][0])
        else:                                                        # 获取真题模考答案
            chapter_name = self.exam_title()
            question_ids = Sql().find_questions_by_exam_name(chapter_name)

        exam_answer = HandleAnswer().get_exam_answers(question_ids)  # 获取本张试卷的全部答案
        self.start_exam().click()
        time.sleep(2)
        self.result_icon().click()
        time.sleep(2)
        for x in [1, len(self.number()) - 2]:
            if self.wait_check_answer_card_page():
                num = self.number()[x].text
                self.number()[x].click()
                time.sleep(1)
                if self.container() == 'dx-container':
                    choices = self.choose_answer()
                    random_index = random.randint(0, len(choices) - 1)
                    mine_answer = choices[random_index].text
                    answer_info[num] = mine_answer
                    choices[random_index].click()
                    time.sleep(0.5)

                elif self.container() == 'bq-container':
                    input_wraps = self.blank_input()
                    answers = []
                    for i in input_wraps:
                        i.click()
                        random_letters = ''.join(random.sample(string.ascii_lowercase, 4))
                        answers.append(random_letters)
                        i.send_keys(random_letters + Keys.ENTER)
                        time.sleep(0.5)

                    answer_info[num] = answers
            self.result_icon().click()
            time.sleep(2)

        if self.wait_check_answer_card_page():
            self.exam_process_exit_icon().click()
            time.sleep(2)
            self.entry.alert_tip_operate()
        return answer_info, exam_answer

    @teststep
    def check_exit_bank_operate(self, answer_info):
        """检测继续考试，之前选的内容是否被选择或者答案是否发生变化"""
        time.sleep(3)
        if self.wait_check_answer_card_page():
            answered_bank = list(answer_info.keys())
            time.sleep(2)
            for x in answered_bank:
                if self.wait_check_answer_card_page():
                    index = int(x) - 1
                    print(index)
                    if 'filled' not in self.number()[index].get_attribute('class'):
                        print('★★★ 已选选项的图标显示未选择')
                    self.number()[index].click()
                    time.sleep(2)
                    if self.container() == 'dx-container':
                        mine_answer = answer_info[x]
                        if 'activate' not in self.get_char_status_by_opt_text(mine_answer):
                            print('★★★ 题目页面已选的选项显示未被选择')

                    elif self.container() == 'bq-container':
                        blank_context = [x.text for x in self.blank_input()]
                        if blank_context != answer_info[x]:
                            print('★★★ 题目的填写内容与已填内容不一致！', blank_context, answer_info[x])
                        for i in self.blank_input():
                            i.click()
                            for j in i.text:
                                i.send_keys(Keys.BACKSPACE)
                            time.sleep(0.5)

                    self.result_icon().click()
                    time.sleep(2)

    @teststeps
    def exam_process_operate(self, exam_answer, wrong_index, wrong_note, choice_record, test_count=1):
        """
            章考核过程
            :param exam_answer: 试卷答案
            :param choice_record: 试卷选择选项记录
            :param test_count: 试卷做题次数
            :param wrong_index 查看得分，若得分为0(-), 即为[], 否则为随机错两个,定位[2,5]
            :param wrong_note  错题记录
        """
        index = 0
        mine_answer = {}
        choice_answer = exam_answer['选择']
        blank_answer = exam_answer["填空"]
        total = len(blank_answer) + len(choice_answer)

        if test_count == 2:
            time.sleep(2)
            print(self.tip_content())
            self.start_exam().click()

        elif test_count == 1:
            self.number()[0].click()
            time.sleep(2)
            print(self.reform_json(choice_answer))
            print(self.reform_json(blank_answer))

        while True:
            if self.container() in ['bq-container', 'dx-container']:
                container_attr = self.container()
                print("第" + str(index + 1) + "题:")

                if index == 0:                                      # 判断第一题时，上一题图标是否置灰
                    if 'disabled' not in self.pre_icon().get_attribute("class"):
                        print('★★★ 上一题图标未置灰')
                else:
                    if 'disabled' in self.pre_icon().get_attribute("class"):
                        print('★★★ 非第一题，上一题图标置灰！')

                    if index == total - 1:                            # 判断最后一题时， 下一题图标是否置灰
                        if 'disabled' not in self.next_icon().get_attribute("class"):
                            print('★★★ 已是最后一题，下一题图标未置灰')

                # 单选内容操作
                if container_attr == 'dx-container':
                    question = self.choose_question()
                    right_answer = choice_answer[question].replace('     ', ' ')
                    print('问题：', question)
                    print('正确答案：', right_answer)
                    page_answers = self.choice_options()

                    # 第一次做题存储所有选项顺序， 第二次时直接与第一次的存储进行比对
                    if test_count == 1:
                        choice_record[question] = [x.text for x in page_answers]
                    else:
                        print("页面顺序：", [x.text for x in page_answers])
                        print("上一次考试顺序：", choice_record[question])
                        if choice_record[question] == [x.text for x in page_answers]:
                            print('★★★ 选项顺序未发生改变')

                    #  做题分为两种， 一种是否需要做错， 另一种是全部做对
                    begin_length = len(list(mine_answer.keys()))
                    for x in page_answers:
                        if index in wrong_index:
                            wrong_note[self.get_question_id()] = right_answer
                            if x.text != right_answer:
                                x.click()
                                mine_answer[question] = x.text
                                break
                        else:
                            if x.text == right_answer:
                                x.click()
                                mine_answer[question] = x.text
                    after_length = len(list(mine_answer.keys()))
                    if begin_length == after_length:
                        print('★★★ 本题未选择！')
                    self.next_icon().click()
                    time.sleep(1)

                # 填空题操作
                elif container_attr == 'bq-container':
                    if test_count != 1:                               # 若不是第一次考试，直接退出考试
                        self.exam_process_exit_icon().click()
                        self.entry.alert_tip_operate()
                        time.sleep(2)
                        break

                    blank_text = self.blank_question_span()
                    print('题干：', blank_text)
                    try:
                        right_answer = blank_answer[blank_text]
                        print('正确答案：', right_answer)
                        input_wraps = self.blank_input()
                        mine_input = []
                        for i in range(len(input_wraps)):
                            input_wraps[i].click()
                            if index in wrong_index:                       # 若为错误顺序内，输入乱序字母
                                wrong_note[self.get_question_id()] = right_answer
                                input_wraps[i].send_keys('mkasmd' + Keys.ENTER)
                                mine_input.append('mkasmd')
                            else:                                           # 输入正确答案，输入内容改为小写
                                input_wraps[i].send_keys(right_answer[i].lower() + Keys.ENTER)
                                mine_input.append(right_answer[i].lower())
                            time.sleep(1)
                        mine_answer[blank_text] = mine_input
                        time.sleep(2)
                    except:
                        mine_answer[blank_text] = ' '
                        self.next_icon().click()
                        time.sleep(1)

            index += 1
            print('-' * 20, '\n')
            if total == index:
                self.result_icon().click()
                time.sleep(2)
                not_complete_bank = [x.text for x in self.number() if 'filled' not in x.get_attribute('class')]
                if len(not_complete_bank) != 0:
                    print('★★★ 存在题已做但状态显示未完成的题', not_complete_bank)
                time.sleep(1)
                break

        # 交卷后分数校验操作
        if self.wait_check_answer_card_page():
            print('交卷')
            self.finish_up_button().click()
            time.sleep(1)
            if self.wait_check_submit_tip_page():
                print(self.tip_content())
                self.confirm_btn().click()
                time.sleep(1)
                if self.wait_check_exam_result_page():
                    print('\n--- 页面分数校验 ---\n')
                    print('分数：', self.exam_score())
                    print(self.result_tag())
                    right_banks = [x.text for x in self.result_number() if 'success' in x.get_attribute('class')]   # 获取正确题目的个数
                    compute_score = int(round(100 / len(self.result_number()) * len(right_banks)))                  # 计算得分
                    page_score = int(self.exam_score())     # 页面分数
                    if compute_score != page_score:         # 计算分数与页面分数比较
                        print('★★★ 页面分数与计算分数不一致！', compute_score, page_score)
                    time.sleep(2)
                    self.exam_result_exit_icon().click()
                    time.sleep(2)
                print('----------------------')

        return mine_answer

