# 📊Techno-Analytics

## 🏙️Company
**Techno Analytics** – This dataset is part of a research project aimed at developing a hybrid recommendation system for techno music events. The database stores user preferences, event details, artist metadata, and recommendation interactions, making it a valuable dataset for music recommendation research, user preference modeling, and event-based recommendation systems.
---

## 🎯 Overview
This project demonstrates full monitoring setup using **Prometheus**, **Grafana**, and **Exporters** for:
- PostgreSQL database performance (Database Dashboard)
- System-level metrics (Node Dashboard)

The dashboards visualize **real-time metrics**, **PromQL queries**, and include **alerts**, **global filters**, and **API verification**.

---

## 🧩 Project Structure
Assignment4/
│
├── docker-compose.yml
├── config/
│ └── prometheus.yml
├── postgres_exporter/
│ └── ...
├── node_exporter/
│ └── ...
├── dashboards/
│ ├── Database_Dashboard.json
│ └── Node_Dashboard.json
├── prometheus_api_test.py
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
- Docker & Docker Compose
- PostgreSQL database (your dataset)
- Python 3.8+

---

### 2️⃣ Run Prometheus + Exporters + Grafana
Create files as below and run:

```bash
docker-compose up -d
- Prometheus → http://localhost:9090
- Grafana → http://localhost:3000

3️⃣ prometheus.yml

Example configuration:

global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgres_exporter:9187']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'my_postgresql_db'

  - job_name: 'node'
    static_configs:
      - targets: ['node_exporter:9100']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'my_local_node'