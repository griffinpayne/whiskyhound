# WhiskyHound

WhiskyHound is a Whiskey Auction Price Scraper tailored for [Whisky Auctioneer](https://www.whiskyauctioneer.com/). It allows users to fetch auction lot URLs based on their whisky brand of interest and optionally, a specific bottling. Once the URLs are fetched, it then scrapes each auction URL to retrieve the winning bid.

If you're running this scraper frequently or for extended periods, it's recommended to use a VPN to avoid potential IP blocks.

## Features

- Fetches auction lot URLs based on specified whisky brand and bottling.
- Multi-threaded scraping for improved efficiency.
- Option to save the results in a CSV file.
- Built-in retry mechanism for increased robustness.

## Prerequisites

Before you begin, ensure you have installed:

- [Python 3.8](https://www.python.org/downloads/) or later.
- [Firefox WebDriver](https://github.com/mozilla/geckodriver/releases) in your system's PATH or in the directory of the script.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/griffinpayne/whiskyhound.git
cd whiskyhound
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python whiskyhound.py
```

2. Follow the on-screen prompts:
- Enter the whisky brand you're interested in.
- Optionally, enter a specific bottling.
3. If prompted, decide whether to save the results in a CSV file and provide the desired filename.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## Upcoming
I plan to incorporate Whisky Hammer into this too, but one thing at a time. 

## License

[GNU](https://www.gnu.org/licenses/gpl-3.0.en.html)

