import re
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading

def fetch_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')
    urls = [url.text for url in soup.find_all('loc') if '/lot/' in url.text]
    return urls

def fetch_winning_bid(url, brand_pattern, bottling_pattern):
    if not re.search(brand_pattern, url, re.IGNORECASE) or (bottling_pattern and not re.search(bottling_pattern, url, re.IGNORECASE)):
        return
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    
    try:
        driver.get(url)
        lot_element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.winning-bid-css-selector'))  # Replace with the actual CSS selector
        )
        for element in lot_element:
            print(f"Winning bid for {url}: {element.text}")
    except Exception as e:
        print(f"No winning bid found for {url}. Exception: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    brand = input("Enter the whisky brand you're interested in: ").replace('*', '.*')
    bottling = input("Enter the specific bottling (optional, press Enter to skip): ").replace('*', '.*')
    
    sitemap_url = 'https://whiskyauctioneer.com/sitemap.xml?page=1'  # Example page, you can loop through different pages
    auction_urls = fetch_sitemap_urls(sitemap_url)
    print(f"Fetched {len(auction_urls)} auction URLs. Filtering by brand: {brand}")

    filtered_urls = [url for url in auction_urls if re.search(brand, url, re.IGNORECASE)]
    if bottling:
        filtered_urls = [url for url in filtered_urls if re.search(bottling, url, re.IGNORECASE)]
    print(f"Filtered to {len(filtered_urls)} auction lot URLs.")

    # Using threads to fetch winning bids
    thread_list = []
    for url in filtered_urls:
        thread = threading.Thread(target=fetch_winning_bid, args=(url, brand, bottling))
        thread.start()
        thread_list.append(thread)
        time.sleep(0.2)  # Introduce a small delay to avoid overwhelming the server

    # Wait for all threads to complete
    for thread in thread_list:
        thread.join()

    print("Scraping complete.")
