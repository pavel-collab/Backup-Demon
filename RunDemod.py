#!/usr/bin/env python

import json
import schedule 
import time
import yadisk
from datetime import datetime
import sys
import os
from Demon import Daemon

import YD_API
import YaDbackup

#? что происходит, если время между отправками меньше времени бэкапа
#! При тестировании возникла ошибка -- косяк с именами. У info.txt есть локальное имя (полный путь) и имя на удаленном сервере.
#! Возникает ошибка при нахождении файла
#TODO дабавить путь к конфигу в глобальную переменную
#TODO добавить log_file_name и path_to_log в конфиг

log_file_name = 'info.txt'

class MyDaemon(Daemon):

        def parse_json(self, config_name: str):
                with open(config_name, 'r') as config_file:
                        info = config_file.read()

                JsonData = json.loads(info)
                return JsonData
        
        def backup(self, y_disk, target_dir: str):
                date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
                if y_disk.check_token():
                        print('[+] Success connection')
                        YaDbackup.backup(y_disk, target_dir)

                        info = f"\
                                {date}\n\
                                [+] The backup was done successful\n\
                                {'='*100}\
                                "
                        YaDbackup.EditLog(y_disk, target_dir, log_file_name, info)
                else:
                        with open(log_file_name, 'a') as readme_f:
                                info = f"\
                                        {date}\n\
                                        [-] Error with Yandex disk access\n\
                                        {'='*100}\
                                        "
                                readme_f.write(info + '\n')
                        os._exit(1)

        def run(self):

                # We can add the field "path-to-token" into json config and
                # parse it in code
                # but actually, we can't do the same with path-to-config
                # so, there is only way -- to hardcode it into src code 
                JsonData = self.parse_json('config.json')
                
                path_to_token = JsonData['token_path']
                target_dir_path = JsonData['target_dir_path']
                period_seconds = JsonData['period_seconds']

                with open(path_to_token, 'r') as Token:
                        token = Token.read()

                y = yadisk.YaDisk(token=token)

                schedule.every(period_seconds).seconds.do(self.backup, y_disk=y, target_dir=target_dir_path)

                # нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
                while True:
                        schedule.run_pending()
                        time.sleep(1)

                
                # YD_API.YD_PrintDiskInfo(y)
        

            
 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        # daemon.start()

        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                        date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
                        if not os.path.exists('/tmp/daemon-example.pid'):
                                with open(log_file_name, 'a') as readme_f:
                                        info = f"\
                                                {date}\n\
                                                [-] Error, there is not deamon pid\n\
                                                {'='*100}\
                                                "
                                        readme_f.write(info + '\n')
                                sys.exit(3)
                        else:
                                with open(log_file_name, 'a') as readme_f:
                                        info = f"\
                                                {date}\n\
                                                [+] Backup demon is running\n\
                                                {'='*100}\
                                                "
                                        readme_f.write(info + '\n')
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print("Usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)