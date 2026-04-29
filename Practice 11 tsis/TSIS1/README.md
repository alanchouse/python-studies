# TSIS1

## Docker только для PostgreSQL

```bash
cd TSIS1
docker compose up -d
docker exec -i tsis1_postgres psql -U postgres -d phonebook_db < schema.sql
docker exec -i tsis1_postgres psql -U postgres -d phonebook_db < procedures.sql
```



### Windows (PowerShell)

```powershell
cd TSIS1
py -3.12 -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python phonebook.py
```

## Остановить PostgreSQL

```bash
cd TSIS1
docker compose down
```
