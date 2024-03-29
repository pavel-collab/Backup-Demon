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
#TODO переписать функционал, чтобы вся отадочная информация печаталась и в лог файл и в консоль
#TODO отладочная информация должна печататься в консоль, только если поднят флаг
#TODO на данный момент, лог фай образуется в корне. Исправить
#TODO DEBUG в 2х местах. Исправить
#TODO рефакторинг имен
#TODO выяснить почему часть функционала не работает. Исправить
#TODO Написать кусок функционала для удаления старых бэкапов на удаленном диске (не хранить больше, чем n бэкапов)
#? Возможно, имеет смысл разделить конфиг на 2 структуры -- структура, которую пользователь меняет и которую не меняет
#TODO Поскольку конфиг всегда храниться в папке с программой -- определять автоматически текущую рабочую папку и коннектить абслютный пусть к названию конфига
#? в момент прерывания сигналом, процесс может оборваться на середине. Как заставить его делать бэкап до конца?

#! Написать объяснение, почему в конфигах надо писать абсолютные пути

config_file_name = 'config.json'
DEBUG = True

class MyDaemon(Daemon):
        
        def backup(self, y_disk, target_dir: str):
                date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
                JsonData = YaDbackup.parse_json(config_file_name)
                log_file_name = JsonData['log_file_name']

                if y_disk.check_token():
                        #! HARDCODE
                        with open(log_file_name, 'a') as readme_f:
                                readme_f.write('[+] Success connection\n')
                        if DEBUG: print('[+] Success connection')
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
                JsonData = YaDbackup.parse_json(config_file_name)
                
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
                        JsonData = YaDbackup.parse_json(config_file_name)
                        log_file_name = JsonData['log_file_name']

                        #! This part of code doesn't work!
                        # if not os.path.exists('/tmp/daemon-example.pid'):
                        #         with open(log_file_name, 'a') as readme_f:
                        #                 info = f"\
                        #                         {date}\n\
                        #                         [-] Error, there is not deamon pid\n\
                        #                         {'='*100}\
                        #                         "
                        #                 readme_f.write(info + '\n')
                        #         sys.exit(3)
                        # else:
                        #         pass
                        #         with open(log_file_name, 'a') as readme_f:
                        #                 info = f"\
                        #                         {date}\n\
                        #                         [+] Backup demon is running\n\
                        #                         {'='*100}\
                        #                         "
                        #                 readme_f.write(info + '\n')
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