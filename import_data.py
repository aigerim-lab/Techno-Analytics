import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="techno musin events",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

tables = [
    "eventartists",
    "eventhistory",
    "favoriteartists",
    "favoritegenres",
    "events",
    "artists",
    "users",
    "locations",
    "countries",
    "genres"
]

for t in tables:
    print(f"🧹 Чищу таблицу {t}...")
    cur.execute(f"TRUNCATE TABLE {t} RESTART IDENTITY CASCADE;")
conn.commit()

files = {
    "countries": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/countries.csv",
    "genres": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/genres.csv",
    "locations": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/locations.csv",
    "users": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/users.csv",
    "artists": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/convertedArtists.csv",
    "events": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/events.csv",
    "eventartists": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/eventartists.csv",
    "eventhistory": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/eventhistory.csv",
    "favoriteartists": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/favoriteartists.csv",
    "favoritegenres": "/Users/aygerimkoszhanova/Desktop/docs/db/archive/favoritegenres.csv"
}


column_mapping = {
    "users": {
        "UserName": "username",
        "FullName": "fullname",
        "Email": "email",
        "Password": "password",
        "LocationId": "locationid",
        "Bio": "bio",
        "RegistrationDate": "registrationdate"
    },
    "artists": {
        "Name": "name",
        "GenreId": "genreid",
        "Bio": "bio",
        "PictureUrl": "pictureurl",
        "SoundCloud": "soundcloud",
        "Spotify": "spotify",
        "Youtube": "youtube"
    },
    "events": {
        "Name": "name",
        "Description": "description",
        "Venue": "venue",
        "Date": "date",
        "CoverUrl": "coverurl",
        "LocationId": "locationid",
        "GenreId": "genreid"
    }
    
}

for table, file in files.items():
    print(f"▶ Загружаю {file} в {table}...")
    df = pd.read_csv(file)

    
    if table in column_mapping:
        df.rename(columns=column_mapping[table], inplace=True)

    for i, row in df.iterrows():
        cols = ','.join(df.columns)
        vals = ','.join(['%s'] * len(row))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
        cur.execute(sql, tuple(row))
    conn.commit()

cur.close()
conn.close()
print("All the data have been succesfully imported!")
