import ProjectConfigs
import scrape_prices
from smtplib import SMTPException

def _price_to_float(price_string: str) -> float:
    return float(price_string.strip('$'))

def update_name(row: dict, scraped_data: dict) -> None:
    """
    Updates the name of the item if it is different from what is saved
    :param row: The row being checked and updated
    :param scraped_data: The new data scraped from the web page
    :return: None
    """
    if 'name' in scraped_data.keys() and scraped_data['name'] != row['ItemName']:
        row['ItemName'] = scraped_data['name']

def update_prices(row: dict, scraped_data: dict):
    """
    Updates the price fields in the csv (StartingPrice, PreviousLow, AllTimeLow, and CurrentPrice) if needed
    :param row:
    :param scraped_data:
    :return:
    """
    # handle starting price
    # If this is the first time we are checking this item, initialize the starting price
    if len(row['StartingPrice']) == 0:
        row['StartingPrice'] = scraped_data['price']

    # handle the previous low
    # if len(row['PreviousLow']) == 0 or _price_to_float(row[5])
    # TODO: figure out how to handle previous low

    # handle All-Time-Low
    if len(row['AllTimeLow']) == 0 or _price_to_float(scraped_data['price']) < _price_to_float(row['AllTimeLow']):
        row['AllTimeLow'] = scraped_data['price']

    # always set current price to the newly retrieved price
    row['CurrentPrice'] = scraped_data['price']


def edit_data(csv_data: [dict]):
    for row in csv_data:
        print(f"Checking row {row['ID']}")

        # Using the link, scrape the data we need
        scraped_data = scrape_prices.get_data_amazon(row['Link'])

        # Update the name
        if 'name' in scraped_data.keys():
            update_name(row, scraped_data)

        # Update all the columns having to do with price
        if 'price' in scraped_data.keys():
            update_prices(row, scraped_data)
