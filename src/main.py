import ProjectConfigs
import readCSV
import scrape_prices
import price_check
import EmailHandler

import csv

def sandbox():
    # test_link = "https://www.amazon.com/dp/B09VFTVNQ5?ref_=cm_sw_r_cp_ud_dp_1NGYB923GHB018KAYZN9"  # hat
    # test_link = "https://www.amazon.com/dp/B0C6RKLQHZ?_encoding=UTF8&psc=1&ref_=cm_sw_r_cp_ud_dp_78G370MFM6PWSGWBRBM9"  # GoPro
    # test_link = "https://www.amazon.com/dp/B00A7YV51C?_encoding=UTF8&psc=1&ref_=cm_sw_r_cp_ud_dp_8J53P82FNM2KEQ8TR2B4" # Divider
    # print(scrape_prices.get_data_amazon(test_link))
    # print(scrape_prices.test_scrape(test_link))
    # scrape_prices.get_data_amazon(test_link)

    test_vals = [[1,2,3],
                 [4,5,6],
                 [7,8,9]]

    # with open(".\\data\\test.csv", mode='r', encoding='utf-8') as f:
        # writer = csv.writer(f, lineterminator='\n')
        # writer.writerows(test_vals)
        # reader = csv.reader(f)
        # print(list(reader))

    ProjectConfigs.initialize()
    print(ProjectConfigs.configs)

    print(readCSV.open_csv())

def main():
    # Initialize project configurations from config.yaml file
    ProjectConfigs.initialize()

    # Attempt email login to ensure valid credentials were provided
    EmailHandler.test_login()

    # Retrieve data from csv
    data = readCSV.open_csv()

    # Edit data retrieved from csv
    price_check.edit_data(data)

    # Update csv with the edited data
    readCSV.update_csv(data)


if __name__ == '__main__':
    # main()
    sandbox()
