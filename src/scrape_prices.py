import ProjectConfigs
import requests
import bs4


# def initialize_session() -> requests.Session:
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
#                'Accept-Language': 'en-US, en;q=0.5'}
#     session = requests.session()
#     session.headers.update(headers)
#     return session

def _get_soup(link: str) -> bs4.BeautifulSoup | None:
    headers = ({'User-Agent': ProjectConfigs.configs['scrapeConfigs']['userAgent'],
                'Accept-Language': ProjectConfigs.configs['scrapeConfigs']['acceptLang']})

    # Check for error response code
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "lxml")
        return soup
    except Exception as exc:
        print(f"There was an issue trying to download the web page ({link}):\n{exc}")
        return None

# def _get_soup_session(session: requests.Session, link: str):
#     response = session.get(link)
#     soup = bs4.BeautifulSoup(response.text, "lxml")
#     return soup

def get_data_amazon(link: str):
    soup = _get_soup(link)

    # Data we want to retrieve from the web page
    data = {}

    if soup:
        # get the price
        price_whole = soup.select('.priceToPay')

        if len(price_whole) > 0:
            data['price'] = price_whole[0].getText().strip().replace(',', '')

        # get the product name
        item_name = soup.select("#productTitle")
        if len(item_name) > 0:
            data['name'] = item_name[0].getText().strip()

    return data

def test_scrape(link: str):
    soup = _get_soup(link)

    prices = soup.select('.priceToPay')

    return [price.getText() for price in prices]


# def get_data_amazon_session(session: requests.Session, link: str):
#     soup = _get_soup_session(session, link)
#     price_whole = soup.select("span.reinventPricePriceToPayMargin:nth-child(3)")
#
#     if len(price_whole) > 0:
#         return price_whole[0].getText()
#     else:
#         return "NA"
