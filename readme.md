# Flipkart Web Scraping Project

This is a small project to explore how web scraping works using two different approaches:
- `requests` + `BeautifulSoup`
- `Selenium`

## Setup

Install the required dependencies using:

```bash
pip install -r requirements.txt
```
## Files

### `scrapper_flipkart.py`

This script uses:

- `requests` to send HTTP requests  
- `BeautifulSoup` to parse and extract data from HTML

###`selenium_scrapper.py`

This script uses:

- `Selenium` WebDriver to render and interact with the webpage before extracting data
