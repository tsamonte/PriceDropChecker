import ProjectConfigs
import requests
import bs4
from CustomLogger import logger

def _get_soup(link: str) -> bs4.BeautifulSoup | None:
    """
    Create a bs4.BeautifulSoup object using the passed in link
    :param link: Web page to be scraped
    :return: bs4.BeautifulSoup object for the product web page to be scraped
    """
    headers = ({'User-Agent': ProjectConfigs.configs['scrapeConfigs']['userAgent'],
                'Accept-Language': ProjectConfigs.configs['scrapeConfigs']['acceptLang']})

    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "lxml")
        return soup
    except Exception as exc:
        logger.warning(f"There was an issue trying to download the web page ({link}):\n\t{exc}")
        return None

def get_data_amazon(link: str) -> dict:
    """
    Scrapes the name and price of the product from the link.
    :param link: Web page to be scraped
    :return: A dict with keys "name" and "price" retrieved from the web page. Can be empty if invalid web page is provided
    """
    soup = _get_soup(link)

    # Data we want to retrieve from the web page
    data = {}

    if soup:
        # get the price, removing any leading/trailing whitespace and commas
        price_whole = soup.select('.priceToPay')
        if len(price_whole) > 0:
            data['price'] = price_whole[0].getText().strip().replace(',', '')

        # get the product name
        item_name = soup.select("#productTitle")
        if len(item_name) > 0:
            data['name'] = item_name[0].getText().strip()

    if len(data) > 0:
        logger.info(f"Data scraped from the web page ({link}):\n\t{data}")
    else:
        logger.info("Web page did not contain name/price data needed for this program")

    return data
