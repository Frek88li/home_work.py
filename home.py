import psycopg2

conn = psycopg2.connect(database="netology_home", user="postgres", password="Dj@mbyl14")

def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client(
    client_id SERIAL PRIMARY KEY,
    first_name varchar(40) NOT NULL,
    last_name varchar(40) NOT NULL,
    email varchar(50) UNIQUE,
    number varchar(10) []
    );
    """)

    conn.commit()
    print("Таблица создана")

def add_client(cursor, first_name, last_name, email, phone=None):
    cursor.execute("""INSERT INTO client(last_name, first_name, email, number)
    VALUES(%s, %s, %s, %s)
    """, ((first_name), (last_name), (email), (phone)))
    conn.commit()
    print(f"Клиент {first_name}, {last_name} добавлен.")

def add_phone(cursor, client_id, new_phone):
    cursor.execute("""
        SELECT number FROM client
        WHERE client_id = %s""", (client_id,))
    phone = cursor.fetchone()
    if phone[0] == None:
        cursor.execute("""
            UPDATE client
            SET number = %s
            WHERE client_id = %s
            """, ([new_phone], client_id))
    else:
        result = phone[0]
        result.append(new_phone)
        cursor.execute("""
            UPDATE client
            SET number = %s
            WHERE client_id = %s
            """, (result, client_id))
    conn.commit()
    print(f"Клиенту {client_id} добавлен номер {new_phone}")

def change_client(cursor, client_id, first_name=None, last_name=None, email=None, phones=None):
    my_dict = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'numbers': phones
    }
    for key, value in my_dict.items():
        if value:
            cursor.execute("""
            UPDATE client
            SET {} = %s
            WHERE client_id = %s
            """.format(key), (value, client_id))
            print(f'У клиента с номером {client_id} изменено поле {key} на {value}')
    conn.commit()


def delete_phone(cursor, client_id, phone):
    cursor.execute("""
    SELECT number
    FROM client
    WHERE client_id = %s""", (client_id,))
    numbers = cursor.fetchone()
    if not numbers[0] or phone not in numbers[0]:
        print(f'У клиента с номером {client_id} отсутствует указанный номер телефона.')
    else:
        result = numbers[0]
        result.remove(phone)
        if not result:
            result = None
        cursor.execute("""
        UPDATE client
        SET number = %s
        WHERE  client_id = %s""", (result, client_id))
        print(f'Абонентский номер {phone} удален у клиента с номером {client_id}')
    conn.commit()


def delete_client(cursor, client_id):
    cursor.execute("""
    SELECT client_id FROM client""")
    id = cursor.fetchall()
    find = 0
    for i in id:
        if client_id in i:
            find+=1
            cursor.execute("""
            DELETE FROM client
            WHERE client_id = %s""", (i[0],))
    conn.commit()
    if find == 0:
        print(f'Клиент с номером {client_id} отсутствует в базе данных.')
    else:
        print(f'Клиент с номером {client_id} удален из базы данных')


def find_client(cursor, first_name=None, last_name=None, email=None, phone=None):
    if first_name == None and last_name == None and email == None and phone == None:
        print('Не выбраны параметры для поиска')
    elif first_name != None and last_name != None: #Поиск по имени и фамилии
        cursor.execute("""
        SELECT * FROM client
        WHERE first_name = %s AND last_name = %s""", (first_name, last_name))
        result = cursor.fetchall()
        if not result:
            print('Клиент отсутствует в базе данных')
        else:
            print(result)
    elif email: # Поиск по email.
        cursor.execute("""
        SELECT * FROM client
        WHERE email = %s""", (email, ))
        result = cursor.fetchone()
        if not result:
            print('Клиент отсутствует в базе данных')
        else:
            print(result)
    elif phone: #Поиск клиента по номеру телефона
        cursor.execute("""
        SELECT * FROM client
        WHERE ARRAY_POSITION(number, %s) IS NOT NULL""", (phone,))
        result = cursor.fetchone()
        if result:
            print(result)
        else:
            print('Клиент с указанным номером телефона отсутствует в базе данных')

with conn.cursor() as cur:
    cur.execute("""
    DROP TABLE client;
    """)
    conn.commit()

    create_table(cur)
    add_client(cur, 'Ivan', 'Shevergen', 'Ishevergen@mail.ru')
    add_client(cur, 'Viktorya', 'Bellaus', 'BelausV@mail.ru', ["9226798356"])
    add_client(cur, 'Vladimir', 'Rakov', 'VR@kov@mail.ru', ["9281256747", "9222222222"])
    add_client(cur, 'Anastasiya', 'Volkova', 'AVolkova@mail.ru', ["9252345678"])
    print()

    add_phone(cur, 2, '9226798356')
    cur.execute("""SELECT first_name, last_name, email, number
            FROM client WHERE client_id = 2""")
    print(cur.fetchone())
    print()

    change_client(cur, 2, first_name='Silvester')
    change_client(cur, 2, last_name='Stalone', email='Sstalone@mail.ru')
    cur.execute("""SELECT first_name, last_name, email, number
            FROM client WHERE client_id = 2""")
    print(cur.fetchone())
    print()

    delete_phone(cur, 4, '9222222222')
    delete_phone(cur, 2, '9281256747')
    delete_phone(cur, 3, '9252345678')
    cur.execute("""SELECT first_name, last_name, email, number
        FROM client WHERE client_id = 4""")
    print(cur.fetchone())
    delete_phone(cur, 3, '12345')
    print()

    delete_client(cur, 1)
    delete_client(cur, 3)
    print()

    find_client(cur)
    find_client(cur, first_name='Viktorya', last_name='Bellaus')
    find_client(cur, first_name='Vladimir', last_name='Rakov')
    find_client(cur, email='Ishevergen@mail.ru')
    find_client(cur, email='VR@kov@mail.ru')
    find_client(cur, phone='9222222222')
    find_client(cur, phone='9876543210')

conn.close()


