
import csv
import json
from connect import get_connection


# create table
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()



# import contacts from csv
def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    try:
        with open("contacts.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                group_name = row.get("group") or "Other"

                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING",
                    (group_name,)
                )

                cur.execute(
                    "SELECT id FROM groups WHERE name = %s",
                    (group_name,)
                )
                group_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO contacts
                    (name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    row["name"],
                    row["phone"],
                    row.get("email") or None,
                    row.get("birthday") or None,
                    group_id
                ))

                contact_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (
                    contact_id,
                    row["phone"],
                    row.get("type") or "mobile"
                ))

        conn.commit()
        print("Contacts imported successfully!")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()



# add contact manually
def insert_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ") or None
    birthday = input("Enter birthday (YYYY-MM-DD): ") or None
    group_name = input("Enter group: ") or "Other"

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING",
            (group_name,)
        )

        cur.execute(
            "SELECT id FROM groups WHERE name = %s",
            (group_name,)
        )
        group_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts
            (name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (name, phone, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, 'mobile')
        """, (contact_id, phone))

        conn.commit()
        print("Contact added!")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()




# show all contacts with all phone numbers
def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
    """)

    contacts = cur.fetchall()

    if contacts:
        print("\nID | NAME | EMAIL | BIRTHDAY | GROUP | PHONES")
        print("-" * 80)

        for contact in contacts:
            print(" | ".join(
                str(value) if value is not None else "-"
                for value in contact
            ))
    else:
        print("PhoneBook is empty.")

    cur.close()
    conn.close()


# search cont
def search_contacts():
    print("1. Search by name")
    print("2. Search by phone prefix")

    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s",
            (f"%{name}%",)
        )

    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute(
            "SELECT * FROM contacts WHERE phone LIKE %s",
            (f"{prefix}%",)
        )

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    if not contacts:
        print("No contacts found.")

    cur.close()
    conn.close()



# update contact
def update_contact():
    contact_id = input("Enter contact ID: ")

    print("1. Update name")
    print("2. Update phone")
    print("3. Update email")
    print("4. Update birthday")

    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            value = input("Enter new name: ")
            cur.execute(
                "UPDATE contacts SET name = %s WHERE id = %s",
                (value, contact_id)
            )

        elif choice == "2":
            value = input("Enter new phone: ")

            cur.execute(
                "UPDATE contacts SET phone = %s WHERE id = %s",
                (value, contact_id)
            )

            cur.execute("""
                UPDATE phones
                SET phone = %s
                WHERE contact_id = %s
                AND type = 'mobile'
            """, (value, contact_id))

        elif choice == "3":
            value = input("Enter new email: ")
            cur.execute(
                "UPDATE contacts SET email = %s WHERE id = %s",
                (value, contact_id)
            )

        elif choice == "4":
            value = input("Enter new birthday (YYYY-MM-DD): ")
            cur.execute(
                "UPDATE contacts SET birthday = %s WHERE id = %s",
                (value, contact_id)
            )

        else:
            print("Invalid choice.")
            return

        conn.commit()

        if cur.rowcount > 0:
            print("Contact updated!")
        else:
            print("Contact not found.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()

#del cont
def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "DELETE FROM contacts WHERE name = %s",
            (name,)
        )

    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute(
            "DELETE FROM contacts WHERE phone = %s",
            (phone,)
        )

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    conn.commit()

    if cur.rowcount > 0:
        print("Contact deleted!")
    else:
        print("Contact not found.")

    cur.close()
    conn.close()



# add another phone to contact
def add_phone():
    name = input("Enter contact name: ")
    phone = input("Enter phone: ")
    phone_type = input("Enter type (home/work/mobile): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL add_phone(%s, %s, %s)",
        (name, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added!")


# move contact to group
def move_contact():
    name = input("Enter contact name: ")
    group = input("Enter group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL move_to_group(%s, %s)",
        (name, group)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved!")


# search by name email or phone
def advanced_search():
    query = input("Enter name, email or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (query,)
    )

    results = cur.fetchall()

    for contact in results:
        print(contact)

    if not results:
        print("No contacts found.")

    cur.close()
    conn.close()


# filter contacts by group
def filter_group():
    group = input("Enter group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
    """, ('%' + group + '%',))

    results = cur.fetchall()

    for contact in results:
        print(contact)

    if not results:
        print("No contacts found.")

    cur.close()
    conn.close()


# sort contacts
def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    columns = {
        "1": "name",
        "2": "birthday",
        "3": "created_at"
    }

    if choice not in columns:
        print("Invalid choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"SELECT id, name, email, birthday FROM contacts ORDER BY {columns[choice]} NULLS LAST"
    )

    for contact in cur.fetchall():
        print(contact)

    cur.close()
    conn.close()


# pagination
def paginate_contacts():
    limit = 5
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        results = cur.fetchall()

        for contact in results:
            print(contact)

        cur.close()
        conn.close()

        command = input("next / prev / quit: ").lower()

        if command == "next":
            if len(results) == limit:
                offset += limit
            else:
                print("Last page.")

        elif command == "prev":
            offset = max(0, offset - limit)

        elif command == "quit":
            break

        else:
            print("Invalid command.")


# export contacts to JSON
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    contacts = {}

    for row in cur.fetchall():
        contact_id, name, email, birthday, group, phone, phone_type = row

        if contact_id not in contacts:
            contacts[contact_id] = {
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group,
                "phones": []
            }

        if phone:
            contacts[contact_id]["phones"].append({
                "phone": phone,
                "type": phone_type
            })

    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(list(contacts.values()), file, ensure_ascii=False, indent=4)

    cur.close()
    conn.close()

    print("Export completed!")


# import contacts from JSON
def import_json():
    with open("contacts.json", "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    try:
        for item in contacts:
            cur.execute(
                "SELECT id FROM contacts WHERE name = %s LIMIT 1",
                (item["name"],)
            )

            existing = cur.fetchone()

            if existing:
                choice = input(
                    f'{item["name"]} exists. Skip or overwrite? (s/o): '
                ).lower()

                if choice == "s":
                    continue

                contact_id = existing[0]

                cur.execute("""
                    UPDATE contacts
                    SET email = %s, birthday = %s
                    WHERE id = %s
                """, (
                    item.get("email"),
                    item.get("birthday"),
                    contact_id
                ))

                cur.execute(
                    "DELETE FROM phones WHERE contact_id = %s",
                    (contact_id,)
                )

            else:
                group_name = item.get("group") or "Other"

                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING",
                    (group_name,)
                )

                cur.execute(
                    "SELECT id FROM groups WHERE name = %s",
                    (group_name,)
                )
                group_id = cur.fetchone()[0]

                phones = item.get("phones", [])
                main_phone = phones[0]["phone"] if phones else "00000"

                cur.execute("""
                    INSERT INTO contacts(name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    item["name"],
                    main_phone,
                    item.get("email"),
                    item.get("birthday"),
                    group_id
                ))

                contact_id = cur.fetchone()[0]

            for phone_item in item.get("phones", []):
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (
                    contact_id,
                    phone_item["phone"],
                    phone_item.get("type", "mobile")
                ))

        conn.commit()
        print("Import completed!")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()



# menu
def menu():
    create_table()

    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Import contacts from CSV")
        print("2. Add contact manually")
        print("3. Show all contacts")
        print("4. Search contacts")
        print("5. Update contact")
        print("6. Delete contact")
        print("7. Add another phone")
        print("8. Move contact to group")
        print("9. Advanced search")
        print("10. Filter by group")
        print("11. Sort contacts")
        print("12. Paginated contacts")
        print("13. Export JSON")
        print("14. Import JSON")

        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_console()
        elif choice == "3":
            show_contacts()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            add_phone()
        elif choice == "8":
            move_contact()
        elif choice == "9":
            advanced_search()
        elif choice == "10":
            filter_group()
        elif choice == "11":
            sort_contacts()
        elif choice == "12":
            paginate_contacts()
        elif choice == "13":
            export_json()
        elif choice == "14":
            import_json()
         
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()

