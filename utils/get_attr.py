# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/1/17 16:29
# -------------------------------------------
from conf.decorator import teststep


class GetAttribute:

    @teststep
    def judge_ele_has_select(self, ele):
        """判断属性是否具有selected属性"""
        try:
            ele.get_attribute('selected')
            return True
        except:
            return False

    @teststep
    def get_class(self, ele):
        return ele.get_attribute('class')