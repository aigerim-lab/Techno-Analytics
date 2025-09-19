import psycopg2


conn = psycopg2.connect(
    dbname="techno musin events",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


queries = [
    "SELECT * FROM artists LIMIT 5;",
    "SELECT genreid, COUNT(*) FROM artists GROUP BY genreid;",
    """
    SELECT e.name AS event_name, AVG(eh.rate) AS avg_rating
    FROM eventhistory eh
    JOIN events e ON eh.eventid = e.id
    GROUP BY e.name
    ORDER BY avg_rating DESC
    LIMIT 5;
    """
]

for q in queries:
    print(f"▶ Running query:\n{q.strip()}")
    cur.execute(q)
    try:
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except:
        print("No results to fetch.")
    print("-" * 50)

cur.close()
conn.close()
print("Done")
