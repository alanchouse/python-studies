from connect import get_connection

def search():
    pattern = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def upsert():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def delete():
    value = input("Name or phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    while True:
        print("\n1.Search")
        print("2.Upsert")
        print("3.Pagination")
        print("4.Delete")
        print("0.Exit")

        c = input("Choose: ")

        if c == "1":
            search()
        elif c == "2":
            upsert()
        elif c == "3":
            pagination()
        elif c == "4":
            delete()
        elif c == "0":
            break

menu()