import unittest
import psycopg2


DB_NAME = 'postgres'
USER = 'postgres'
PASSWORD = '12345678'
HOST = 'localhost'

class BasicTemplate(unittest.TestCase):
    conn = None
    table_name = None

    @classmethod
    def setUpClass(self):
        print("set_up")
        # Подключение к БД
        try:
            # пытаемся подключиться к базе данных
            self.conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except:
            # в случае сбоя подключения будет выведено сообщение в STDOUT
            print('Can`t establish connection to database')

    @classmethod
    def tearDownClass(self):
        print("tearDown")
        # Закрываем соединение с БД после всех тестов
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")