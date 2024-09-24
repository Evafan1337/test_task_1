import unittest
import psycopg2
from psycopg2 import sql

from basic import BasicTemplate
from utils import Utils

class TestDatabase(BasicTemplate):

    table_name = "people2"
    # Создание базы данных
    def testCreateDatabasePeople2(self):
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS public.people2 (
                        id SERIAL PRIMARY KEY,  
                        firstname VARCHAR(255) NOT NULL,
                        familyname VARCHAR(255) NOT NULL,         
                        dateofbirth DATE NOT NULL,
                        occupation VARCHAR(255),
                        hobby VARCHAR(255)
                    )
                ''')

    # people2 test
    def testRenameTable(self):

        # Определение ожидаемого и фактического результатов
        # В будущем это можно параметризовать
        original_table_name = "people2"
        new_table_name = "people2edit"

        # Выполнение переименования таблицы
        Utils.rename_table(self.cursor, original_table_name, new_table_name)

        # Проверка существует ли в БД таблица с оригинальным названием ОР: False
        # Проверка существует ли в БД таблица с измененным названием ОР: True
        # print("original_table_exists:", Utils.check_for_exist_table(self.cursor, original_table_name))
        # print("renamed_table_exists:", Utils.check_for_exist_table(self.cursor, new_table_name))

        self.assertFalse(Utils.check_for_exist_table(self.cursor, original_table_name))
        self.assertTrue(Utils.check_for_exist_table(self.cursor, new_table_name))

        # Восстановление состояния таблицы
        # т.н teardown
        Utils.rename_table(self.cursor, new_table_name, original_table_name)



    def testRenameInvalidName(self):

        test_cases = ["test_table_name","SELECT"]

        for elem in test_cases:
            with self.subTest("Testing parametrized addition"):
                Utils.create_empty_table(self.cursor, elem)

                expected = "people2"

                with self.assertRaises(psycopg2.errors.DuplicateTable):
                    Utils.rename_table(self.cursor, expected, elem)

                self.assertTrue(Utils.check_for_exist_table(self.cursor, expected))

                # Teardown
                Utils.drop_table(self.cursor, elem)


    def testRenameField(self):
        original_name = "firstname"
        expected = "firstname_edit"

        Utils.rename_column(self.cursor, "people2", original_name, expected)
        self.assertTrue(Utils.check_for_column_exist(self.cursor, "people2", expected))

        # Teardown
        Utils.rename_column(self.cursor, "people2", expected, original_name)


    def testRenameToExistField(self):
        original_name = "firstname"
        expected = "firstname"

        with self.assertRaises(psycopg2.errors.DuplicateColumn):
            Utils.rename_column(self.cursor, "people2", original_name, expected)

        # Utils.rename_column(self.cursor, "people2", original_name, expected)
        # self.assertTrue(Utils.check_for_column_exist(self.cursor, "people2", expected))

    def testChangeColumnType(self):
        column_name = "dateofbirth"
        original_type = "DATE"
        new_type = "TEXT"

        # Change the column type
        Utils.change_column_type(self.cursor, "people2", column_name, new_type)
        self.assertTrue(Utils.check_column_type(self.cursor, "people2", column_name, new_type))

        # Teardown
        Utils.change_column_type(self.cursor, "people2", column_name, original_type)
        self.assertTrue(Utils.check_column_type(self.cursor, "people2", column_name, original_type))

    def testChangeColumnTypeInvalid(self):
        column_name = "dateofbirth"
        invalid_type = "INVALID_TYPE"

        with self.assertRaises(psycopg2.errors.UndefinedObject):
            Utils.change_column_type(self.cursor, "people2", column_name, invalid_type)