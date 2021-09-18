# coding = utf-8
import re


class DoSentence:
    def del_punctuation(string):
        pattern = re.compile(r'[a-zA-Z0-9\u4e00-\u9fa5\s]')  # 查找数字、大小写字母、汉字
        result = pattern.findall(string)
        return "".join(result)

    def del_blank(string):
        pattern = re.compile(r'[^\s]')  # 查找数字、大小写字母、汉字
        result = pattern.findall(string)
        return "".join(result)

    def del_punctuation_blank(string):
        pattern = re.compile(r'[a-zA-Z0-9\u4e00-\u9fa5]')  # 查找数字、大小写字母、汉字
        result = pattern.findall(string)
        return "".join(result)

    def get_blank(string):
        index_list = [i.start() for i in re.finditer('\s', string)]
        return index_list

    def get_punctuation(string):
        pattern = re.compile(r'[^(a-zA-Z)^(0-9)^(\u4e00-\u9fa5)^\s]')
        result = pattern.findall(string)
        punctuation = "".join(result)
        # index_list = [i.start() for i in re.finditer(pattern, string)]
        return punctuation

    def remove_firstandlast_punctuation(string):  # 去除句首句尾标点规定符号
        punctuation = ',.()!?&";'
        if string[-1] in punctuation:
            string = string[:-1]
        if string[0] in punctuation:
            string = string[1:]
        return string

    def replace_punctuation(string):  # 替换规定的英中标点
        punctuation_en = ",.();!?[]:"
        punctuation_cn = "，。（）；！？〔〕："
        for i in range(len(punctuation_en)):
            string = string.replace(punctuation_en[i], punctuation_cn[i])
        return string


if __name__ == '__main__':
    string = ""
    ds = DoSentence.get_punctuation
    print(ds(string))
    a = 4
    b = 7





