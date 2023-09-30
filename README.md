# WhiskyHound

WhiskyHound is a whisky auction price scraper tailored for [Whisky Auctioneer](https://www.whiskyauctioneer.com/). It allows users to search and retrieve the winning bid prices for a specified whisky (or brand, bottles, etc., by adding OR between search terms) from the search results efficiently, eliminating the need to navigate to each auction lot URL individually.

## Features

- Retrieves winning bids, brand, bottling, ending date, and URLs directly from the search results based on specified criteria, allowing for comprehensive price analysis easily.
- Displays a graphical representation of the average price of each bottling over time using Matplotlib and Plotly.
- Provides an option to output the scraped results to an Excel file with structured columns for Brand, Bottling, URL, End Date, and Price.
- Multi-threaded scraping optimizes the retrieval process.
- Implements a retry mechanism to enhance robustness.

## Prerequisites

Ensure you have:
- [Python 3.8](https://www.python.org/downloads/) or later installed.
- [Firefox WebDriver](https://github.com/mozilla/geckodriver/releases) added to your system's PATH or placed in the script's directory.
- A VPN is recommended to avoid any potential IP blocks when running the scraper for extended periods or frequently.

## Installation

1. Clone the repository:
```sh
git clone https://github.com/griffinpayne/whiskyhound.git
cd whiskyhound
```

2. Install the required dependencies:
```sh
pip install -r requirements.txt
```

## Usage

1. Run the script:
```sh
python whiskyhound.py
```

2. Follow the on-screen prompts to enter the whisky you're interested in.
3. Name the Excel file to save the search results.

## Contributing

Pull requests are welcome. For substantial changes, please open an issue first to discuss what you would like to change.

## Upcoming

The incorporation of Whisky Hammer is in the pipeline, progressing one step at a time.

## License

[GNU](https://www.gnu.org/licenses/gpl-3.0.en.html)