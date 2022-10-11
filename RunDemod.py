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

#TODO: добавить в конфиг параметр "пусть к конфигу" (обязательно прописывать абсолютный пусть)
#TODO: добавить в конфиг параметр "пусть к токену" (обязательно прописывать абсолютный пусть)
#TODO: убрать из конфига параметр "период по секундам"
#! бэкап занимает некоторое количество времени t, если период выгрузки данных T>t, то могут возникнуть проблемы
#TODO добавить автоматическую проверку, работает ли демон

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
                with open('token', 'r') as Token:
                        token = Token.read()

                y = yadisk.YaDisk(token=token)

                JsonData = self.parse_json('config.json')
                target_dir_path = JsonData['target_dir_path']
                period_seconds = JsonData['period_seconds']

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