import psycopg2

hostname='localhost'
database='techno musin events'
username='postgres'
pwd='1234'
port_id=5432
conn=None
cur=None

try:
    conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=pwd,
            host=hostname,
            port=port_id)
    
    cur = conn.cursor()


    

    cur.execute("DROP TABLE IF EXISTS eventhistory CASCADE;")

    cur.execute("""
    CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

    CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

    CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    countryid INT REFERENCES countries(id) ON DELETE CASCADE
);  
    
    
    
    CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    fullname VARCHAR,
    email VARCHAR,
    password VARCHAR,
    locationid INT REFERENCES locations(id) ON DELETE SET NULL,
    bio VARCHAR,
    registrationdate TIMESTAMP
);

    CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    genreid INT REFERENCES genres(id) ON DELETE SET NULL,
    bio TEXT,
    pictureurl TEXT,
    soundcloud TEXT,
    spotify TEXT,
    youtube TEXT
);

    CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    venue VARCHAR,
    date TIMESTAMP,
    coverurl VARCHAR,
    locationid INT REFERENCES locations(id) ON DELETE SET NULL,
    genreid INT REFERENCES genres(id) ON DELETE SET NULL
);

    CREATE TABLE eventartists (
    id SERIAL PRIMARY KEY,
    eventid INT REFERENCES events(id) ON DELETE CASCADE,
    artistid INT REFERENCES artists(id) ON DELETE CASCADE
);
    
    CREATE TABLE eventhistory (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id) ON DELETE CASCADE,
    eventid INT REFERENCES events(id) ON DELETE CASCADE,
    rate SMALLINT CHECK (rate BETWEEN 0 AND 5),
    hasattended SMALLINT CHECK (hasattended IN (0,1)),
    isinterested SMALLINT CHECK (isinterested IN (0,1))
);

    CREATE TABLE favoriteartists (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id) ON DELETE CASCADE,
    artistid INT REFERENCES artists(id) ON DELETE CASCADE
);

    CREATE TABLE favoritegenres (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id) ON DELETE CASCADE,
    genreid INT REFERENCES genres(id) ON DELETE CASCADE
);
""")

    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

print("All the tables have been created succesfully!")
