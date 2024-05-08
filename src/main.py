import ProjectConfigs
import manage_csv
import price_check
import email_handler

def main():
    # Initialize project configurations from config.yaml file
    ProjectConfigs.initialize()

    # Attempt email login to ensure valid credentials were provided
    email_handler.test_login()

    # Retrieve data from csv
    data = manage_csv.open_csv()

    # Edit data retrieved from csv
    price_check.notify_price_drops(data)

    # Update csv with the edited data
    manage_csv.update_csv(data)


if __name__ == '__main__':
    main()
