import csv
import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Resolve data directory relative to this script
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "job_links.csv"

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Run in headless mode for efficiency
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def collect_rozee_links(driver, max_links=10):
    print("Collecting from Rozee.pk...")
    search_url = "https://www.rozee.pk/job/jsearch/q/Software+Engineer"
    driver.get(search_url)
    time.sleep(3)
    
    job_links = set()
    # Basic scroll to trigger any lazy loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute('href')
        if href and 'rozee.pk' in href and '-jobs-' in href:
            clean_href = href.split('?')[0]
            job_links.add(clean_href)
            if len(job_links) >= max_links:
                break
    return list(job_links)

def collect_lever_links(driver, company_url, max_links=10):
    print(f"Collecting from Lever: {company_url}")
    driver.get(company_url)
    time.sleep(4)
    links = driver.find_elements(By.CSS_SELECTOR, "a.posting-title")
    job_urls = [link.get_attribute('href') for link in links if 'jobs.lever.co' in link.get_attribute('href')]
    return job_urls[:max_links]

def collect_greenhouse_links(driver, company_url, max_links=10):
    print(f"Collecting from Greenhouse: {company_url}")
    driver.get(company_url)
    time.sleep(4)
    # Greenhouse links often in .opening or specific page structure
    links = driver.find_elements(By.CSS_SELECTOR, "div.opening a, a[data-mapped='true']")
    job_urls = []
    for link in links:
        href = link.get_attribute('href')
        if href and ('boards.greenhouse.io' in href or 'jobs' in href):
            # Resolve relative links if necessary (handled by get_attribute('href') usually)
            job_urls.append(href)
    
    # Fallback for redirected pages like Dropbox
    if not job_urls:
         links = driver.find_elements(By.TAG_NAME, "a")
         job_urls = [l.get_attribute('href') for l in links if l.get_attribute('href') and ('/jobs/' in l.get_attribute('href') or '/opening/' in l.get_attribute('href'))]

    return list(set(job_urls))[:max_links]

def main():
    sources = [
        {"name": "Rozee.pk", "type": "rozee"},
        {"name": "Discord", "url": "https://boards.greenhouse.io/discord", "type": "greenhouse"},
        {"name": "Palantir", "url": "https://jobs.lever.co/palantir", "type": "lever"},
        {"name": "Figma", "url": "https://www.figma.com/careers/", "type": "greenhouse"},
        {"name": "Elastic", "url": "https://boards.greenhouse.io/elastic", "type": "greenhouse"},
    ]

    all_links = []
    driver = get_driver()

    try:
        for source in sources:
            try:
                if source["type"] == "rozee":
                    links = collect_rozee_links(driver)
                elif source["type"] == "lever":
                    links = collect_lever_links(driver, source["url"])
                elif source["type"] == "greenhouse":
                    links = collect_greenhouse_links(driver, source["url"])
                
                print(f"Found {len(links)} links for {source['name']}")
                all_links.extend(links)
            except Exception as e:
                print(f"Error collecting from {source['name']}: {e}")

    finally:
        driver.quit()

    # Save to CSV
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_url'])
        for link in all_links:
            writer.writerow([link])
    
    print(f"\nSuccessfully collected {len(all_links)} total links.")
    print(f"Results saved to {DATA_PATH}")

if __name__ == "__main__":
    main()
