from nbformat import read
import yadisk
import os
from datetime import datetime

with open('token', 'r') as Token:
    token = Token.read()

y = yadisk.YaDisk(token=token)
print(y.check_token()) # Проверим токен

# def run(path):
#     date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
#     y.mkdir(f'/test/{date}')

#     for address, dirs, files in os.walk(path):
#         for dir in dirs:
#             y.mkdir(f'/test/{date}/{dir}')
#             print(f'Папка {dir} создана')
#         for file in files:
#             print(f'Файл {file} загружен')
#             y.upload(f'{address}/{file}', f'/test/{date}/{file}')

# if __name__ == '__main__':
#     pass
#     # run(r'C:\folder\путь к папке для загрузки')