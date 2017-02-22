import pymssql

class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError, "no such database")
        self.conn = pymssql.connect(host = self.host, user = self.user, password = self.pwd, database = self.db, charset = "utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "failed when connecting db")
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
    ms = MSSQL("10.25.18.9","sa","p@ssw0rd","IVAS")
    resList = ms.ExecQuery("SELECT * FROM PUser")
    for (id,uname,upassword,name) in resList:
        print str(id) + uname + upassword + name
if __name__ =='__main__':
    main()