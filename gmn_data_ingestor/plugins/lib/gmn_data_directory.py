from datetime import datetime
from typing import List
import requests
from bs4 import BeautifulSoup

GMN_DATA_DIRECTORY_BASE_URL = 'https://globalmeteornetwork.org/data/traj_summary_data/'
GMN_DATA_START_DATE = datetime(2022, 1, 9)


class GMNDataDirectory():
    def __init__(self, base_url: str = GMN_DATA_DIRECTORY_BASE_URL):
        self.base_url = base_url

    def get_all_daily_filenames(self) -> List[str]:
        return _get_url_paths(self.base_url + 'daily/', 'txt')

    def get_all_monthly_files(self) -> List[str]:
        pass

    def get_daily_file_url_by_date(self, date: datetime, current_date: datetime) -> str:
        if date == current_date:
            return self.base_url + 'daily/traj_summary_latest_daily.txt'

        if date.day == current_date.day - 1:
            return self.base_url + 'daily/traj_summary_yesterday.txt'

        all_daily_filenames = self.get_all_daily_filenames()
        files_containing_date = [f for f in all_daily_filenames if date.strftime('%Y%m%d') in f]
        return files_containing_date[0]

    def get_month_file_url_by_month(self, date: datetime, current_date: datetime) -> str:
        pass

    def get_daily_file_content_by_date(self, date: datetime, current_date: datetime) -> str:
        file_url = self.get_daily_file_url_by_date(date, current_date)

        response = requests.get(file_url)
        if response.ok:
            return response.text
        else:
            raise response.raise_for_status()


def _get_url_paths(url: str, ext: str = '') -> List[str]:
    response = requests.get(url)
    if response.ok:
        response_text = response.text
    else:
        raise response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    return parent
