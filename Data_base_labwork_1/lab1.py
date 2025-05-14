import threading, time
from threading import Thread
import psycopg2
from time import time
import random

DB_PARAMS = {
    "dbname":   "lab_1",
    "user":     "kyryl_o",
    "password": "157329",
    "host":     "localhost",
    "port":     5432,
}

def reset_counter():
    conn = psycopg2.connect(**DB_PARAMS)
    with conn as c, c.cursor() as cur:
        cur.execute("UPDATE user_counter SET counter = 0, version = 0 WHERE user_id = 1")

def lost_update():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    for _ in range(10000):
        cur.execute("SELECT counter FROM user_counter WHERE user_id = 1")
        counter = cur.fetchone()[0]
        counter += 1
        cur.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1", (counter,))
        conn.commit()
    cur.close()
    conn.close()

def inplace_update():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    for _ in range(10000):
        cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = 1")
        conn.commit()
    cursor.close()
    conn.close()

def row_lock_update():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    for _ in range(10000):
        cursor.execute("BEGIN")
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
        value = cursor.fetchone()[0] + 1
        cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1", (value,))
        conn.commit()
    cursor.close()
    conn.close()

def optimistic_update():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    for _ in range(10000):
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
            counter, version = cursor.fetchone()
            new_counter = counter + 1
            new_version = version + 1
            cursor.execute("""
                UPDATE user_counter SET counter = %s, version = %s
                WHERE user_id = %s AND version = %s
            """, (new_counter, new_version, 1, version))
            if cursor.rowcount > 0:
                conn.commit()
                break
    cursor.close()
    conn.close()

def run_test(fn, label):
    reset_counter()
    start = time()
    threads = [Thread(target=fn) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time()

    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
    final_value = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    print(f"{label} виконано за {end - start:.2f} секунд")
    print(f"Значення каунтера: {final_value}")

# Приклад:
run_test(lost_update, "Lost Update")
run_test(inplace_update, "In-place Update")
run_test(row_lock_update, "Row-Level Locking")
run_test(optimistic_update, "Optimistic Locking")