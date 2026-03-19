import csv
import time
import os
from pathlib import Path
from selenium import webdriver

# Resolve data directory relative to this script, not the working directory
BASE_DIR = Path(__file__).parent.parent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def collect_rozee_links(search_query="Software Engineer", max_links=50):
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Uncomment for headless mode if needed
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the driver
    driver = webdriver.Chrome(options=options)
    
    # Encode the search query
    query_encoded = search_query.replace(' ', '+')
    search_url = f"https://www.rozee.pk/job/jsearch/q/{query_encoded}"
    
    print(f"Navigating to {search_url}")
    driver.get(search_url)
    
    # Wait for the job listings container to load
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job")))
    except Exception as e:
        print("Timeout waiting for job listings. Page source might be different.")
        # Proceed anyway to see if we can find links
        
    job_links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while len(job_links) < max_links:
        # Extract links on current view
        links = driver.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            href = link.get_attribute('href')
            if href and 'rozee.pk' in href and '-jobs-' in href:
                # Remove tracking queries
                clean_href = href.split('?')[0]
                job_links.add(clean_href)
                if len(job_links) >= max_links:
                    break
                    
        print(f"Collected {len(job_links)} links so far...")
                
        if len(job_links) >= max_links:
            break
            
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Rozee typically has pagination. Let's look for a 'next' button if scrolling doesn't load more
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Try to click next page
            try:
                next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'next') or contains(text(), 'Next')]")
                if next_button:
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)
                else:
                    print("Reached the end of results.")
                    break
            except Exception:
                print("No next page button found.")
                break
        last_height = new_height

    driver.quit()
    
    print(f"Total links collected: {len(job_links)}")
    return list(job_links)

def save_to_csv(links, filename):
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_url'])
        for link in links:
            writer.writerow([link])
    print(f"Saved to {filename}")

if __name__ == "__main__":
    links = collect_rozee_links(search_query="Software Engineer", max_links=30)
    save_to_csv(links, str(BASE_DIR / "data" / "raw" / "job_links.csv"))
