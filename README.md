# 🚀 Global Job Intelligence Scraper

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-2F558C?logo=python&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-8EC63F?logo=scrapy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)

An end-to-end data pipeline designed to automate job discovery and market intelligence across multiple global career portals. This project utilizes a hybrid **Selenium-Scrapy** architecture to target 5 diverse job sources.

---

## ✨ Features

- **🌍 Multi-Source Extraction** — Targets 5 diverse career portals (Rozee.pk, Discord, Palantir, Figma, Elastic)
- **🧩 Universal ATS Support** — Handles Lever and Greenhouse platforms alongside custom scrapers
- **📄 Intelligent Parsing** — Uses `application/ld+json` (JSON-LD) for high-accuracy extraction with CSS fallbacks
- **📊 Automated Analysis** — Generates comprehensive market reports with Pandas, highlighting top skills and hiring trends
- **🛡️ Ethical Crawling** — Respectful delays, public data only, no personal data collection

---

## 🏗️ Architecture

```text
Global Job Intelligence Scraper/
├── selenium/            # Phase 1: Browser automation for URL discovery
│   └── link_collector.py
├── scrapy_project/      # Phase 2: High-concurrency job data extraction
│   └── scraper/
│       └── spiders/
│           └── jobs_spider.py
├── analysis/           # Phase 3: Data processing and insight generation
│   └── analyze.py
├── data/               # Persistent storage for raw and final datasets
│   ├── raw/
│   └── final/
└── docs/               # Generated reports and documentation
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Selenium** | Browser automation for job URL discovery |
| **Scrapy** | High-concurrency data extraction |
| **BeautifulSoup** | HTML parsing fallback |
| **Pandas** | Data analysis and report generation |
| **uv** | Modern Python package manager |

---

## ⚙️ Prerequisites

- **Python 3.11+**
- **uv** (Modern Python package manager)
- **Chrome/ChromeDriver** (For Selenium phase)

---

## 🚀 Setup

### 1. Clone & Install

```bash
git clone https://github.com/mtahanaeem/Global-Job-Intelligence-Scraper.git
cd Global-Job-Intelligence-Scraper
uv sync
```

### 2. Run the Pipeline

**Phase 1 — Discovery (Selenium):**
```bash
uv run python selenium/link_collector.py
```

**Phase 2 — Extraction (Scrapy):**
```bash
cd scrapy_project
uv run python -m scrapy crawl jobs -o ../data/final/jobs.csv
```

**Phase 3 — Intelligence (Pandas):**
```bash
cd analysis
uv run python analyze.py
```

---

## 📈 Market Intelligence

After running the pipeline, a detailed report is generated at `docs/report.md` covering:

- ✅ **Top 10 In-Demand Skills**
- ✅ **Regional Hotspots** (Top Cities)
- ✅ **Leading Employers** in the Software Sector
- ✅ **Entry-Level Availability** (Internships / Junior roles)

---

## 🛡️ Compliance & Ethics

- **Respectful Crawling** — Configured with a `DOWNLOAD_DELAY` to prevent server strain
- **Public Data Only** — Scrapes only publicly accessible job listings
- **Privacy First** — No personal data or login credentials are required or processed

---

## 👤 Author

**Muhammad Taha Naeem**

- 📧 muhamadtahanaeem.pro@gmail.com
- 🐙 [mtahanaeem](https://github.com/mtahanaeem)

---

*Created for University Assignment 1 — Web Intelligence and Data Engineering*
