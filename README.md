# Global Job Intelligence Scraper

A 3-phase Python pipeline that uses Selenium (URL discovery) + Scrapy (JSON-LD extraction with CSS fallbacks) + Pandas (market analysis) to scrape job postings from 5 online sources and generate a Markdown report of top skills, cities, companies, and entry-level opportunities.

## What it does

Phase 1 (Selenium) opens Chrome headless, scrolls for lazy-loaded listings, and collects job detail URLs from Rozee.pk, Discord (Greenhouse ATS), Palantir (Lever ATS), Figma, and Mustakbil. Phase 2 (Scrapy) reads those URLs, parses `application/ld+json` (JSON-LD) structured data with CSS selector fallbacks for each field, and outputs clean job records. Phase 3 (Pandas) analyzes the extracted data — skill keyword matching, location/company frequency, entry-level detection — and writes `docs/report.md` with market insights.

## Tech stack

- Python 3.11+, Selenium (Chrome WebDriver), Scrapy, Pandas, `w3lib` (HTML tag removal)
- Package manager: `uv`

## Features

- **Multi-source extraction** — Rozee.pk, Discord (Greenhouse), Palantir (Lever), Figma, Mustakbil
- **ATS-agnostic parsing** — Handles Greenhouse and Lever ATS patterns; JSON-LD extraction with CSS fallbacks
- **Market analysis** — Top skills, cities, employers, entry-level availability
- **Sample output** — `docs/report.md` shows 69 job records with Python as top skill (17 mentions)

## Setup

```bash
git clone https://github.com/tahasync/Global-Job-Intelligence-Scraper.git
cd Global-Job-Intelligence-Scraper
uv sync

# Phase 1: URL discovery
uv run python selenium/link_collector.py

# Phase 2: Job extraction
cd scrapy_project && uv run python -m scrapy crawl jobs -o ../data/final/jobs.csv

# Phase 3: Market analysis
cd analysis && uv run python analyze.py
```

## Status

**Academic project — complete.** Scrapes 5 real job sources with working Selenium + Scrapy integration. Generated report included. Note: `items.py` in the Scrapy project is empty (unused); `pipelines.py` and `middlewares.py` are default Scrapy boilerplate.

*Created for University Assignment 1 — Web Intelligence and Data Engineering*