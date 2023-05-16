import sqlite3 as sq

class DB():
    def __init__(self):
        try:
            self.sqlite_connection = sq.connect('BotDataBase.db')
            self.cursor = self.sqlite_connection.cursor()
            print("База данных создана и успешно подключена к SQLite")

            sqlite_select_query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_query)
            record = self.cursor.fetchall()
            print("Версия базы данных SQLite: ", record)

        except sq.Error as error:
            print("Ошибка при подключении к sqlite :", error)

    def get_id(self, table_name):
        try:
            sqlite_select_query = f"""SELECT * from {table_name}"""
            self.cursor.execute(sqlite_select_query)
            data = len(self.cursor.fetchall())
            return data

        except sq.Error as error:
            print("Ошибка при работе с SQLite/read_table", error)

    def delete_record(self, table_name, id):
        try:
            sql_update_query = f"""DELETE from {table_name} where {table_name[:-1]}_id = {id}"""
            self.cursor.execute(sql_update_query)
            self.sqlite_connection.commit()
            print("Запись успешно удалена")

        except sq.Error as error:
            print("Ошибка при работе с SQLite", error)

    def update_table(self, table_name, us_id, item, value):
        try:
            sqlite_update_query = f"""UPDATE {table_name} set {item} = {value} where user_id = {us_id}"""
            self.cursor.execute(sqlite_update_query)
            self.sqlite_connection.commit()
            print("Изменения внесены успешно!")

        except sq.Error as error:
            print("Ошибка при работе с SQLite", error)

    def show_table(self, table_name, user_id):
        try:
            sqlite_select_query = f"""SELECT * from {table_name} where user_id = {user_id}"""
            self.cursor.execute(sqlite_select_query)
            data = self.cursor.fetchall()
            return data

        except sq.Error as error:
            print("Ошибка при работе с SQLite/show_table", error)

    def create_profile(self, table_name, *args):
        try:
            val_str = ''
            for i in args:
                val_str += (f"'{str(i)}'" + " ,")
            val_str = val_str[:-1]
            sqlite_insert_query = f'''INSERT INTO {table_name} VALUES ({val_str})'''  # Не уверен, что оно будет работать корректно
            self.cursor.execute(sqlite_insert_query)
            self.sqlite_connection.commit()
            print("Переменные Python успешно вставлены в таблицу")

        except sq.Error as error:
            print("Ошибка при работе с SQLite/Create profile", error)

    def read_table(self, table_name, user_id, item):
        try:
            sqlite_select_query = f"""SELECT {item} from {table_name} where user_id = {user_id}"""
            self.cursor.execute(sqlite_select_query)
            data = self.cursor.fetchone()
            return data

        except sq.Error as error:
            print("Ошибка при работе с SQLite", error)

