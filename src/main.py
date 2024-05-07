import ProjectConfigs
import readCSV
import price_check
import EmailHandler

def main():
    # Initialize project configurations from config.yaml file
    ProjectConfigs.initialize()

    # Attempt email login to ensure valid credentials were provided
    EmailHandler.test_login()

    # Retrieve data from csv
    data = readCSV.open_csv()

    # Edit data retrieved from csv
    price_check.notify_price_drops(data)

    # Update csv with the edited data
    readCSV.update_csv(data)


if __name__ == '__main__':
    main()
