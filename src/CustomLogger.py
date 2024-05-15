import logging
from datetime import date

class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        """
        Extends the built-in logging.Logger class to keep track of the current log filename.
        Logs will be rotated every month. The log for each month will be in the following format:
        "./log/<year>-<month>.log"
        """
        super().__init__(name, level)

        # Initialize and keep track of current log file name
        today = date.today()
        self.logfile = f"./log/{today.year}-{today.month}.log"

        # Create log Formatter, do not keep track
        log_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] {%(filename)s:%(lineno)d} - %(message)s", "%Y-%m-%d %H:%M:%S")

        # Initialize FileHandler for sending logs to file
        file_handler = logging.FileHandler(self.logfile)
        file_handler.setFormatter(log_formatter)

        # Initialize StreamHandler for sending logs to console as well
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)

        # Add both handlers to the internal handler list from parent class
        self.addHandler(console_handler)
        self.addHandler(file_handler)

    def _is_new_month(self) -> bool:
        """
        Checks if it is a new month/year compared to the current logfile
        :return: bool. True if it is a new month/year, False if not
        """
        today = date.today()
        new_log = f"./log/{today.year}-{today.month}.log"

        return new_log != self.logfile

    def change_logfile(self) -> None:
        """
        First checks if we need to change the log file (if it is a new month/year).
        If needed, sets the FileHandler to point to the new file.
        """
        if self._is_new_month():
            # FileHandler to remove from the logger
            to_remove = self.handlers[-1]

            # Create new FileHandler with the new file path
            today = date.today()
            file_handler = logging.FileHandler(f"./log/{today.year}-{today.month}.log")
            file_handler.setFormatter(to_remove.formatter)

            # remove old FileHandler and add new FileHandler
            self.removeHandler(to_remove)
            self.addHandler(file_handler)


logger = CustomLogger(__name__, logging.INFO)
