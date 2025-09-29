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
    # 1. Events genre = 1
    "SELECT * FROM events WHERE genreid=1 ORDER BY date;",

    # 2. Count of artists by genre
    "SELECT genreid, COUNT(*) FROM artists GROUP BY genreid;",

    # 3. Count of users by location
    "SELECT locationid, COUNT(*) FROM users GROUP BY locationid;",

    # 4. 5 most recent events
    "SELECT id, name, date FROM events ORDER BY date DESC LIMIT 5;",

    # 5. Users with favorite artists
    """SELECT a.username, b.name AS favourite_artist
       FROM favoriteartists fa
       JOIN users a ON fa.userid=a.id
       JOIN artists b ON fa.artistid=b.id;""",

    # 6. Event names with location names
    """SELECT e.name AS event_name, l.name AS location_name
       FROM events e
       INNER JOIN locations l ON e.locationid = l.id;""",

    # 7. Users with country names
    """SELECT u.username, c.name AS country_name
       FROM users u
       LEFT JOIN locations l ON u.locationid = l.id
       LEFT JOIN countries c ON l.countryid = c.id;""",

    # 8. Artists with genre names
    """SELECT a.name AS artist_name, g.name AS genre_name
       FROM artists a
       RIGHT JOIN genres g ON a.genreid = g.id;""",

    # 9. Events with genres
    """SELECT e.name AS event_name, g.name AS genre_name
       FROM events e
       LEFT JOIN genres g ON e.genreid = g.id;""",

    # 10. Users and their favorite genres
    """SELECT u.username, g.name AS favorite_genre
       FROM favoritegenres fg
       INNER JOIN users u ON fg.userid = u.id
       INNER JOIN genres g ON fg.genreid = g.id;"""
]

# Выполнение всех запросов
for i, q in enumerate(queries, start=1):
    print(f"\n--- Query {i} ---")
    cur.execute(q)
    try:
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except psycopg2.ProgrammingError:
        print("No results to fetch or query has no output.")
    print("-" * 50)

# Закрываем соединение
cur.close()
conn.close()
print("Done")