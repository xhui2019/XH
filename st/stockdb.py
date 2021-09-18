import sqlite3


class Stdb:
    def __init__(self,dbName):
        self._conn = sqlite3.connect(dbName)
        self._cur = self._conn.cursor()
        self._time_now = "[" + sqlite3.datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]"

    def close_con(self):
        self._cur.close()
        self._conn.close()

    def excute_sql(self, sql):
        """
        创建表初始化
        :param sql: 建表语句
        :return: True is ok
        """
        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[CREATE ERROR]", e)
            return False

    def drop_table(self, table_name):
        """
        删除表
        :param table_name: 表名
        :return:
        """
        try:
            self._cur.execute('DROP TABLE {0}'.format(table_name))
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[DROP TABLE ERROR]", e)
            return False

    def delete_table(self, sql):
        """
        删除表记录
        :param sql:
        :return: True or False
        """
        try:
            if 'DELETE' in sql.upper():
                self._cur.execute(sql)
                self._conn.commit()
                return True
            else:
                print(self._time_now, "[EXECUTE SQL IS NOT DELETE]")
                return False
        except Exception as e:
            print(self._time_now, "[DELETE TABLE ERROR]", e)
            return False

    def fetchall_table(self, sql, limit_flag=True):
        """
        查询所有数据
        :param sql:
        :param limit_flag: 查询条数选择，False 查询一条，True 全部查询
        :return:
        """
        try:
            self._cur.execute(sql)
            war_msg = self._time_now + ' The [{}] is empty or equal None!'.format(sql)
            if limit_flag is True:
                r = self._cur.fetchall()
                return r if len(r) > 0 else war_msg
            elif limit_flag is False:
                r = self._cur.fetchone()
                return r if len(r) > 0 else war_msg
        except Exception as e:
            print(self._time_now, "[SELECT TABLE ERROR]", e)

    def insert_update_table(self, sql):
        """
        插入/更新表记录
        :param sql:
        :return:
        """
        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[INSERT/UPDATE TABLE ERROR]", e)
            return False

    def insert_table_many(self, sql, value):
        """
        插入多条记录
        :param sql:
        :param value: list:[(),()]
        :return:
        """
        try:
            self._cur.executemany(sql, value)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[INSERT MANY TABLE ERROR]", e)
            return False


class conTest:
    """测试类"""

    def __init__(self, file):
        self.con = sqlite3.connect(file)
        self.cur = self.con.cursor()

    def create_table_test(self, bm):
        sql = '''CREATE TABLE `mytest2` (
                  `id` DATETIME DEFAULT NULL,
                  `user` VARCHAR(12) DEFAULT NULL,
                  `name` VARCHAR(12) DEFAULT NULL,
                  `number` VARCHAR(12) DEFAULT NULL
                )'''
        sql1 = f'PRAGMA table_info ({bm})'
        print(sql1)
        self.cur.execute(sql1)
        self.con.commit()
        value2 = self.cur.fetchall()
        print(value2)
        print(1111)
        if len(value2) == 0:
            try:
                print(self.cur.execute(sql))
                self.con.commit()
                value3 = self.cur.fetchone()
                print(value3)
            except:
                print("建立表出错")
        else:
            print("表已经存在")

    def drop_table_test(self):
        sql1 = "delete from mytest"
        self.cur.execute((sql1))
        self.con.commit()
        # print(self.con.drop_table("mytest"))

    def fetchall_table_test(self):
        sql = "SELECT * from mytest WHERE user='1003';"
        sql_all = "SELECT * from mytest;"
        print("全部记录", self.cur.execute(sql_all))
        print("全部记录", self.cur.fetchall())
        print("单条记录", self.cur.execute(sql))
        print("条件查询", self.cur.execute(sql))

    def delete_table_test(self):
        sql = "DELETE FROM mytest WHERE user='1003';"
        self.con.delete_table(sql)

    def update_table_test(self):
        sql_update = "UPDATE mytest SET id={0},user={1},name={2},number={3} WHERE number={4}".format(1, 1002, "'王五'",
                                                                                                     1002, 1002)
        self.cur.execute(sql_update)
        self.con.commit()

        # print(self.con.insert_update_table(sql_update))

    def insert_table_test_one(self):
        sql = """INSERT INTO mytest VALUES (3, 1003, "王五", 1003);"""
        self.cur.execute((sql))
        self.con.commit()

    def insert_table_test_many(self):
        sql = """INSERT INTO mytest VALUES (?,?,?,?) """
        value = [(2, 1004, "赵六", 1004), (4, 1005, "吴七", 1005)]
        for i in value:
            self.cur.execute(sql, i)
            self.con.commit()


    def close_con(self):
        self.con.close()


if __name__ == "__main__":
    file = "d:/test.db"
    sql = '''CREATE TABLE STOCK (
                      CODE TEXT PRIMARY KEY NOT NULL,
                      NAME TEXT NOT NULL,
                      MARKET TEXT,
                      TOTAL_MV TEXT,
                      CIRC_MV TEXT,
                      PE TEXT,
                      VAR TEXT
                    )'''
    t = Stdb(file)
    t.create_table(sql)
    # contest.insert_table_test_many()
    # contest.fetchall_table_test()
    # contest.insert_table_test_one()
    # contest.fetchall_table_test()
    # contest.update_table_test()
    # contest.drop_table_test()
    # contest.close_con()
