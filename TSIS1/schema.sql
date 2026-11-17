
-- сreate groups table
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- adding new columns to contac
ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS email VARCHAR(100),
ADD COLUMN IF NOT EXISTS birthday DATE,
ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id),
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- create phones table
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

-- add default groupss
INSERT INTO groups (name)
VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other')
ON CONFLICT (name) DO NOTHING;

-- move old phone numbers to phones table
INSERT INTO phones (contact_id, phone, type)
SELECT c.id, c.phone, 'mobile'
FROM contacts c
WHERE c.phone IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM phones p
    WHERE p.contact_id = c.id
    AND p.phone = c.phone
);

-- check results
SELECT * FROM groups;
SELECT * FROM contacts;
SELECT * FROM phones;
