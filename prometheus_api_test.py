import requests, json

URL = "http://localhost:9090/api/v1/query"
queries = [
    "pg_stat_database_numbackends",
    "pg_database_size_bytes",
    "rate(pg_stat_database_xact_commit[1m])",
    "rate(pg_stat_database_xact_rollback[1m])",
    "rate(pg_stat_database_blks_hit[5m])"
]

for q in queries:
    resp = requests.get(URL, params={"query": q})
    data = resp.json()
    print(f"\n--- {q} ---")
    print(json.dumps(data, indent=2))
