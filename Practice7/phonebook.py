import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row["name"], row["phone"])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV inserted")


def insert_console():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def update_contact():
    name = input("Name to update: ")
    new_phone = input("New phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()


def delete_contact():
    name = input("Name to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()


def menu():
    create_table()

    while True:
        print("\n1.Add CSV")
        print("2.Add manually")
        print("3.Show")
        print("4.Update")
        print("5.Delete")
        print("0.Exit")

        c = input("Choose: ")

        if c == "1":
            insert_from_csv()
        elif c == "2":
            insert_console()
        elif c == "3":
            show_contacts()
        elif c == "4":
            update_contact()
        elif c == "5":
            delete_contact()
        elif c == "0":
            break


menu()