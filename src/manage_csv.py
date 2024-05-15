import ProjectConfigs
import csv
from CustomLogger import logger

def open_csv() -> [dict]:
    """
    Reads the csv data and returns the data as a Python object
    :return: A list of dictionaries representing each row from the csv file
    """
    try:
        csv_file = open(ProjectConfigs.configs['csvConfigs']['filePath'], encoding='utf-8')
        logger.info(f"Opened csv file ({ProjectConfigs.configs['csvConfigs']['filePath']})")
        reader = csv.DictReader(csv_file)
        data = list(reader)
        csv_file.close()
        return data
    # If the file is not in expected path, we should end program
    except FileNotFoundError:
        logger.error(f"csv file not found at specified path: \"{ProjectConfigs.configs['csvConfigs']['filePath']}\"")
        raise


def update_csv(data: [dict]):
    """
    Updates the csv with the new data
    :param data: A 2-d list representing the data to place in the csv file
    """
    fields = ProjectConfigs.configs['csvConfigs']['fieldNames']
    try:
        csv_file = open(ProjectConfigs.configs['csvConfigs']['filePath'], mode='w', encoding='utf-8')
        writer = csv.DictWriter(csv_file, fieldnames=fields, lineterminator='\n')

        # First write all the field names at the top of the csv
        writer.writerow({field: field for field in fields})

        # Write the data starting from the second row of the csv
        writer.writerows(data)
        csv_file.close()
        logger.info(f"Updated data in the csv file ({ProjectConfigs.configs['csvConfigs']['filePath']})")
    # An error when writing to the csv should not end the program
    except PermissionError:
        logger.error(f"Permission denied trying to write to the file at \"{ProjectConfigs.configs['csvConfigs']['filePath']}\"."
                     "\n\tEnsure the file is not being used by any other program and that you have permission to write to it.")
    except Exception as e:
        logger.error(f"There was an error trying to update the csv:\n\t{e}")
