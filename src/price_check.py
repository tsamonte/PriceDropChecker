import scrape_prices
import email_handler

def _price_to_float(price_string: str) -> float:
    """
    Converts a price string to a float
    :param price_string: Price string with leading "$" symbol
    :return: Float of the passed in string
    """
    return float(price_string.strip('$'))

def _update_name(row: dict, scraped_data: dict) -> None:
    """
    Updates the name of the item if it is different from what is saved
    :param row: The row being checked and updated
    :param scraped_data: The new data scraped from the web page
    """
    if 'name' in scraped_data.keys() and scraped_data['name'] != row['ItemName']:
        row['ItemName'] = scraped_data['name']

def _update_prices(row: dict, scraped_data: dict) -> str:
    """
    Updates the price fields in the csv (StartingPrice, PreviousLow, AllTimeLow, and CurrentPrice) if needed
    :param row: The row being checked and updated
    :param scraped_data: The new data scraped from the web page
    :return: A message telling if the scraped price is low enough to be sent in the email. Can be empty
    """
    # Scenarios for email:
    #   - New price is lower than starting price and the previous low
    #   - New price is lower than all-time price
    # Scenarios for no email:
    #   - First time this item is being checked
    #   - New price is lower than starting price, but higher than the previous low
    #   - New price is higher than the starting price
    message = ""

    # handle starting price
    # If any of the price fields (starting price, previous low, or all-time low) are empty,
    # assume this is the first time we are seeing this item
    if len(row['StartingPrice']) == 0 or len(row['PreviousLow']) == 0 or len(row['AllTimeLow']) == 0:
        row['StartingPrice'] = scraped_data['price']
        row['PreviousLow'] = scraped_data['price']
        row['AllTimeLow'] = scraped_data['price']

    else:
        # If scraped price < starting price
        if _price_to_float(scraped_data['price']) < _price_to_float(row['StartingPrice']):
            # If scraped price is also LOWER than previous low, we want to add to email
            # Prevents email from being sent multiple times in a row on the same price
            if _price_to_float(scraped_data['price']) < _price_to_float(row['PreviousLow']):
                difference = _price_to_float(row['StartingPrice']) - _price_to_float(scraped_data['price'])
                message = f"&emsp;&emsp;The item is ${difference:.2f} less than when you added it to your list! Get it now for {scraped_data['price']}"
                row['PreviousLow'] = scraped_data['price']
            # If scraped price is also HIGHER than previous low, we don't want to add to email
            # But we should overwrite the stored previous low
            else:
                row['PreviousLow'] = scraped_data['price']

        # If scraped price < all-time low
        if _price_to_float(scraped_data['price']) < _price_to_float(row['AllTimeLow']):
            row['AllTimeLow'] = scraped_data['price']
            message = f"&emsp;&emsp;The item has reached an all-time low!<br>{message}"

    # always set current price to the newly retrieved price
    row['CurrentPrice'] = scraped_data['price']

    return message


def _update_data(csv_data: [dict]) -> str:
    """
    Takes data retrieved from the csv, scrapes the necessary data from the webpage,and performs any necessary updates
    :param csv_data: List of dict representing rows from the csv file
    :return: A message containing price drop alerts for any items. Can be empty.
    """
    msg_body = ""
    for row in csv_data:
        print(f"Checking row {row['ID']}")

        # Using the link, scrape the data we need
        scraped_data = scrape_prices.get_data_amazon(row['Link'])

        # Update the name
        if 'name' in scraped_data.keys():
            _update_name(row, scraped_data)

        # Update all the columns having to do with price
        if 'price' in scraped_data.keys():
            msg = _update_prices(row, scraped_data)
            if msg != "":
                msg_body += f"<p>Item Name - <a href=\"{row['Link']}\">{row['ItemName']}</a><br>{msg}</p><br>"

    return msg_body

def notify_price_drops(csv_data: [dict]) -> None:
    """
    Takes csv data and performs updates. Sends email notifications if a price drop is detected
    :param csv_data: List of dict representing rows from the csv file
    """
    msg_body = _update_data(csv_data)
    if msg_body != "":
        try:
            msg_body = f"<html><body>{msg_body}</body></html>"
            smtp = email_handler.login()
            email_handler.send_email(smtp, msg_body)
            smtp.quit()
            print("Price drop notification email sent")
        # In-depth error messages are logged within the above-called functions
        # Exceptions here should not end persistent program. Simply do not send email and continue running
        except:
            print("Email unable to be sent")
