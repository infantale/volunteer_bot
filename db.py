import sqlite3


def init_db():
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    # Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS 'users'(id TEXT UNIQUE, tz TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS 'answers'
                                  (id text, number text, time text, text text, uid text)
                               """)
    conn.commit()


def read_data_in_answers(chatid):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    c = cursor.execute(f"""SELECT number,time,text FROM 'answers' WHERE id={chatid}""")
    result = ''.join(['| '.join(map(str, x)) for x in c])
    return result
