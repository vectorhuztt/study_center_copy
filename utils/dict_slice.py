#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/25 11:57
# -----------------------------------------
from conf.decorator import teststep


class DictSlice:

    @teststep
    def dict_slice(self, split_dict, start=None, end=None):
        keys = list(split_dict.keys())
        if start is None:
            start_index = 0
        else:
            start_index = start

        if end is None:
            end_index = len(keys)
        else:
            end_index = end

        dict_slice = {}
        for k in keys[start_index:end_index]:
            dict_slice[k] = split_dict[k]
        return dict_slice