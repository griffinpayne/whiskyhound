# WhiskyHound

WhiskyHound is a whisky auction price scraper tailored for [Whisky Auctioneer](https://www.whiskyauctioneer.com/). It provides users with the ability to efficiently search and retrieve the winning bid prices for a specified whisky whisky (or brand, bottles, etc., just add OR between search terms) from the search results, without having to navigate to each auction lot URL individually.

To avoid any potential IP blocks when running this scraper for extended periods or frequently, consider using a VPN.

## Features

- Retrieves the winning bids directly from the search results, based on the specified criteria, eliminating the need to navigate to each individual auction lot URL, allowing for price analysis easily.
- Extracts the brand and bottling details from the auction lot URLs for more structured and meaningful results.
- Multi-threaded scraping to optimize the retrieval process.
- Option to output the scraped results to a CSV file, with structured columns for Brand, Bottling, URL, and Price.
- Retry mechanism to enhance robustness.

## Prerequisites

Before starting, ensure you have:

- [Python 3.8](https://www.python.org/downloads/) or later.
- [Firefox WebDriver](https://github.com/mozilla/geckodriver/releases) added to your system's PATH or placed in the directory of the script.

## Installation

1. Clone the repository:
```
git clone https://github.com/griffinpayne/whiskyhound.git
cd whiskyhound
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Run the script:
```
python whiskyhound.py
```

2. Follow the on-screen prompts:
- Enter the whisky you're interested in.

3. Name the CSV file and specify to save the search results. 

## Contributing

Pull requests are welcome. For substantial changes, please open an issue first to discuss your proposed alterations.

## Upcoming

The incorporation of Whisky Hammer is in the pipeline—progressing one step at a time.

## License

[GNU](https://www.gnu.org/licenses/gpl-3.0.en.html)

This updated README provides clear and concise information about the improved functionalities and the updated process flow of your script.