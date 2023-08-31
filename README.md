Данный репозиторий создан для моего домашнего проекта -- бэкап демон на Linux.

По задумке демон должен работать в фоне операционной системы и с установленной переодичностью
выполнять бэкап указанных папок. Затем данные папки должны автоматически выгружаться на удаленную систему. В планах написать реализацию для выгрузки данных на Яндекс Диск 
(используя python Yandex API) и на отдельный серверок, построенный на базе raspberry pi 
(предполагается делать это через ssh соединение).

### Requirements

```
apt-get install -y python3
RUN apt-get install -y pip
pip install yadisk
pip install schedule 
```

### How to use docker

Докер предназначен для тестирования.
Собираем образ на базе ubuntu:20.04.
```
docker build -t test_demon .
```
Запускаем докер-контейнер в интерактивном режиме и запускаем демона.
```
docker run --rm -it test_demon
```

### For developer

what do you need to do to test program in docker container.

In the docker container you have to make some settings in config.
You have to change the path to your taget dir and path to your token.

For example, when u test it u have all files in 
```
/usr/src/app
```
so, u need to change your config to:
```
[
    {
        "target_dir_path"   : "/usr/src/app/test_dir/",
        "token_path"        : "/usr/src/app/token",
        "log_file_name"     : "info.txt",
        "remout_backup_dir" : "/test_backup/"
    },

    {
        "backup_amount"   : 5,

        "period_seconds"  : 5,
        "period_minutes"  : 1,
        "period_hour"     : 1,
        "period_day"      : 1,
        "period_week"     : 0
    }
]
```
After that start your program by
```
python3 RunDemod.py start
```

When you chaked all the proceses run correctly, you need to stop your programm, but if
you will do it in the same terminal, you will not stop the proces.

Actually, you need to stop the program, use 
```
docker exec
```

Firstly you will need an id of docker container:
```
docker ps -a
```

After u will copy the container id, you will be able to 
```
docker exec <container-id> python3 RunDemod.py stop
```

Проверяем /tmp/ (там должен быть пид процесса)
```
ls /tmp/
```

### TODO LIST
- [ ] Просмотреть внимательно код демона. Написать комментарии, где это необходимо.
- [ ] Дописать дункционал для демона.
    - Вызов статуса
    - Вызов информации (сколько копий сделано, последний бэкап, статус работы)
    - Смена целевой дериктории
- [X] Написать файл взаиможейтсвия с YandexDisk API
- [ ] Сделать implementation демона на C
- [ ] Сделать implementations копирования дерикторий с помощью различных средств (python, c++, unix).
- [ ] Протестировать на скорость ращличные варианты работы программы 
- [ ] Написать нормальную сборку.