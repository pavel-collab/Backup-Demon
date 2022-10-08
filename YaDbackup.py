import yadisk
import os
from datetime import datetime

import YD_API



# y = yadisk.YaDisk(token=token)
# print(y.check_token()) # Проверим токен

def backup(y_disk, path):
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    # date = datetime.strftime(datetime.now(), "%d.%m.%Y")
    
    if YD_API.YD_FindObj(y_disk, '/test_backup', f'{date}'):
        print('[-] Sorry, such backup is already existed')
        return
    
    y_disk.mkdir(f'/test_backup/{date}')

    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y_disk.mkdir(f'/test_backup/{date}/{dir}')
            print(f'[+] The folder {dir} has been created')
        for file in files:
            intermediate_path = address[len(path):]
            if intermediate_path != '': intermediate_path += '/'

            # print(f'/test_backup/{date}/{intermediate_path}{file}')
            y_disk.upload(f'{address}/{file}', f'/test_backup/{date}/{intermediate_path}{file}')
            print(f'[+] The file {file} has been uploaded')
    
    print(f'[+] Backup has been successful compleated! [{date}]')

if __name__ == '__main__':
    with open('token', 'r') as Token:
        token = Token.read()

    y = yadisk.YaDisk(token=token)

    if y.check_token():
        print('[+] Success connection')
        backup(y, './test_dir/')
    else:
        os._exit(1)

    YD_API.YD_PrintDiskInfo(y)