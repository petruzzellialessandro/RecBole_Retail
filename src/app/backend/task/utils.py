import os
import re
from datetime import datetime

def find_latest_model(directory: str, prefix: str) -> str:
    regex_pattern = rf"{prefix}-([A-Za-z]+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)\.pth"
    latest_file = None
    latest_time = None

    for file in os.listdir(directory):
        match = re.match(regex_pattern, file, re.IGNORECASE)
        if match:
            month_str, day, year, hour, minute, second = match.groups()
            datetime_str = f"{day} {month_str} {year} {hour}:{minute}:{second}"
            try:
                file_time = datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S')
            except ValueError as e:
                print(f"Something went wrong during model file name conversion {file}: {e}")
                continue

            if latest_time is None or file_time > latest_time:
                latest_file = file
                latest_time = file_time

    return os.path.join(directory, latest_file)