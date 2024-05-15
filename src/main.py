import ProjectConfigs
import manage_csv
import price_check
import email_handler
import sys
import schedule
import time
from CustomLogger import logger

def initialize_app():
    # Initialize project configurations from config.yaml file
    ProjectConfigs.initialize()

    # Attempt email login to ensure valid credentials were provided
    email_handler.test_login()

def run_app():
    # Check if log file should be changed and update if needed
    logger.change_logfile()

    # Retrieve data from csv
    data = manage_csv.open_csv()

    # Edit data retrieved from csv
    price_check.notify_price_drops(data)

    # Update csv with the edited data
    manage_csv.update_csv(data)

def main():
    initialize_app()

    # if cmd argument "persist" was passed, run price check logic every 2 hours
    if len(sys.argv) >= 2 and sys.argv[1] == 'persist':
        schedule.every(2).hours.do(run_app)

        try:
            print("Running application. Press CTRL+C to exit.")
            while True:
                schedule.run_pending()
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit) as end:
            logger.info(f"Program ended ({end})")

    # if cmd argument "persist" wasn't passed, only run once
    else:
        run_app()


if __name__ == '__main__':
    main()
