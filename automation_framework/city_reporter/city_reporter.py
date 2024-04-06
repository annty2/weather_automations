import enum
from typing import Dict, List
import pandas as pd

ReportType = Dict[str, List[str]]


class Status(enum.Enum):
    SUCCESS = 'Success'
    API_NOT_FOUND = 'City not found in API'
    WEB_NOT_FOUND = 'City not found in web page'
    NOT_FOUND = 'City not found in web page and API'


class CityReporter:

    def __init__(self):
        self.report_data: ReportType = {
            'City': [],
            'API Temperature': [],
            'Website Temperature': [],
            'Temperature Difference': [],
            'Status': []
        }

    def append_to_report(self, city: str, api_temp: str, web_temp: str, temp_differ: str,
                         status: Status):
        self.report_data['City'].append(city)
        self.report_data['API Temperature'].append(api_temp)
        self.report_data['Website Temperature'].append(web_temp)
        self.report_data['Temperature Difference'].append(temp_differ)
        self.report_data['Status'].append(status.value)

    def save_report(self):
        df = pd.DataFrame(self.report_data)
        df.to_excel('../temperature_report.xlsx', index=False)
