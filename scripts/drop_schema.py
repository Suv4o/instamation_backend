import psycopg2

# console = Logger("app").get()

conn = psycopg2.connect(host="localhost", port="5432", database="database_dev", user="username", password="password")

cur = conn.cursor()

try:
    cur.execute("DROP SCHEMA IF EXISTS public CASCADE")
    # console.info("Dropped schema public")
except Exception as e:
    pass
    # console.error(e)

conn.commit()

cur.close()
conn.close()
