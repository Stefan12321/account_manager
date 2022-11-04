import threading

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import random
import string
import re
from random import randint
# from logger import setup_logger

class GoogleSheet:
    def __init__(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        self.CREDENTIALS_FILE = 'autoreg/long-axle-300911-206a7e12084a.json'

    def write_data(self, range_, Data):


        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])  # Читаем ключи из файла

        httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
        service = googleapiclient.discovery.build('sheets', 'v4',
                                                  http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

          # сохраняем идентификатор файла

        service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
            "valueInputOption": "USER_ENTERED",
            # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {
                    "range": range_,
                    "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                    "values": [Data],
                }
            ]
        }).execute()

    def read_data(self, Number):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])  # Читаем ключи из файла

        httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
        service = googleapiclient.discovery.build('sheets', 'v4',
                                                  http=httpAuth)  # Выбираем работу с таблицами и 4 версию API


        results = service.spreadsheets().values().batchGet(spreadsheetId=self.spreadsheetId,
                                                           ranges=Number,
                                                           valueRenderOption='FORMATTED_VALUE',
                                                           dateTimeRenderOption='FORMATTED_STRING').execute()
        print(results)
        sheet_values = results['valueRanges'][0]['values']

        return sheet_values

    def paint(self, line, color):
        line = int(line)
        if color == 'orange':
            red = 1
            green = 0.5
            blue = 0
        elif color == 'red':
            red = 1
            green = 0
            blue = 0
        elif color == 'white':
            red = 1
            green = 1
            blue = 1
        elif color == 'green':
            red = 0
            green = 1
            blue = 0
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])  # Читаем ключи из файла

        httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
        service = googleapiclient.discovery.build('sheets', 'v4',
                                                  http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

        # сохраняем идентификатор файла
        # a = {"userEnteredFormat": {"backgroundColor": {"red": 1}}}
        body = {
            "requests": [{
                "updateCells": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": line - 1,
                        "endRowIndex": line,
                        "startColumnIndex": 0,
                        "endColumnIndex": 15
                    },
                    "rows": [{
                        "values": [{"userEnteredFormat": {"backgroundColor": {'red': red, 'green': green, 'blue': blue}}} for i in range(15)]
                    }],
                    "fields": "userEnteredFormat.backgroundColor"
                }
            }]
        }
        res = service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body).execute()



if __name__ == '__main__':
    pass
