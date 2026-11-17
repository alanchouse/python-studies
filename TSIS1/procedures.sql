
--insert or update contact
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts WHERE name = p_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- insert contacts with phone validation
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names TEXT[],
    p_phones TEXT[],
    INOUT p_invalid TEXT[] DEFAULT ARRAY[]::TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
BEGIN
    p_invalid := ARRAY[]::TEXT[];

    IF array_length(p_names, 1) IS DISTINCT FROM
       array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Names and phones arrays must have equal length';
    END IF;

    FOR i IN 1..COALESCE(array_length(p_names, 1), 0)
    LOOP
        IF p_names[i] IS NULL OR btrim(p_names[i]) = ''
           OR p_phones[i] !~ '^[0-9]{5,20}$' THEN
            p_invalid := array_append(
                p_invalid,
                COALESCE(p_names[i], 'Unknown') || ': ' ||
                COALESCE(p_phones[i], 'NULL')
            );
        ELSIF EXISTS (
            SELECT 1 FROM contacts WHERE name = p_names[i]
        ) THEN
            p_invalid := array_append(
                p_invalid,
                p_names[i] || ': contact already exists'
            );
        ELSE
            INSERT INTO contacts(name, phone)
            VALUES (p_names[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;


-- delete contact by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_type = 'name' THEN
        DELETE FROM contacts WHERE name = p_value;
    ELSIF p_type = 'phone' THEN
        DELETE FROM contacts WHERE phone = p_value;
    ELSE
        RAISE EXCEPTION 'Type must be name or phone';
    END IF;
END;
$$;

-- Добавить дополнительный номер контакту
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type';
    END IF;

    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- Переместить контакт в группу
-- Если группы нет, создать её
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;


-- поиск по имени имаил и все телефонам
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE
        c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    ORDER BY c.id;
END;
$$;
