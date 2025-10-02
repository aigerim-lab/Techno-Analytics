import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import uuid
from config import DB_URI

engine = create_engine(DB_URI)

sql_chart = """
SELECT g.name AS genre, COUNT(e.id) AS events_count
FROM events e
JOIN genres g ON g.id = e.genreid
GROUP BY g.name
ORDER BY events_count DESC;
"""

def plot_events_by_genre(msg):
    df = pd.read_sql(sql_chart, engine)
    df.plot.bar(x="genre", y="events_count", legend=False)
    plt.title(f"Events by Genre ({msg})")
    plt.xlabel("Genre"); plt.ylabel("Events")
    plt.xticks(rotation=30)
    plt.show()
    return df

def insert_demo_event():
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO events (name, description, venue, date, locationid, genreid)
            VALUES (:name, 'demo insert', 'Hall A', '2025-10-01', 6, 3);
        """), {"name": f"Demo-{uuid.uuid4().hex[:6]}"})   # уникальное имя

def delete_demo_events():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM events WHERE description = 'demo insert';"))

# === Демонстрация ===
print("До вставки:")
plot_events_by_genre("Before")

print("Добавляем событие...")
insert_demo_event()

print("После вставки:")
plot_events_by_genre("After Insert")

print("Удаляем событие...")
delete_demo_events()

print("После удаления:")
plot_events_by_genre("After Delete")
