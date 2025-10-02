# main.py
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine
from config import DB_URI
from pathlib import Path

SQL_FILE = Path(__file__).resolve().parent / "sql" / "new_queries.sql"

def load_queries(sql_path: Path) -> dict:
    text = sql_path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in text.split(";") if b.strip()]
    queries = {}
    for i, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        qname = None
        body = []
        for ln in lines:
            if ln.lower().startswith("-- name:"):
                qname = ln.split(":", 1)[1].strip()
            else:
                body.append(ln)
        if not qname:
            qname = f"q{i:02d}"
        queries[qname] = "\n".join(body).strip()
    return queries

def main():
    engine = create_engine(DB_URI)
    queries = load_queries(SQL_FILE)

    print("Available queries:", list(queries.keys()))

    # 1. Pie chart
    df = pd.read_sql(queries.get("q1_users_by_country", list(queries.values())[0]), engine)
    df.set_index(df.columns[0]).plot.pie(y=df.columns[1], autopct="%1.1f%%", legend=False)
    plt.title("Users by Country")
    plt.show()

    # 2. Bar chart
    df = pd.read_sql(queries.get("q2_events_by_genre", list(queries.values())[1]), engine)
    df.plot.bar(x=df.columns[0], y=df.columns[1], legend=False)
    plt.title("Events by Genre")
    plt.xlabel(df.columns[0]); plt.ylabel(df.columns[1])
    plt.xticks(rotation=30)
    plt.show()

    # 3. Horizontal bar chart
    df = pd.read_sql(queries.get("q3_top_artists_by_events", list(queries.values())[2]), engine)
    df.plot.barh(x=df.columns[0], y=df.columns[1], legend=False)
    plt.title("Top Artists by Events")
    plt.xlabel(df.columns[1]); plt.ylabel(df.columns[0])
    plt.show()

    # 4. Line chart
    df = pd.read_sql(queries.get("q4_events_by_month", list(queries.values())[3]), engine)
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"])
    df.plot(x=df.columns[0], y=df.columns[1], marker="o")
    plt.title("Events per Month")
    plt.xticks(rotation=30)
    plt.show()

    
    
    # 5. Histogram (Rating distribution)
    df = pd.read_sql(queries.get("q5_rating_distribution", list(queries.values())[4]), engine)
    col = df.columns[0]  # "rate"

    df[col].plot.hist(
    bins=range(int(df[col].min()), int(df[col].max())+2), 
    align="left", 
    rwidth=0.8
    )

    plt.title("Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.xticks(range(int(df[col].min()), int(df[col].max())+1))
    plt.yticks(range(0, df[col].value_counts().max()+1))
    plt.show()



    # 6. Scatter plot
    df = pd.read_sql(queries.get("q6_rating_vs_attendance", list(queries.values())[5]), engine) 
    df.plot.scatter(x=df.columns[1], y=df.columns[0])
    plt.title("Avg Rating vs Attended Events")
    plt.xlabel(df.columns[1]); plt.ylabel(df.columns[0])
    plt.show()

    # 7. Time slider (Plotly)
    sql = """
    WITH months AS (
      SELECT generate_series(
        date_trunc('month', MIN(e.date)),
        date_trunc('month', MAX(e.date)),
        interval '1 month'
      ) AS month
      FROM events e
    ),
    genres_used AS (
      SELECT DISTINCT g.id, g.name
      FROM events e
      JOIN genres g ON e.genreid = g.id
    ),
    counts AS (
      SELECT date_trunc('month', e.date) AS month,
             g.id AS genre_id,
             COUNT(*)::int AS cnt
      FROM events e
      JOIN genres g ON e.genreid = g.id
      GROUP BY month, g.id
    )
    SELECT m.month,
           gu.name AS genre,
           COALESCE(c.cnt, 0) AS cnt
    FROM months m
    CROSS JOIN genres_used gu
    LEFT JOIN counts c
           ON c.month = m.month AND c.genre_id = gu.id
    ORDER BY m.month, gu.name;
    """
    df = pd.read_sql(sql, engine)
    df["month_str"] = pd.to_datetime(df["month"]).dt.strftime("%Y-%m")
    fig = px.bar(
        df, x="genre", y="cnt",
        animation_frame="month_str",
        title="Events by Genre over Time",
        range_y=[0, max(1, df["cnt"].max()) * 1.2],
    )
    fig.show()

if __name__ == "__main__":
    main()
