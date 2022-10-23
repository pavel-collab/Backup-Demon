import yadisk
import os
from datetime import datetime
import json

import YD_API

# log_file_name = 'info.txt'
# remote_backup_dir = '/test_backup/'

def parse_json(config_name: str):
    with open(config_name, 'r') as config_file:
            info = config_file.read()

    JsonData = json.loads(info)
    return JsonData

def EditLog(y_disk, path_to_log, log_file_name, info):

    if YD_API.YD_FindObj(y_disk, path_to_log, log_file_name):
        y_disk.remove(path_to_log+log_file_name, permanently=True)

    with open(log_file_name, 'a') as readme_f:
        readme_f.write(info + '\n')
    
    y_disk.upload(log_file_name, path_to_log+log_file_name)

def backup(y_disk, path, config_name):
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    # date = datetime.strftime(datetime.now(), "%d.%m.%Y")
    
    JsonData = parse_json(config_name)
    remote_backup_dir = JsonData['remout_backup_dir']
    log_file_name = JsonData['log_file_name']

    if YD_API.YD_FindObj(y_disk, remote_backup_dir, f'{date}'):
        print('[-] Sorry, such backup is already existed')
        return
    
    y_disk.mkdir(f'{remote_backup_dir}{date}')

    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y_disk.mkdir(f'{remote_backup_dir}{date}/{dir}')
            print(f'[+] The folder {dir} has been created')
        for file in files:
            intermediate_path = address[len(path):]
            if intermediate_path != '': intermediate_path += '/'

            # print(f'/test_backup/{date}/{intermediate_path}{file}')
            y_disk.upload(f'{address}/{file}', f'{remote_backup_dir}{date}/{intermediate_path}{file}')
            print(f'[+] The file {file} has been uploaded')

    info = f"\
            {date}\n\
            [+] The backup was done successful\n\
            {'='*100}\
            "
    EditLog(y_disk, remote_backup_dir, log_file_name, info)
    
    print(f'[+] Backup has been successful compleated! [{date}]')