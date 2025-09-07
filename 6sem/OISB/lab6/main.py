import sqlite3
import re

DB_FILE = 'data.db'

PROTECTION_ENABLED = False

pattern = r'^([a-zA-Z0-9_]+( (asc|desc))?(, [a-zA-Z0-9_]+( (asc|desc))?)*?)?$'

def list_users(sort_string):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            with conn:
                cur = conn.cursor()
                if PROTECTION_ENABLED:
                    if sort_string and re.match(pattern, sort_string):
                        order_by = f" ORDER BY {sort_string}"
                    else:
                        order_by = " ORDER BY id asc"
                    query = f'SELECT id, username, age FROM "USERS" {order_by}'
                    cur.execute(query)
                    users = cur.fetchall()
                    for user in users:
                        print(user)
                else:
                    queries = [q.strip() for q in sort_string.split(';') if q.strip()]
                    if not queries:
                        query = 'SELECT id, username, age FROM "USERS" ORDER BY id asc'
                        cur.execute(query)
                        users = cur.fetchall()
                        for user in users:
                            print(user)
                    else:
                        query = f'SELECT id, username, age FROM "USERS" ORDER BY {queries[0]}'
                        cur.execute(query)
                        results = cur.fetchall()
                        print("Результаты:")
                        for row in results:
                            print(row)
                        for query in queries[1:]:
                            cur.execute(query)
                            results = cur.fetchall()
                            if results:
                                print("Результаты:")
                                for row in results:
                                    print(row)
                            else:
                                print("Запрос выполнен, результатов нет.")
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")

# Главная функция
def main():
    print(f"Защита от SQL-инъекций: {'ВКЛЮЧЕНА' if PROTECTION_ENABLED else 'ВЫКЛЮЧЕНА'}")
    sort_string = input("Введите строку сортировки или SQL-запросы (например, 'username asc'): ")
    list_users(sort_string)

if __name__ == '__main__':
    main()