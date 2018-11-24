import yaml
from mysql import connector

class DatabaseManager:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        self.config = yaml.load(open('config_database.yaml', 'r'))

    def connect(self):
        self.conn = connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            passwd=self.config['passwd'],
            database=self.config['database'],
            auth_plugin=self.config['auth_plugin']
        )
        self.cursor = self.conn.cursor()
    
    def foo(self):
        self.connect()
        self.cursor.execute("SELECT * FROM MESSAGE_LOG")
        print(self.cursor.fetchall())

if __name__ == '__main__':
    dbm = DatabaseManager()
    dbm.foo()