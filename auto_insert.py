import time
import random
from datetime import datetime
from sqlalchemy import create_engine, text

# === connection string ===
DB_URI = "postgresql+psycopg2://postgres:1234@localhost:5432/techno musin events"
engine = create_engine(DB_URI, echo=False)

print("Auto insert started... Press Ctrl+C to stop.")

while True:
    genreid = random.randint(1, 5)
    locationid = random.randint(6, 18)
    event_name = f"Live Event #{random.randint(100,999)}"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = text("""
        INSERT INTO events (name, description, venue, date, locationid, genreid)
        VALUES (:name, :desc, :venue, :date, :loc, :genre)
    """)

    with engine.connect() as conn:
        conn.execute(sql, {
            "name": event_name,
            "desc": "Auto-generated event",
            "venue": "Main Hall",
            "date": date,
            "loc": locationid,
            "genre": genreid
        })
        conn.commit()

    print(f"[OK] Added new event: {event_name} at {date}")
    time.sleep(10)  # каждые 10 секунд
