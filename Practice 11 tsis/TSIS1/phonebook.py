import csv
import json
import re
from datetime import datetime
from pathlib import Path

from psycopg2.extras import RealDictCursor

from connect import get_connection


BASE_DIR = Path(__file__).resolve().parent
PHONE_PATTERN = re.compile(r"^\+?\d{7,15}$")
PHONE_TYPES = {"home", "work", "mobile"}
SORT_COLUMNS = {
    "name": "c.name",
    "birthday": "c.birthday",
    "date": "c.created_at",
}


def run_sql_file(filename):
    path = BASE_DIR / filename
    with open(path, "r", encoding="utf-8") as file:
        sql_text = file.read()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_text)
        conn.commit()


def init_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    print("Schema and procedures are ready.")


def valid_phone(phone):
    return bool(PHONE_PATTERN.match(phone or ""))


def valid_phone_type(phone_type):
    return (phone_type or "").lower() in PHONE_TYPES


def parse_date(date_text):
    if not date_text:
        return None
    return datetime.strptime(date_text, "%Y-%m-%d").date()


def get_or_create_group(cur, group_name):
    group_name = (group_name or "Other").strip() or "Other"
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT(name) DO NOTHING",
        (group_name,),
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def upsert_contact_with_phone(cur, name, email, birthday, group_name, phone, phone_type):
    if not valid_phone(phone):
        raise ValueError(f"Invalid phone format: {phone}")
    if not valid_phone_type(phone_type):
        raise ValueError(f"Invalid phone type: {phone_type}")

    group_id = get_or_create_group(cur, group_name)
    cur.execute(
        """
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT(name)
        DO UPDATE SET email = EXCLUDED.email,
                      birthday = EXCLUDED.birthday,
                      group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (name, email, birthday, group_id),
    )
    contact_id = cur.fetchone()[0]
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type.lower()))
    return contact_id


def import_from_csv(path):
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        upsert_contact_with_phone(
                            cur=cur,
                            name=row["name"].strip(),
                            email=(row.get("email") or "").strip() or None,
                            birthday=parse_date((row.get("birthday") or "").strip()),
                            group_name=(row.get("group") or "Other").strip(),
                            phone=(row.get("phone") or "").strip(),
                            phone_type=(row.get("type") or "mobile").strip().lower(),
                        )
                    except Exception as err:
                        print(f"Skipped row {row}: {err}")
        conn.commit()
    print(f"CSV import finished: {path}")


def fetch_contacts(group_name=None, email_query=None, sort_by="name"):
    order_column = SORT_COLUMNS.get(sort_by, "c.name")
    where_clauses = []
    params = []

    if group_name:
        where_clauses.append("g.name = %s")
        params.append(group_name)
    if email_query:
        where_clauses.append("COALESCE(c.email, '') ILIKE %s")
        params.append(f"%{email_query}%")

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    query = f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name,
            c.created_at,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        {where_sql}
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order_column}
    """

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 60)
        print(f"Name      : {row['name']}")
        print(f"Email     : {row['email'] or '-'}")
        print(f"Birthday  : {row['birthday'] or '-'}")
        print(f"Group     : {row['group_name'] or '-'}")
        print(f"Phones    : {row['phones'] or '-'}")
        print(f"Date added: {row['created_at']}")
    print("-" * 60)


def paginate_contacts():
    page_size = int(input("Page size (default 3): ") or "3")
    page = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            while True:
                try:
                    cur.execute(
                        "SELECT * FROM get_contacts_paginated(%s, %s)",
                        (page_size, page * page_size),
                    )
                except Exception:
                    conn.rollback()
                    cur.execute(
                        """
                        SELECT c.name, COALESCE(p.phone, '')
                        FROM contacts c
                        LEFT JOIN LATERAL (
                            SELECT phone
                            FROM phones
                            WHERE contact_id = c.id
                            ORDER BY id
                            LIMIT 1
                        ) p ON TRUE
                        ORDER BY c.name
                        LIMIT %s OFFSET %s
                        """,
                        (page_size, page * page_size),
                    )

                rows = cur.fetchall()
                if not rows:
                    print("No rows on this page.")
                else:
                    print(f"\nPage {page + 1}:")
                    for item in rows:
                        print(item)

                action = input("Command [next/prev/quit]: ").strip().lower()
                if action == "next":
                    page += 1
                elif action == "prev":
                    page = max(0, page - 1)
                elif action == "quit":
                    break
                else:
                    print("Unknown command.")


def export_to_json(path):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    c.id, c.name, c.email, c.birthday, c.created_at,
                    g.name AS group_name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.name
                """
            )
            contacts = cur.fetchall()

            cur.execute(
                """
                SELECT p.contact_id, p.phone, p.type
                FROM phones p
                ORDER BY p.id
                """
            )
            phones = cur.fetchall()

    phone_map = {}
    for row in phones:
        phone_map.setdefault(row["contact_id"], []).append(
            {"phone": row["phone"], "type": row["type"]}
        )

    result = []
    for c in contacts:
        result.append(
            {
                "name": c["name"],
                "email": c["email"],
                "birthday": c["birthday"].isoformat() if c["birthday"] else None,
                "group": c["group_name"],
                "created_at": c["created_at"].isoformat(),
                "phones": phone_map.get(c["id"], []),
            }
        )

    with open(path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    print(f"Exported {len(result)} contacts to {path}")


def import_from_json(path):
    with open(path, "r", encoding="utf-8") as file:
        records = json.load(file)

    with get_connection() as conn:
        with conn.cursor() as cur:
            for rec in records:
                name = (rec.get("name") or "").strip()
                if not name:
                    print("Skipped record without name.")
                    continue

                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                existing = cur.fetchone()
                if existing:
                    choice = input(
                        f'Contact "{name}" exists. [s]kip or [o]verwrite? '
                    ).strip().lower()
                    if choice.startswith("s"):
                        continue

                    group_id = get_or_create_group(cur, rec.get("group") or "Other")
                    cur.execute(
                        """
                        UPDATE contacts
                        SET email = %s,
                            birthday = %s,
                            group_id = %s
                        WHERE id = %s
                        """,
                        (
                            rec.get("email"),
                            parse_date(rec.get("birthday")),
                            group_id,
                            existing[0],
                        ),
                    )
                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing[0],))
                    contact_name = name
                else:
                    group_id = get_or_create_group(cur, rec.get("group") or "Other")
                    cur.execute(
                        """
                        INSERT INTO contacts(name, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            name,
                            rec.get("email"),
                            parse_date(rec.get("birthday")),
                            group_id,
                        ),
                    )
                    existing = cur.fetchone()
                    contact_name = name

                for phone_info in rec.get("phones", []):
                    phone_value = (phone_info.get("phone") or "").strip()
                    phone_type = (phone_info.get("type") or "mobile").strip().lower()
                    if not valid_phone(phone_value) or not valid_phone_type(phone_type):
                        print(
                            f"Skipped invalid phone for {contact_name}: "
                            f"{phone_value} ({phone_type})"
                        )
                        continue
                    cur.execute(
                        "CALL add_phone(%s, %s, %s)",
                        (contact_name, phone_value, phone_type),
                    )

        conn.commit()
    print(f"JSON import finished: {path}")


def search_everywhere():
    query = input("Search query (name/email/phone): ").strip()
    if not query:
        return

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()
    print_contacts(rows)


def advanced_filter_menu():
    group_name = input("Group (or empty): ").strip() or None
    email_query = input("Email contains (or empty): ").strip() or None
    sort_by = input("Sort by [name/birthday/date]: ").strip().lower() or "name"
    rows = fetch_contacts(group_name=group_name, email_query=email_query, sort_by=sort_by)
    print_contacts(rows)


def menu():
    while True:
        print(
            """
1. Init DB schema + procedures
2. Import contacts from CSV
3. Filter/search/sort contacts
4. Paginated navigation (next/prev/quit)
5. Export all contacts to JSON
6. Import contacts from JSON
7. Search contacts via DB function
0. Exit
"""
        )
        choice = input("Choose option: ").strip()

        if choice == "1":
            init_database()
        elif choice == "2":
            default_csv = str(BASE_DIR / "contacts.csv")
            path = input(f"CSV path [{default_csv}]: ").strip() or default_csv
            import_from_csv(path)
        elif choice == "3":
            advanced_filter_menu()
        elif choice == "4":
            paginate_contacts()
        elif choice == "5":
            default_json = str(BASE_DIR / "contacts_export.json")
            path = input(f"Export path [{default_json}]: ").strip() or default_json
            export_to_json(path)
        elif choice == "6":
            default_json = str(BASE_DIR / "contacts_export.json")
            path = input(f"Import path [{default_json}]: ").strip() or default_json
            import_from_json(path)
        elif choice == "7":
            search_everywhere()
        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    menu()
