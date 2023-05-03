import sqlite3 as sq


def start_db(): # Эта функция просто подключает базу данных
    try:
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)
        cursor.close()

    except sq.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")


def create_table(zapros): # По сути эта функция особо и не нужна, все базы данных я создал заранее
    try:
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print("База успешно подключена к SQLite")

        create_table_query = zapros
        cursor.execute(create_table_query)
        sqlite_connection.commit()
        print("Таблица успешно создана")

        cursor.close()
    except sq.Error as error:
        print('Ошибка при подключении к SQLite :', error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")


def create_profile(table_name, *args):
    try:
        print('Create profile')
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print('База данных создана и успешно подключена к SQLite')
        val_str = ''
        for i in args:
            val_str += (f"'{str(i)}'" + " ,")
        val_str = val_str[:-1]
        sqlite_insert_query = f'''INSERT INTO {table_name} VALUES ({val_str})''' # Не уверен, что оно будет работать корректно
        cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу")

        cursor.close()
    except sq.Error as error:
        print("Ошибка при работе с SQLite/Create profile", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")


def read_table(table_name, user_id, item):
    try:
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = f"""SELECT {item} from {table_name} where user_id = {user_id}"""
        cursor.execute(sqlite_select_query)
        data = cursor.fetchone()

        cursor.close()
        return data

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")

def show_table(table_name, user_id):
    try:
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = f"""SELECT * from {table_name} where user_id = {user_id}"""
        cursor.execute(sqlite_select_query)
        data = cursor.fetchall()
        cursor.close()
        return data

    except sq.Error as error:
        print("Ошибка при работе с SQLite/show_table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")

def give_id(table_name):
    try:
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = f"""SELECT * from {table_name}"""
        cursor.execute(sqlite_select_query)
        data = len(cursor.fetchall())

        cursor.close()
        return data

    except sq.Error as error:
        print("Ошибка при работе с SQLite/read_table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")


def delete_record(table_name, id):
    try:
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = f"""DELETE from {table_name} where {table_name[:-1]}_id = {id}"""
        cursor.execute(sql_update_query)
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()
        sqlite_connection.commit()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")


def update_table(table_name, us_id, item, value):
    try:
        sqlite_connection = sq.connect('BotDataBase.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_update_query = f"""UPDATE {table_name} set {item} = {value} where user_id = {us_id}"""
        cursor.execute(sqlite_update_query)
        print("Изменения внесены успешно!")
        cursor.close()

        sqlite_connection.commit()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто\n")


