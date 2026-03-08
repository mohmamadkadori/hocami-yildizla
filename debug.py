import psycopg2

try:
    conn = psycopg2.connect(
        host="db.gnqtismdbgwyyzcxgneg.supabase.co",
        dbname="postgres",
        user="postgres",
        password="YOUR_PASSWORD",
        port=5432
    )
    print("Connected")
except Exception as e:
    print(e)