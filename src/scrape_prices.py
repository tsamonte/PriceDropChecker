import ProjectConfigs
import requests
import bs4

def _get_soup(link: str) -> bs4.BeautifulSoup | None:
    headers = ({'User-Agent': ProjectConfigs.configs['scrapeConfigs']['userAgent'],
                'Accept-Language': ProjectConfigs.configs['scrapeConfigs']['acceptLang']})

    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "lxml")
        return soup
    except Exception as exc:
        print(f"There was an issue trying to download the web page ({link}):\n{exc}")
        return None

def get_data_amazon(link: str):
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

    return data

# TODO: delete
def test_scrape(link: str):
    soup = _get_soup(link)

    prices = soup.select('.priceToPay')

    return [price.getText() for price in prices]
