#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/11/4 16:32
# -----------------------------------------
from conf.base_page import BasePage
from conf.decorator import teststep


class EleAttrCheck(BasePage):

    @teststep
    def check_ele_is_enabled(self, ele):
        if 'disable' in ele.get_attribute('class'):
            return False
        else:
            return True

    @teststep
    def check_word_is_in_class(self, value, ele):
        if value in ele.get_attribute('class'):
            return True
        else:
            return False