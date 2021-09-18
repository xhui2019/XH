import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print(lg)
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

res = bs.query_history_k_data_plus("sz.000333",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2021-8-01', end_date='2021-8-26',
    frequency="d", adjustflag="3")

data_list = []
while (res.error_code == '0') & res.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(res.get_row_data())
result = pd.DataFrame(data_list, columns=res.fields)
print(result)