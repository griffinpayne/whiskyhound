import re
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


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

    print("Hang tight, this might take a minute...")
    start_time = time.time()

    with webdriver.Firefox(options=options) as driver:
        page_num = 0
        while True:
            try:
                search_url = base_url
                if page_num > 0:
                    search_url += f"&page={page_num}"
                driver.get(search_url)

                elapsed_time = time.time() - start_time
                if 180 < elapsed_time <= 181:
                    print("I'm still looking up those bottles... calm down.")
                elif 300 < elapsed_time <= 301:
                    print("Quite a few bottles you're after, huh?")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.views-row'))
                )

                total_lots_element = driver.find_element(By.CSS_SELECTOR, 'p.left')
                total_lots_text = total_lots_element.text
                total_lots = int(re.search(r'\d+', total_lots_text).group(0))
                num_of_pages = -(-total_lots // 500)

                if total_lots == 0:
                    break

                for i in range(1, 501):  # Attempt to fetch up to 500 lots on the current page
                    if (page_num * 500) + i > total_lots:
                        break  # break out of the loop if the total number of elements is reached

                    try:
                        bid_selector = f'div.views-row:nth-child({i}) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2)'
                        bid_info = driver.find_element(By.CSS_SELECTOR, bid_selector).text

                        url_selector = f'div.views-row:nth-child({i}) a'
                        url = driver.find_element(By.CSS_SELECTOR, url_selector).get_attribute('href')

                        brand, bottling = extract_brand_bottling(url)

                        end_date_selector = f'div.views-row:nth-child({i}) > div:nth-child(3) > span:nth-child(1)'
                        end_date = driver.find_element(By.CSS_SELECTOR, end_date_selector).text

                        results.append({
                            'brand': brand,
                            'bottling': bottling,
                            'bid_info': bid_info,
                            'end_date': end_date,
                            'url': url
                        })
                    except NoSuchElementException:
                        print(f"Element not found for index {i}")

                if page_num >= num_of_pages - 1:
                    break

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, 'div.item-list:nth-child(4) > ul:nth-child(1) > li:nth-child(11) > a:nth-child(1)')
                    next_button.click()
                    page_num += 1
                except NoSuchElementException:
                    break  # Break if "Next" button is not found

            except TimeoutException:
                print("Timeout occurred while loading the page.")
                break
            except Exception as e:
                print(f"Failed to process the page. Exception: {e}")
                break

    return results


def main():
    brand = input("Enter the whisky you're interested in: ").replace(' ', '+')
    base_url = f'https://whiskyauctioneer.com/auction-search?text={brand}&sort=field_reference_field_end_date+DESC&items_per_page=500'

    results = fetch_winning_bids(base_url, brand)
    print("Scraping complete.")
    print(f"Found {len(results)} results.")

    csv_filename = input("Enter the name of the CSV file to save the results: ")
    if not csv_filename.endswith('.csv'):
        csv_filename += '.csv'
    with open(csv_filename, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Brand', 'Bottling', 'Price', 'End Date', 'URL'])
        for result in results:
            csv_writer.writerow([result['brand'], result['bottling'], result['bid_info'], result['end_date'], result['url']])


if __name__ == "__main__":
    main()

