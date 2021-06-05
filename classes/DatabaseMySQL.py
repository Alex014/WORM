from interfaces.idatabase import idatabase
from classes.Storage import Storage
import pymysql.cursors


class DatabaseMySQL(idatabase):

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = int(port)
        self.login = user
        self.password = password
        self.database = database

    def check(self):
        try:
            connection = pymysql.connect(host=self.host,
                                         user=self.login,
                                         port= self.port,
                                         password= self.password,
                                         database=self.database,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
        except Exception:
            print('No connection to DATABASE MySQL')
            return False

        return connection

    def last_insert_id(self, table: str):
        with Storage.connection.cursor() as cursor:
            sql = "SELECT LAST_INSERT_ID() AS id FROM `"+table+"`"
            cursor.execute(sql)
            result = cursor.fetchone()

            if len(result) > 0:
                return result['id']
            else:
                return 0

    def get_by_field(self, table: str, field: str, value: str):
        with Storage.connection.cursor() as cursor:
            sql = "SELECT * FROM `"+table+"` WHERE `"+field+"`=%s"
            cursor.execute(sql, (value))
            return cursor.fetchone()
