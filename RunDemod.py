#!/usr/bin/env python

import schedule 
import time
import yadisk
from datetime import datetime
import sys
import os
from Demon import Daemon

# import YD_API
import YaDbackup

#? что происходит, если время между отправками меньше времени бэкапа
#TODO рефакторинг имен
#? в момент прерывания сигналом, процесс может оборваться на середине. Как заставить его делать бэкап до конца?
#TODO добавить возможность исключать папки и фалы, которые не нужно бэкапить (через конфиг)
#TODO Добавить паттерн для datetime, чтобы можно было менять его в одном месте
#TODO создать несколько веток для различных реализаций:
#TODO   реализация чисто через python
#TODO   реализация через python и C
#TODO   реалзация через python и C++
#TODO   реалихация со встроенной библиотекой для демона
#TODO   демон на C

#! Написать объяснение, почему в конфигах надо писать абсолютные пути
#! написать комментарии)

config_file_name = YaDbackup.dir_location + 'config.json'

class MyDaemon(Daemon):
        
        def backup(self, y_disk, target_dir: str):
                date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
                dir_settings, system_settings = YaDbackup.parse_json(config_file_name)
                log_file_name = YaDbackup.dir_location + dir_settings['log_file_name']

                if y_disk.check_token():
                        with open(log_file_name, 'a') as readme_f:
                                readme_f.write('[+] Success connection\n')
                        if YaDbackup.DEBUG: print('[+] Success connection')
                        YaDbackup.backup(y_disk, target_dir, config_file_name)
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
                dir_settings, system_settings = YaDbackup.parse_json(config_file_name)
                
                path_to_token = dir_settings['token_path']
                target_dir_path = dir_settings['target_dir_path']

                #TODO setting of backup period
                period_seconds = system_settings['period_seconds']

                with open(path_to_token, 'r') as Token:
                        token = Token.read()

                y = yadisk.YaDisk(token=token)

                schedule.every(period_seconds).seconds.do(self.backup, y_disk=y, target_dir=target_dir_path)

                # нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
                while True:
                        schedule.run_pending()
                        time.sleep(1)

            
 
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
                print("Usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)