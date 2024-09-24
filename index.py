import psycopg2

def test1(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM test_schema.papers')
    res = cursor.fetchall()
    cursor.close()
    print(res)


try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='12345678', host='localhost')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')

test1(conn)

l1 = [1,2,3,4,5,6]
print(l1[-1:0:-1])