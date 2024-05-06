import ProjectConfigs
import csv

def open_csv() -> [dict]:
    """
    Reads the csv data and returns the data as a Python object
    :return: A list of dictionaries representing each row from the csv file
    """
    try:
        csv_file = open(ProjectConfigs.configs['csvConfigs']['filePath'], encoding='utf-8')
        reader = csv.DictReader(csv_file)
        data = list(reader)
        csv_file.close()
        return data
    except FileNotFoundError:
        print("File Not Found")
        raise


def update_csv(data: [dict]):
    """
    Updates the csv with the new data
    :param data: A 2-d list representing the data to place in the csv file
    :return: Success code. 1 if successful, -1 if not
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
        return 1
    except FileNotFoundError:
        return -1
