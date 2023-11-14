import sqlite3
import Help


# Функционал БД
def insert_varible_into_table(id='', thing='', grade='', day='', lesson='',
                              name_of_the_database='bot.db', name_of_the_table=''):
    global sqlite_insert_with_param, data_tuple, sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(name_of_the_database)
        cursor = sqlite_connection.cursor()
        status = "Подключен к SQLite"
        if name_of_the_table == 'classes':
            sqlite_insert_with_param = 'INSERT INTO classes(id, thing) VALUES (?, ?);'
            data_tuple = (id, thing)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            status = 'classes'
            print(status)
        elif name_of_the_table == 'timesheet':
            sqlite_insert_with_param = 'INSERT INTO timesheet(class, day, lesson) VALUES (?, ?, ?);'
            data_tuple = (grade, day, lesson)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            status = 'timesheet'
            print(status)
        sqlite_connection.commit()
        status = "Переменные Python успешно вставлены в таблицу things"

    except sqlite3.Error as error:
        status = ("Ошибка при работе с S"
                  "QLite", error)
        print(status)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            status = "Соединение с SQLite закрыто"
            print(status)

def make_class():
    grades = ['7А', '7Б', "7В", "8А", "8Б", "8В", "8Г", "9А", "9Б", "9В", "9Г", "10А", "10Б", "10В", "10Г", "11А", "11Б"]
    for grade in grades:
        for day in range(6):
            for i in range(1, 10):
                insert_varible_into_table(grade=grade, day=str(day), lesson=str(i), name_of_the_table='timesheet')


def make_timesheet():
    lessons = []
    for i in Help.timesheet:
        for k in i:
            lessons.append(k)

    for i in lessons:
        lesson1 = 'UPDATE timesheet set thing = (SELECT id FROM classes id WHERE thing = ?)\
        WHERE lesson = ?'
        data = (i, lessons.index(i))
        cur.execute(lesson1, data)


# Инициализация базы данных
database = sqlite3.connect('bot.db')
classes = 'CREATE TABLE IF NOT EXISTS classes(id TEXT PRIMARY KEY, thing TEXT)'
timesheet = ('CREATE TABLE IF NOT EXISTS timesheet(id INTEGER PRIMARY KEY, class TEXT, day TEXT, lesson TEXT, '
             'thing TEXT, cabinet INTEGER)')
cur = database.cursor()
cur.execute(timesheet)
cur.execute(classes)
for i in Help.translate.values():
    insert_varible_into_table(id=str(list(Help.translate.values()).index(i)), thing=i,  name_of_the_table='classes')
make_class()
make_timesheet()
tablee = cur.execute(timesheet)

result0 = cur.execute("""SELECT * FROM timesheet""").fetchall()
result1 = cur.execute('''SELECT * FROM classes''').fetchall()
print(result0)
print(result1)
print(Help.timesheet)


