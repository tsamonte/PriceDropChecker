import yaml
import getpass
from error.ConfigurationException import ConfigurationException
from CustomLogger import logger

configs = {}

def _field_exists(parent: str, field_name: str) -> bool:
    """
    Checks if the specified field was provided in the configuration.yaml
    :param parent: Parent yaml key
    :param field_name: Key of value in question
    :return: True if field exists, False if not
    """
    global configs

    return field_name in configs[parent] and configs[parent][field_name] is not None

def _validate_required_field(parent: str, field_name: str, type_name: type = None) -> None:
    """
    Checks if a required field was provided in the configuration.yaml
    If type_name parameter is passed, also checks if the value matches the expected type
    :raises ConfigurationException: if required field was not provided or unexpected value type is provided
    :param parent: Parent yaml key
    :param field_name: The key name of the required yaml value
    :param type_name: The expected type for the value
    """
    global configs

    if not _field_exists(parent, field_name):
        raise ConfigurationException(f"config.yaml: The field \"{parent}.{field_name}\" is missing")

    if type_name is not None and type(configs[parent][field_name]) is not type_name:
        raise ConfigurationException(f"config.yaml: The field \"{parent}.{field_name}\" must be of type {type_name}")

def initialize() -> None:
    """
    Initialize the project configurations using the config.yaml file
    Should only be called once at the beginning of run time
    """
    global configs

    try:
        logger.info("Setting project configs from config.yaml")
        with open('config.yaml') as f:
            configs = yaml.safe_load(f)

        # -------------------- Validate Email Configs --------------------
        if 'emailConfigs' in configs:
            # validate smtpHost (required)
            _validate_required_field('emailConfigs', 'smtpHost', str)
            logger.info(f"Setting SMTP host to: {configs['emailConfigs']['smtpHost']}")

            # validate smtpPort (required)
            _validate_required_field('emailConfigs', 'smtpPort', int)
            logger.info(f"Setting SMTP port to: {configs['emailConfigs']['smtpPort']}")

            # validate sender email (optional)
            # If not provided, allow user to enter in console
            if not _field_exists('emailConfigs', 'senderEmail'):
                print("No sender email provided. Please enter the sender email")
                while True:
                    email = input("\tEnter email: ")
                    # TODO: user input for email in loop. Validate email syntax and break when valid email provided
                    break
                configs['emailConfigs']['senderEmail'] = email
            logger.info(f"Setting sender email to: {configs['emailConfigs']['senderEmail']}")

            # validate email app password (optional)
            # If not provided, allow user to enter in console
            if not _field_exists('emailConfigs', 'password'):
                print("No app password provided. Please enter the app password")
                configs['emailConfigs']['password'] = getpass.getpass("\tEnter password: ")
            logger.info("Email app password set")

            # validate receiver email (optional)
            # If not provided, set receiver email to be same as sender email
            if not _field_exists('emailConfigs', 'receiverEmail'):
                print("No receiver email provided. Setting receiver email to the same value as sender email")
                configs['emailConfigs']['receiverEmail'] = configs['emailConfigs']['senderEmail']
            logger.info(f"Setting receiver email to: {configs['emailConfigs']['receiverEmail']}")

        # if 'emailConfigs' field is missing
        else:
            raise ConfigurationException("config.yaml: The field \"emailConfigs\" is missing")

        # -------------------- Validate csv Configs --------------------
        if 'csvConfigs' in configs:
            # validate file name (required)
            _validate_required_field('csvConfigs', 'filePath')
            logger.info(f"Setting csv file path to: {configs['csvConfigs']['filePath']}")

            # validate field names (required)
            _validate_required_field('csvConfigs', 'fieldNames', list)
            logger.info(f"Setting csv column names to: {configs['csvConfigs']['fieldNames']}")

        # if 'csvConfigs' field is missing
        else:
            raise ConfigurationException("config.yaml: The field \"csvConfigs\" is missing")

        # -------------------- Validate Web Scraper Configs --------------------
        if 'scrapeConfigs' in configs:
            # validate user agent (optional)
            # if not provided, set a default user agent
            if not _field_exists('scrapeConfigs', 'userAgent'):
                print("User agent was not provided. Setting user agent to default value")
                configs['scrapeConfigs']['userAgent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
            logger.info(f"Setting user agent to: \"{configs['scrapeConfigs']['userAgent']}\"")

            # validate accept language (optional)
            if not _field_exists('scrapeConfigs', 'acceptLang'):
                print("Accept-language field was not provided. Setting accept language to default value")
                configs['scrapeConfigs']['acceptLang'] = "en-US, en;q=0.5"
            logger.info(f"Setting accept-language to: {configs['scrapeConfigs']['acceptLang']}")

        # if 'scrapeConfigs' field is missing
        # Note that scrapeConfigs and its child fields are optional, so no exception is raised
        else:
            # add scrapeConfigs to configs dict for default values
            configs['scrapeConfigs'] = {}
            # set default user agent
            print("User agent was not provided. Setting user agent to default value")
            configs['scrapeConfigs']['userAgent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
            logger.info(f"Setting user agent to: \"{configs['scrapeConfigs']['userAgent']}\"")

            # set default accept-language
            print("Accept-language field was not provided. Setting accept language to default value")
            configs['scrapeConfigs']['acceptLang'] = "en-US, en;q=0.5"
            logger.info(f"Setting accept-language to: \"{configs['scrapeConfigs']['acceptLang']}\"")

    # Error handling: Catch and rethrow any exceptions
    # Since everything in this module is run at beginning of project, any exceptions here should end program
    except FileNotFoundError as fnf:
        logger.error(f"config.yaml file not found. Please add a config.yaml file in the root\nException:\n{fnf}")
        raise
    except yaml.YAMLError as yaml_err:
        logger.error(f"An invalid yaml file was provided.\nException:\n\t{yaml_err}")
        raise
    except ConfigurationException as ce:
        logger.error(f"Invalid or missing values detected during project initialization:\n\t{ce}")
        raise
    except Exception as e:
        logger.error(f"An error occurred during project initialization:\n\t{e}")
        raise
