import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def extract_brand_bottling(url):
    try:
        parts = url.split('/')
        brand_part = parts[5].split('-')[0]
        last_part = parts[-1]
        bottling_parts = last_part.split('-')[1:]
        bottling = ' '.join(bottling_parts)
    except IndexError:
        brand_part = ''
        bottling = ''
    return brand_part, bottling

def fetch_winning_bids(base_url, brand):
    results = []
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    with webdriver.Firefox(options=options) as driver:
        try:
            search_url = f"{base_url}?text={brand}&sort=field_reference_field_end_date+DESC&items_per_page=500"
            driver.get(search_url)
            total_lots_element = driver.find_element(By.CSS_SELECTOR, 'p.left')
            total_lots_text = total_lots_element.text
            total_lots = int(re.search(r'\d+', total_lots_text).group(0))
            
            for i in range(1, total_lots + 1):
                try:
                    bid_selector = f'div.views-row:nth-child({i}) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2)'
                    bid_info = driver.find_element(By.CSS_SELECTOR, bid_selector).text
                    
                    url_selector = f'div.views-row:nth-child({i}) a'
                    url = driver.find_element(By.CSS_SELECTOR, url_selector).get_attribute('href')
                    
                    brand, bottling = extract_brand_bottling(url)
                    results.append({
                        'brand': brand,
                        'bottling': bottling,
                        'bid_info': bid_info,
                        'url': url
                    })
                    
                except NoSuchElementException:
                    print(f"Element not found for index {i}")
                    
        except Exception as e:
            print(f"Failed to process the page. Exception: {e}")
    return results

def main():
    brand = input("Enter the whisky you're interested in: ").replace(' ', '+')
    base_url = 'https://whiskyauctioneer.com/auction-search'
    
    results = fetch_winning_bids(base_url, brand)
    print("Scraping complete.")
    
    csv_filename = input("Enter the name of the CSV file to save the results: ")
    if csv_filename:
        with open(csv_filename, "w", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Brand', 'Bottling', 'Winning Bid', 'URL'])
            for result in results:
                csv_writer.writerow([result['brand'], result['bottling'], result['bid_info'], result['url']])
                
if __name__ == "__main__":
    main()
