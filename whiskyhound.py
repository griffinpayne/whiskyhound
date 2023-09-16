import re
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()

def fetch_sitemap_urls(base_url, max_page):
    all_urls = []
    
    def extract_urls(content):
        soup = BeautifulSoup(content, 'xml')
        return [url.text for url in soup.find_all('loc')]
      
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(session.get, f"{base_url}?page={page}") for page in range(1, max_page+1)]
        for future in futures:
            content = future.result().content
            urls = extract_urls(content)
            all_urls.extend([url for url in urls if '/lot/' in url])
            
    return all_urls

def fetch_winning_bid(url, brand_pattern, bottling_pattern):
    if not re.search(brand_pattern, url, re.IGNORECASE) or (bottling_pattern and not re.search(bottling_pattern, url, re.IGNORECASE)):
        return
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    with webdriver.Firefox(options=options) as driver:
        try:
            driver.get(url)
            lot_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#new-layout div.place-bid.bid-section.bid-info span'))
            )
            return (url, lot_element.text)
        except Exception as e:
            print(f"No winning bid found for {url}. Exception: {e}")

def prompt_to_output_to_csv():
    csv_output = input("Do you want to output the results to a CSV file? (y/n) ")
    if csv_output.lower() == "y":
        csv_filename = input("Enter the name of the CSV file: ")
        return csv_filename
    else:
        return None

def main():
    brand = input("Enter the whisky brand you're interested in: ").replace('*', '.*')
    bottling = input("Enter the specific bottling (optional, press Enter to skip): ").replace('*', '.*')
    
    sitemap_url = 'https://whiskyauctioneer.com/sitemap.xml'
    auction_urls = fetch_sitemap_urls(sitemap_url, 618)
    filtered_urls = [url for url in auction_urls if re.search(brand, url, re.IGNORECASE)]
    if bottling:
        filtered_urls = [url for url in filtered_urls if re.search(bottling, url, re.IGNORECASE)]
    
    print(f"Filtered to {len(filtered_urls)} auction lot URLs.")
    
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_winning_bid, url, brand, bottling) for url in filtered_urls]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
                
    print("Scraping complete.")
    
    csv_filename = prompt_to_output_to_csv()
    if csv_filename:
        with open(csv_filename, "w", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for result in results:
                csv_writer.writerow(result)

if __name__ == "__main__":
    main()
