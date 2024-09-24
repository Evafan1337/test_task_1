import unittest
import psycopg2
from basic import BasicTemplate
from utils import Utils

class TestDatabase(BasicTemplate):

    table_name = "people"
    # Создание базы данных
    # Параметризовать обе БД?
    def testCreateDatabasePeople(self):
        print("testCreateDatabase")
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS public.People (
                        id SERIAL PRIMARY KEY,  
                        Name VARCHAR(255) NOT NULL,         
                        DateOfBirth DATE NOT NULL           
                    )
                ''')
        self.conn.commit()
        # Как проверить?

    # TO-DO:Можно параметризовать тесты
    # TEST single_row
    # Первичное полное добавление данных
    def test_solo_insert_empty_table(self):
        Utils.make_solo_insert_people(self.cursor, "1_John Doe", "1990-05-15")

    def test_correct_data_insert(self):

        test_cases = [
            ('John Doe', '1990-05-15'),
            ('John Doe2','1992-05-14'),
            ('Michael Max', '1993-02-10,')
        ]

        for test_case_elem in test_cases:
            name, date = test_case_elem
            with self.subTest("Testing parametrized addition"):
                #TO-DO: reformat string
                #TO-DO: use new

                request_str = Utils.prepare_request_insert(name, date)
                self.cursor.execute(request_str)
                self.conn.commit()

    def test_data_select(self):
        Utils.select_from_table_by_id(self.cursor, "people", 1)

    def test_data_select_with_like(self):
        Utils.select_from_table_by_column_letter(self.cursor, "people", "name", "J")

    def test_data_update(self):
        Utils.update_row(self.cursor, "people", "name", 1)

    # Негативные тесты можно параметризовать
    def test_data_update_invalid_id(self):
        target_id = 999999
        Utils.update_row(self.cursor, "people", "name", target_id)

        self.cursor.execute("SELECT name FROM people WHERE id = 99999")
        result = Utils.select_from_table_by_id(self.cursor, "people", target_id)
        self.assertIsNone(result, "Обновление должно было не изменять запись для несуществующего id")

    def test_data_update_invalid_collumn(self):
        with self.assertRaises(psycopg2.errors.UndefinedColumn):
            Utils.update_row(self.cursor, "people", "invalid_column", 1)

    def test_data_update_invalid_table(self):
        with self.assertRaises(psycopg2.errors.UndefinedTable):
            # Попробуем обновить данные в несуществующей таблице 'invalid_table'
            Utils.update_row(self.cursor, "invalid_table", "name", 1)

    def test_data_delete(self):

        name, date = ('Name To Delete', '1990-05-14')
        Utils.make_solo_insert_people(self.cursor, name, date)

        res = Utils.select_last_row(self.cursor, "people")
        Utils.delete_last_item(self.cursor,"people")

        res2 = Utils.select_last_row(self.cursor, "people")

        self.assertFalse(res[1] == res2[1])

