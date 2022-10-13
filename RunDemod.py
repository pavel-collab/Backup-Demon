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

#TODO: дописать нормальное оформление log файла (возможно поменять расширение, чтобы можно было читать прямо с яндекс диска)
#TODO: убрать из конфига параметр "период по секундам"
#! бэкап занимает некоторое количество времени t, если период выгрузки данных T>t, то могут возникнуть проблемы
#TODO сделать запись информации о ходе бэкапа в log

class MyDaemon(Daemon):

        def parse_json(self, config_name: str):
                with open(config_name, 'r') as config_file:
                        info = config_file.read()

                JsonData = json.loads(info)
                return JsonData
        
        def backup(self, y_disk, target_dir: str):
                if y_disk.check_token():
                        print('[+] Success connection')
                        YaDbackup.backup(y_disk, target_dir)
                else:
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
                        if not os.path.exists('/tmp/daemon-example.pid'):
                                print('[-] Error, there is not deamon pid')
                                sys.exit(3)
                        else:
                                print('[+] Backup demon is running')    
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)