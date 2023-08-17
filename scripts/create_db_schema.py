import sys

sys.path.append("..")

import psycopg2
from config.logging import Logger
from config.environments import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

console = Logger("app").get()

conn = psycopg2.connect(
    host=POSTGRES_HOST, port=POSTGRES_PORT, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD
)

cur = conn.cursor()

try:
    cur.execute("CREATE SCHEMA IF NOT EXISTS public")
    console.info("Dropped schema public")
except Exception as e:
    console.error(e)

conn.commit()

cur.close()
conn.close()
