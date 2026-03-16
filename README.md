# Rozee.pk Job Scraper Project

This project fulfills the university assignment requirements to build an end-to-end web scraper using Selenium and Scrapy. It targets Rozee.pk to discover software engineering positions and parse them into a structured dataset.

## Project Structure

- `selenium/`: Browser automation scripts using Selenium.
  - `link_collector.py`: Collects job detail URLs from standard site search.
- `scrapy_project/`: Scrapy spiders, items, and settings.
  - `jobs_spider.py`: Scrapes structured job data from the collected URLs using DOM parsing and JSON-LD.
- `data/raw/`: Contains intermediate data (`job_links.csv`).
- `data/final/`: Final exported dataset (`jobs.csv`).
- `analysis/`: Pandas script to extract insights from the data.
  - `analyze.py`: Reads the final dataset and outputs a markdown report.
- `docs/`: Markdown reports and findings.
  - `report.md`: The generated insight report.

## Requirements

1. **Python 3.11+**
2. **uv Package Manager**

## Setup and Installation

1. Clone or clone this repository.
2. Initialize and sync the project dependencies:
   ```bash
   uv sync
   ```

## Running the Pipeline

The workflow is divided into three consecutive steps:

1. **Run Link Collector (Selenium)**
   ```bash
   cd selenium
   uv run python link_collector.py
   ```
   *This outputs `data/raw/job_links.csv`.*

2. **Run Data Extractor (Scrapy)**
   ```bash
   cd scrapy_project
   uv run scrapy crawl jobs -o ../data/final/jobs.csv
   ```
   *This reads the raw links, visits each page, and writes the structured dataset.*

3. **Run Data Analysis (Pandas)**
   ```bash
   cd analysis
   uv run python analyze.py
   ```
   *This reads `jobs.csv` and outputs `docs/report.md`.*

## Analysis Insights
Please review `docs/report.md` for the trends, top skills, cities, companies, and roles derived from the scraped dataset.

## Compliance
- Only publicly available listings on Rozee.pk were scraped.
- No logins or bypasses were used.
- Scrapy delay (`DOWNLOAD_DELAY = 1`) was configured to respect the server.
