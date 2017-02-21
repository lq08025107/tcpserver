import pymssql

class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host = self.host, user = self.user, password = self.pwd, database = self.db, charset = "utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "数据库连接失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

def main():
    ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
    resList = ms.ExecQuery("SELECT id,weibocontent FROM WeiBo")
    for (id,weibocontent) in resList:
        print str(weibocontent).decode("utf8")

if __name__ =='__main__':
    main()