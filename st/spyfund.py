import tushare as ts
import datetime
import numpy as np
from st.stockdb import Stdb
import time

class St:
    def __init__(self):
        ts.set_token("ef4ac822493ed1068c996f1dfe26ab28f9f65de21e5c4a1e4d731029")
        self.pro = ts.pro_api()

    def get_all_stock(self):
        data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,market')
        zhuban = data[(data["name"].str.contains("ST")==False)&(data["market"]=="主板")]
        return zhuban

    def get_basics(self, code):
        res = self.pro.daily_basic(ts_code=code,limit=1,fields='close,pe,pe_ttm,pb,total_mv,circ_mv')
        return res

    def get_ma(self, code):
        res = ts.pro_bar(ts_code=code, limit=70, ma=[5, 10, 20, 30, 60])
        head = res.loc[0]
        return [head["ma5"],head["ma10"],head["ma20"],head["ma30"],head["ma60"]]

    def glue(self,list):
        res = []
        list = list[:-1]
        n = len(list)
        for i in range(n-1):
            for j in range(i+1,n):
                result = abs(list[i]/list[j]-1)
                res.append(result)
        aver = sum(res)/len(res)
        return aver


    def get_var(self,list):
        return np.var(list)

    def get_thirty_mins(self, code):
        res = ts.pro_bar(ts_code=code, limit=80, freq="30min",ma=[5])
        head = res
        return [head["ma5"]]

if __name__ == "__main__":
    def action():
        sql_file = "d:/test.db"
        st = St()
        db = Stdb(sql_file)
        sql_table = '''CREATE TABLE STOCK (
                          CODE TEXT PRIMARY KEY NOT NULL,
                          NAME TEXT NOT NULL,
                          MARKET TEXT,
                          CLOSE REAL,
                          TOTAL_MV REAL ,
                          CIRC_MV REAL,
                          PE REAL ,
                          PE_TTM REAL ,
                          VAR REAL
                        )'''
        db.excute_sql(sql_table)
        stocks = st.get_all_stock()
        print(stocks)
        for index, row in stocks.iterrows():
            code = row['ts_code']
            name = row['name']
            print("###########index:{},code:{},".format(index,code))
            market = row['market']
            data = st.get_basics(code)
            pe = data.loc[0]['pe']
            pe_ttm = data.loc[0]['pe_ttm']
            close = data.loc[0]['close']
            if pe=='nan':
                pe=0
            if pe_ttm=='nan':
                pe_ttm=0
            total_mv = data.loc[0]['total_mv']
            circ_mv = data.loc[0]['circ_mv']
            var = st.glue(st.get_ma(code))
            sql_temp = '''INSERT INTO STOCK (CODE,NAME,MARKET,CLOSE,TOTAL_MV,CIRC_MV,PE,PE_TTM,VAR)
            VALUES (?,?, ?,?, ?, ?,?,?,?);'''
            values = [(code,name,market,close,total_mv,circ_mv,pe,pe_ttm,var)]
            db.insert_table_many(sql_temp,values)
            # time.sleep(1)
    # action()
    st = St()
    data = st.get_thirty_mins("002340.SZ")
    # data = st.get_ma("002340.SZ")
    print(data)
    # print(data)
    # aver = st.glue(data)
    # print(aver)




