import os, datetime


def save_extracted_data_file(extracted_data_directory: str, target_date: datetime, logical_date: datetime,
                             execution_date: datetime, file_content: str) -> str:
    execution_date_extracted_data_directory = os.path.join(os.path.expanduser(extracted_data_directory),
                                                           execution_date.strftime('%Y%m%d'))
    os.makedirs(execution_date_extracted_data_directory, exist_ok=True)
    filename = f"target_{target_date}_logical_{logical_date}_execution_{execution_date}.txt" + ".{}"
    file_path = os.path.join(execution_date_extracted_data_directory, filename)
    counter = 0
    while os.path.isfile(file_path.format(counter)):
        counter += 1
    file = open(file_path.format(counter), "w")
    file.write(file_content)
    file.close()

    return file_path.format(counter)
