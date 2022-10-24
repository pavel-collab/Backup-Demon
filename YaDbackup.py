import yadisk
import os
from datetime import datetime
import json
import time

import YD_API

DEBUG = True
dir_location = os.path.abspath(__file__).replace(os.path.basename(__file__), '')

def parse_json(config_name: str):
    with open(config_name, 'r') as config_file:
            info = config_file.read()

    JsonData = json.loads(info)
    return JsonData

def CleanBackups(y_disk, path, log_file_name, saved_copies_amount=5):
    '''
    If we want to contain on the remoute server only N (for example 8) copies 
    '''

    # this is an array of objects
    Info = YD_API.YD_GetDirInfo(y_disk, path)
    # 5 copies + log file
    if len(Info) > saved_copies_amount+1:
        dates = {}
        for obj in Info:
            if obj['name'] != log_file_name:
                dates[time.strptime(datetime.strftime(obj['created'], "%d.%m.%Y-%H.%M.%S"), "%d.%m.%Y-%H.%M.%S")] = obj
        
        the_oldest_backup = min(dates.keys())

        for item in list(dates.items()):
            if item[0] == the_oldest_backup:
                the_oldest_obj = item[1]
                break

        y_disk.remove(the_oldest_obj['path'])

        return the_oldest_obj['name'], the_oldest_obj['path']
    return None

def EditLog(y_disk, path_to_log_remoute, path_to_log_local, log_file_name, info):

    if YD_API.YD_FindObj(y_disk, path_to_log_remoute, log_file_name):
        y_disk.remove(path_to_log_remoute+log_file_name, permanently=True)

    with open(path_to_log_local+log_file_name, 'a') as readme_f:
        readme_f.write(info + '\n')
    
    y_disk.upload(path_to_log_local+log_file_name, path_to_log_remoute+log_file_name)

def backup(y_disk, path, config_name):

    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    # date = datetime.strftime(datetime.now(), "%d.%m.%Y")
    
    JsonData = parse_json(config_name)
    remote_backup_dir = JsonData['remout_backup_dir']
    log_file_name = JsonData['log_file_name']

    log = open(dir_location + log_file_name, 'a')

    if YD_API.YD_FindObj(y_disk, remote_backup_dir, f'{date}'):
        log.write('[-] Sorry, such backup is already existed')
        if DEBUG: print('[-] Sorry, such backup is already existed')
        return
    
    y_disk.mkdir(f'{remote_backup_dir}{date}')

    for address, dirs, files in os.walk(path):
        for dir in dirs:
            y_disk.mkdir(f'{remote_backup_dir}{date}/{dir}')
            log.write(f'[+] The folder {dir} has been created\n')
            if DEBUG: print(f'[+] The folder {dir} has been created')
        for file in files:
            intermediate_path = address[len(path):]
            if intermediate_path != '': intermediate_path += '/'

            y_disk.upload(f'{address}/{file}', f'{remote_backup_dir}{date}/{intermediate_path}{file}')
            log.write(f'[+] The file {file} has been uploaded\n')
            if DEBUG: print(f'[+] The file {file} has been uploaded')

    log.close()
    
    info = f"\
            {date}\n\
            [+] The backup was done successful\n\
            {'='*100}\
            "

    rm_backup_result = CleanBackups(y_disk, remote_backup_dir, log_file_name)

    if rm_backup_result != None:
        if DEBUG: print(f"[+] backup [{rm_backup_result[0]}] was removed from [{rm_backup_result[1]}]")
        info = info + f"\n\
                        [+] backup [{rm_backup_result[0]}]\
                        was removed from\
                        [{rm_backup_result[1]}]\
                        \n"

    EditLog(y_disk, remote_backup_dir, dir_location, log_file_name, info)
    
    if DEBUG: print(f'[+] Backup has been successful compleated! [{date}]')