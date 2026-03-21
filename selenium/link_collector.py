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

def collect_ats_links(driver, url, max_links=10):
    print(f"Collecting from ATS: {url}")
    driver.get(url)
    
    try:
        # Wait for at least one <a> tag to be present
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    except:
        print(f"Wait timeout for {url}")

    time.sleep(5)
    
    # Scroll multiple times to handle lazy loading
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    job_urls = []
    print(f"Total raw links found on {url}: {len(links)}")
    
    for link in links:
        try:
            href = link.get_attribute('href')
            if not href: continue
            
            # Robust filtering for direct job postings
            # Greenhouse: gh_jid or /jobs/ with digits
            # Lever: /jobs.lever.co/company/abc-123
            # Ashby: /ashbyhq.com/company/abc-123
            is_job = (('boards.greenhouse.io' in href and '/jobs/' in href and any(char.isdigit() for char in href.rstrip('/').split('/')[-1])) or ('gh_jid=' in href)) or \
                     ('lever.co' in href and len(href.rstrip('/').split('/')) >= 5) or \
                     ('ashbyhq.com' in href and len(href.rstrip('/').split('/')) >= 5)
            
            if is_job:
                job_urls.append(href)
        except:
            continue

    return list(set(job_urls))[:max_links]

def collect_mustakbil_links(driver, max_links=10):
    url = "https://www.mustakbil.com/jobs/software-engineer"
    print(f"Collecting from Mustakbil: {url}")
    driver.get(url)
    time.sleep(5)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    job_urls = []
    for link in links:
        try:
            href = link.get_attribute('href')
            if href and 'mustakbil.com/job/' in href:
                job_urls.append(href)
        except: continue
    return list(set(job_urls))[:max_links]

def main():
    sources = [
        {"name": "Rozee.pk", "type": "rozee"},
        {"name": "Discord", "url": "https://boards.greenhouse.io/discord", "type": "ats"},
        {"name": "Palantir", "url": "https://jobs.lever.co/palantir", "type": "ats"},
        {"name": "Figma", "url": "https://www.figma.com/careers/", "type": "ats"},
        {"name": "Mustakbil", "type": "mustakbil"},
    ]

    all_links = []
    driver = get_driver()

    try:
        for source in sources:
            try:
                if source["type"] == "rozee":
                    links = collect_rozee_links(driver)
                elif source["type"] == "mustakbil":
                    links = collect_mustakbil_links(driver)
                else:
                    links = collect_ats_links(driver, source["url"])
                
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
