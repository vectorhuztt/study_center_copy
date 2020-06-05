import json
import re
from app.common_ele.common_page import CommonElePage
from conf.decorator import teststep


class PassionHomePage(CommonElePage):

    @teststep
    def chapter_study(self):
        """章节目录"""
        ele = self.driver.find_element_by_css_selector(".box .icon-study")
        return ele

    @teststep
    def error_book(self):
        """错题本"""
        ele = self.driver.find_element_by_css_selector(".box .icon-file-wrong")
        return ele

    @teststep
    def exam(self):
        """真题模考"""
        ele = self.driver.find_element_by_css_selector(".box .icon-exam")
        return ele

    @teststep
    def chapter_total_num(self):
        """章节总个数"""
        ele = self.driver.find_element_by_css_selector('.box .box-wrap:nth-child(1) .progress')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def finish_chapter(self):
        """已完成的章学习"""
        ele = self.driver.find_element_by_css_selector('.box .el-button:nth-child(1)')
        return ele

    @teststep
    def error_num(self):
        """错题个数"""
        ele = self.driver.find_element_by_css_selector('.box .box-wrap:nth-child(2) .progress')
        return int(ele.text)

    @teststep
    def study_counter(self):
        """学习统计按钮"""
        ele = self.driver.find_element_by_css_selector('.box .el-button:nth-child(2)')
        return ele

    @teststep
    def finish_exam_num(self):
        """试卷完成个数"""
        ele = self.driver.find_element_by_css_selector('.box .box-wrap:nth-child(3) .progress')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def exam_record(self):
        """考试记录"""
        ele = self.driver.find_element_by_css_selector('.box .el-button:nth-child(3)')
        return ele

    @teststep
    def book_id(self):
        """书籍id"""
        url = self.driver.current_url
        return int(url.split('/')[-1])

    @teststep
    def write_data_to_file(self, file_name, write_type,  data):
        """将数据写入文件"""
        with open('app/passion/test_data/{}'.format(file_name), write_type) as f:
            json.dump(data, f, ensure_ascii=False)

    @teststep
    def read_data_from_file(self, file_name):
        """从文件中读取数据"""
        with open('app/passion/test_data/{}'.format(file_name), 'r') as f:
            return json.loads(f.read())




