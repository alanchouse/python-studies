# TSIS4

## Docker только для PostgreSQL

```bash
cd TSIS4
docker compose up -d
```



`PG*` переменные читаются автоматически из файла `.env` в папке `TSIS4`.

### Windows (PowerShell)

```powershell
cd TSIS4
py -3.12 -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python main.py
```

## Остановить PostgreSQL

```bash
cd TSIS4
docker compose down
```
