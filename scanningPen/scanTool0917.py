# coding=utf-8
import serial
import time
import os
import pandas as pd
from dosentence import DoSentence

class Ser:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.read_timeout = 0.2
        self.write_timeout = 0.2
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.read_timeout)

    def open(self):
        if self.ser.is_open:
            raise Exception("Port  %s is open"%self.port)
        else:
            self.ser.open()

    def close(self):
        if self.ser.is_open:
            self.ser.close()
        else:
            raise Exception("Port  %s is closed" % self.port)

    def write(self, cmd):
        cmd += '\r\n'
        cmd = cmd.encode()
        self.ser.flushOutput()
        self.ser.flushInput()
        self.ser.write(cmd)
        time.sleep(0.2)

    def readall(self):
        return str(self.ser.readall(), encoding='utf-8')

    def get_result(self):
        while True:
            rec = self.ser.readline()
            # print(rec)
            rec = rec.decode()
            # print(rec)
            crash_list = ["Aborted", "Segmentation fault", "Illegal instruction"]  # crash关键字
            for i in crash_list:
                if rec.find(i) != -1:
                    return False
            n = rec.find("############################")
            if n != -1:
                return rec.replace("\r\n","")[29:]

    def get_settings(self):
        return self.ser.getSettingsDict()

    def check_str(self, string, str):
        return True if string.find(str) != -1 else False

    def check_outdir(self):
        self.write("ls -l /data/roobotest/out/")
        rec = self.readall()
        str = "total"
        return self.check_str(rec, str)   # 检测out目录若存在，返回True

    def delete_outdir(self):
        self.write("rm -rf /data/roobotest/out/")
        return True if self.check_outdir() is False else False

    def mkdir_outdir(self):
        self.write("mkdir -p /data/roobotest/out/")
        return True if self.check_outdir() is True else False

    def changeName_outdir(self, name):
        self.write("mv /data/roobotest/out/ /data/roobotest/{}/".format(name))
        self.write("ls -l /data/roobotest/{}/".format(name))
        rec = self.readall()
        str = "total"
        return self.check_str(rec, str)

    def clear_roobotest(self):
        self.write("rm -rf /data/roobotest/*")


def get_data(file_dir):
    files = os.listdir(file_dir)
    path = []
    if "data.xlsx" in files:
        df = pd.read_excel(file_dir+"/data.xlsx",index_col="name")
        for file in files:
            if file.endswith(".yuv"):
                if file not in df.index:
                    raise Exception("数据错误，文件%s在data.xlxs中不存在" % file)
                # path.append((file_dir + "/" + file).replace("//192.168.10.53/PCShared", "/mnt/nfs"))
                path.append(file)
        for index in df.index:
            if index not in path:
                raise Exception("数据错误，当前目录不存在%s文件" % index)
        return df
    else:
        raise Exception("文件目录不完整，缺少标注内容data.xlsx文件")


if __name__ == "__main__":
    print("测试开始："+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    port = "com11"
    baudrate = 115200
    ser = Ser(port, baudrate)
    ser.write("cd /data")
    ser.write("cd /data/spen")
    file_dir = r"//192.168.10.52/RooboShared/02.yuv_capture/02.picture/06.english_suite"
    # file_dir = r"//192.168.10.52/RooboShared/02.yuv_capture/02.picture/08.smoke_test/01JXW/stage_three"
    # file_dir = r"//192.168.10.52/RooboShared/10.customer_data/zuchuangwei_pic/alldata"
    # 04.colorful_background
    # 05.chinese_suite
    # 06.english_suite
    data = get_data(file_dir)
    num_pass = 0
    num_PassWithoutPunBlank = 0
    num_duozi = 0
    num_shaozi = 0
    num_punWrong = 0
    num_blankWrong = 0
    num_otherWrong = 0
    ser.clear_roobotest()
    print("数据\t原文\t识别结果\t测试結果\t多字\t少字\t标点错误\t空格错误\t错字及其他")
    for i in data.index:
        path = (file_dir + "/" + i).replace("//192.168.10.52/RooboShared", "/mnt/nfs2")
        # cmd = "./demo_styuv_pen " + path
        # cmd = "./hehe_demo_npu "+path
        cmd = "./hehe_demo_npu {} 1 1".format(path)
        ser.write(cmd)
        result = ser.get_result()
        orgin = data.loc[i]["value"]
        if result == False:
            print("{}\t{}\tcrash\tFail\tN\tN\tN\tN\tN".format(i,orgin))
        elif result == orgin:
            num_pass += 1
            print("{}\t{}\t{}\tPass\tN\tN\tN\tN\tN".format(i,orgin,result))
        else:
            ds = DoSentence
            del_punctuation_blank = ds.del_punctuation_blank
            get_blank = ds.get_blank
            get_punctuation = ds.get_punctuation
            result_str = ""
            duozi_str = ""
            shaozi_str = ""
            punctuation_str = ""
            blank_str = ""
            other_str = ""
            result_new = del_punctuation_blank(result)
            orgin_new = del_punctuation_blank(orgin)
            result_len = len(result_new)
            orgin_len = len(orgin_new)
            if result_new == orgin_new:
                result_str = "PassWithoutPuncation&blank"
                other_str = "N"
                num_PassWithoutPunBlank += 1
            else:
                result_str = "Fail"
                other_str = "Y" if result_len == orgin_len else "N"
            duozi_str = "Y" if result_len > orgin_len else "N"
            shaozi_str = "Y" if result_len < orgin_len else "N"
            punctuation_str ="Y" if get_punctuation(result) != get_punctuation(orgin) else "N"
            blank_str = "Y" if get_blank(result) != get_blank(orgin) else "N"
            # other_str = "Y" if duozi_str=="N" and shaozi_str=="N" and punctuation_str=="N" and blank_str=="N" else "N"
            function = lambda x,y: y+1 if x == 'Y' else y
            num_duozi = function(duozi_str,num_duozi)
            num_shaozi = function(shaozi_str,num_shaozi)
            num_punWrong = function(punctuation_str,num_punWrong)
            num_blankWrong = function(blank_str,num_blankWrong)
            num_otherWrong = function(other_str,num_otherWrong)
            print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format
                  (i, orgin, result, result_str, duozi_str, shaozi_str, punctuation_str, blank_str,other_str))
        time.sleep(1)
    sum = len(data.index)
    print("总共测试{}条,正确:{}条，整体识别率:{}".format(sum, num_pass, num_pass/sum))
    print("去除标点符号空格，新增正确:{}条。去除标点和空白识别率：{}".format(num_PassWithoutPunBlank,(num_PassWithoutPunBlank+num_pass)/sum))
    print("统计多字: {}条。多字率：{}".format(num_duozi,num_duozi/sum))
    print("统计少字：{}条，少字率:{}".format(num_shaozi,num_shaozi/sum))
    print("统计标点错误：{}条，标点错误率:{}".format(num_punWrong,num_punWrong/sum))
    print("统计空格错误：{}条，空格错误率:{}".format(num_blankWrong,num_blankWrong/sum))
    print("错字及其他：{}条，错误率:{}".format(num_otherWrong,num_otherWrong/sum))
    print("测试结束："+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
