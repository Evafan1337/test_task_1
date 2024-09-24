import psycopg2
from psycopg2 import sql

class Utils():

    @staticmethod
    def rename_column(db_obj:psycopg2.extensions.cursor, table_name:str, old_name:str, new_name:str):

        sql_rqst = f"ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}"
        print("sql_rqst:", sql_rqst)

        db_obj.execute(
            sql_rqst
            # sql.SQL("ALTER TABLE {} RENAME COLUMN {} TO {}").format(
            #     sql.Identifier(table_name),
            #     sql.Identifier(old_name),
            #     sql.Identifier(new_name)
            # )
        )

    @staticmethod
    def check_for_column_exist(db_obj:psycopg2.extensions.cursor, table_name:str, column_name:str):

        sql_rqst = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name='{column_name}'"
        print(sql_rqst)

        db_obj.execute(sql_rqst
            # sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name= {} AND column_name= {}").format(
            #     sql.Identifier(table_name),
            #     sql.Identifier(old_name),
            # )
        )

        res = db_obj.fetchone()
        print("res:", res)
        print("t-f:", bool(res))

        return bool(res)

    @staticmethod
    def create_empty_table(db_obj:psycopg2.extensions.cursor, table_name:str):
        db_obj.execute(
            sql.SQL("CREATE TABLE IF NOT EXISTS {} (id SERIAL PRIMARY KEY)").format(
                sql.Identifier(table_name),
            )
        )

    @staticmethod
    def drop_table(db_obj:psycopg2.extensions.cursor, table_name:str):
        db_obj.execute(
            sql.SQL("DROP TABLE IF EXISTS {}").format(
                sql.Identifier(table_name),
            )
        )

    @staticmethod
    def prepare_request_insert(name: str, birth: str) -> str:
        return f'''
                INSERT INTO People (Name, DateOfBirth)
                VALUES ('{name}', '{birth}');
                '''

    #TO-DO: Можно придти к одной параметризованной функции. Проработать вводимые типы
    @staticmethod
    def make_solo_insert_people(db_obj:psycopg2.extensions.cursor, name:str, date:str):
        db_obj.execute(
            sql.SQL("INSERT INTO People (Name, DateOfBirth) VALUES({}, {})").format(
                sql.Literal(name),
                sql.Literal(date)
            )
        )

    @staticmethod
    def rename_table(db_obj:psycopg2.extensions.cursor, old_table_name:str, new_table_name:str):
        db_obj.execute(
            sql.SQL("ALTER TABLE {} RENAME TO {}").format(
                sql.Identifier(old_table_name),
                sql.Identifier(new_table_name)
            )
        )

    @staticmethod
    def check_for_exist_table(db_obj:psycopg2.extensions.cursor, original_table_name:str) -> bool:
        db_obj.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    )
                """, (original_table_name,))
        table_exists_flag = db_obj.fetchone()[0]
        return table_exists_flag


    @staticmethod
    def select_from_table_by_id(db_obj:psycopg2.extensions.cursor, table_name:str, id:int):
        db_obj.execute(
            sql.SQL("SELECT * FROM {} WHERE id = {}").format(sql.Identifier(table_name), sql.Literal(str(id)))
        )
        result = db_obj.fetchone()
        print("res1:", result)
        return result

    # Вывод всех записей значение целевого столбца column_name начинается с символа target из таблицы table_name
    @staticmethod
    def select_from_table_by_column_letter(db_obj:psycopg2.extensions.cursor, table_name:str, column_name:str, target:str):

        target = f"{target}%"

        # res_sql = sql.SQL("SELECT * FROM {} WHERE {} LIKE {}").format(sql.Identifier(table_name), sql.Identifier(column_name), sql.Literal(target))
        # res_sql = res_sql.as_string(db_obj)
        # print("db:", res_sql)

        db_obj.execute(
            sql.SQL("SELECT * FROM {} WHERE {} LIKE {}").format(sql.Identifier(table_name), sql.Identifier(column_name), sql.Literal(target))
        )
        result = db_obj.fetchone()
        return result
        print("res2:", result)

    @staticmethod
    def select_last_row(db_obj:psycopg2.extensions.cursor, table_name:str):
        db_obj.execute(
            sql.SQL("SELECT * FROM {} ORDER BY id DESC LIMIT 1").format(sql.Identifier(table_name))
        )
        result = db_obj.fetchone()
        return result


    @staticmethod
    def update_row(db_obj:psycopg2.extensions.cursor, table_name:str, col_name:str, id:int):

        db_obj.execute(
            sql.SQL("UPDATE {} SET {} = 'edit_1' WHERE id = {}").format(
                sql.Identifier(table_name),
                sql.Identifier(col_name),
                sql.Literal(id)
            )
        )


    @staticmethod
    def delete_last_item(db_obj:psycopg2.extensions.cursor, table_name:str):
        db_obj.execute(
            sql.SQL("DELETE FROM {} WHERE id = (SELECT id FROM {} ORDER BY id DESC LIMIT 1)").format(
                sql.Identifier(table_name),
                sql.Identifier(table_name)
            )
        )

    @staticmethod
    def change_column_type(db_obj: psycopg2.extensions.cursor, table_name: str, column_name: str, new_type: str):
        sql_rqst = sql.SQL("ALTER TABLE {table} ALTER COLUMN {col} TYPE {type}").format(
            table=sql.Identifier(table_name),
            col=sql.Identifier(column_name),
            type=sql.SQL(new_type)
        )
        db_obj.execute(sql_rqst)

    @staticmethod
    def check_column_type(db_obj: psycopg2.extensions.cursor, table_name: str, column_name: str, expected_type: str) -> bool:
        query = sql.SQL("""
            SELECT data_type
            FROM information_schema.columns
            WHERE table_name = {table} AND column_name = {col}
        """).format(
            table=sql.Literal(table_name),
            col=sql.Literal(column_name)
        )
        db_obj.execute(query)
        result = db_obj.fetchone()
        return result and result[0] == expected_type
