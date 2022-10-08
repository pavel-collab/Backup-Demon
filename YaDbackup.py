import yadisk
import os
from datetime import datetime

import YD_API



# y = yadisk.YaDisk(token=token)
# print(y.check_token()) # Проверим токен

def backup(y_disk, path):
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    
    if YD_API.YD_FindObj(y_disk, '/', '/backup/{date}'):
        print('[-] Sorry, such backup is already existed')
        return
    
    y_disk.mkdir(f'/backup/{date}')

    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y_disk.mkdir(f'/{dir}')
            print(f'[+] The folder {dir} has been created')
        for file in files:
            y_disk.upload(f'{address}/{file}', f'/{date}/{file}')
            print(f'[+] The file {file} has been uploaded')
    
    print('[+] Backup has been successful compleated! [{date}]')

if __name__ == '__main__':
    with open('token', 'r') as Token:
        token = Token.read()

    y = yadisk.YaDisk(token=token)

    # print(y.check_token()) # Проверим токен
    if y.check_token():
        print('[+] Success connection')
        backup(y, './test_dir')
    else:
        os._exit(1)