import os
import psycopg2

# Connexion à la base postgre
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# Query
cursor.execute("SELECT * FROM Bank WHERE trustScore < 1;")
rows = cursor.fetchall()
print(rows)

# Déconnexion
cursor.close()
conn.close()
