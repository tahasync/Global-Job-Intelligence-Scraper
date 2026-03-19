# 🚀 Rozee.pk Job Intelligence Scraper

An end-to-end data pipeline designed to automate job discovery and market intelligence for the software engineering sector in Pakistan. This project combines browser automation and high-performance crawling to generate actionable career insights.

---

## 🌟 Key Features

- **Hybrid Extraction**: Utilizes **Selenium** for dynamic link discovery and **Scrapy** for high-performance data extraction.
- **Intelligent Parsing**: Extracts data via DOM selectors and `application/ld+json` (JSON-LD) for maximum accuracy.
- **Robust Networking**: Includes a built-in fix for tracking redirects and TLS fingerprinting issues.
- **Automated Analysis**: Generates comprehensive market reports using **Pandas**, highlighting top skills, cities, and hiring trends.

---

## 🛠️ Project Architecture

```text
rozee_scraper/
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

## ⚙️ Prerequisites

- **Python 3.11+**
- **uv** (Modern Python package manager)
- **Chrome/ChromeDriver** (For Selenium phase)

---

## 🚀 Getting Started

### 1. Installation

Clone the repository and sync dependencies using `uv`:

```bash
uv sync
```

### 2. Running the Pipeline

The pipeline is executed in three logical phases:

#### **Phase 1: Discovery (Selenium)**

Collect job URLs from Rozee.pk search results.

```bash
uv run python selenium/link_collector.py
```

#### **Phase 2: Extraction (Scrapy)**

Crawl individual job pages and parse details.
*Note: The spider is configured with `allowed_domains` to filter out problematic tracking redirects.*

```bash
cd scrapy_project
uv run scrapy crawl jobs -o ../data/final/jobs.csv
```

#### **Phase 3: Intelligence (Pandas)**

Process the raw data and generate a professional market report.

```bash
cd analysis
uv run python analyze.py
```

---

## 📊 Market Intelligence

After running the pipeline, a detailed report is generated at `docs/report.md`. This report covers:

- ✅ **Top 10 In-Demand Skills**
- ✅ **Regional Hotspots** (Top Cities)
- ✅ **Leading Employers** in the Software Sector
- ✅ **Entry-Level Availability** (Internships/Junior roles)

---

## 🛡️ Compliance & Ethics

- **Respectful Crawling**: Configured with a `DOWNLOAD_DELAY` to prevent server strain.
- **Public Data Only**: Scrapes only publicly accessible job listings.
- **Privacy First**: No personal data or login credentials are required or processed.

---

*Created for University Assignment 1 - Focused on Web Intelligence and Data Engineering.*
