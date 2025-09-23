import psycopg2


conn = psycopg2.connect(
    dbname="techno musin events",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


cur.execute("Select name from artists Where name Like '%o';")
print(cur.fetchall())


queries = [
    """
    Select a.username, b.name As favourite_artist
    From favoriteartists fa 
    Join users a On fa.userid=a.id
    Join artists b On fa.artistid=b.id;



    SELECT e.name AS event_name, l.name AS location_name
    FROM events e
    INNER JOIN locations l ON e.locationid = l.id;
    """
]

for q in queries:
    
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
