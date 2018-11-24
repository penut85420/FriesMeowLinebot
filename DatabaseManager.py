import yaml
from datetime import datetime as dt
from mysql import connector

class DatabaseManager:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        self.config = yaml.load(open('config_database.yaml', 'r'))

    # Common Database Operation

    def connect(self):
        self.conn = connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            passwd=self.config['passwd'],
            database=self.config['database'],
            auth_plugin=self.config['auth_plugin']
        )
        self.cursor = self.conn.cursor(buffered=True)
    
    def execute(self, sql, val):
        self.connect()
        self.cursor.execute(sql, val)
        self.conn.commit()

    # Message Log Operation

    def insert_msg_log(self, arg):
        sql = "INSERT INTO MESSAGE_LOG (msg_date, user_uid, msg_receive, msg_send) VALUES (%s, %s, %s, %s)"
        self.execute(sql, arg)
    
    def get_lastest_tarot(self, arg):
        sql = "SELECT msg_send FROM MESSAGE_LOG WHERE user_uid = %s ORDER BY msg_date DESC"
        self.execute(sql, arg)
        f = self.cursor.fetchall()
        rtn_list = list()
        for i in f:
            if "[Tarot Img]" in i[0]:
                for j in i[0][2:-2].split("', '"):
                    rtn_list.append(j[len("[Tarot Img]"):])
                break
        return rtn_list
    # User Table Operation

    def update_user_state(self, uid, state):
        if not self.is_user_exist(uid):
            self.insert_new_user(uid)
        sql = "UPDATE user_table SET user_state=%s WHERE user_uid=%s"
        val = [state, uid]
        self.execute(sql, val)

    def insert_new_user(self, uid):
        sql = "INSERT INTO USER_TABLE (user_uid, user_state) VALUES (%s, %s)"
        val = [uid, "INIT"]
        self.execute(sql, val)
    
    def is_user_exist(self, uid):
        sql = "SELECT * FROM USER_TABLE WHERE user_uid=%s"
        val = [uid]
        self.execute(sql, val)
        return len(self.cursor.fetchall()) > 0

    def foo(self):
        self.connect()
        self.cursor.execute("SELECT * FROM MESSAGE_LOG")
        print(self.cursor.fetchall())

if __name__ == '__main__':
    dbm = DatabaseManager()
    # msg_date = dt.now()
    # uid = "@@##TESTING##@@"
    # receive = "嗨"
    # send = "你好啊喵"

    # dbm.update_user_state("@@##UNKNOWN##@@", "HELLO")
    # print(dbm.is_user_exist("@@##UNKNOWN##@@"))
    # dbm.insert_msg_log([msg_date, uid, receive, send])
    for i in dbm.get_lastest_tarot(["U3c70a0e93aaa36c5643ab480f7f1a023"]):
        print(i)