Данный репозиторий создан для моего домашнего проекта -- бэкап демон на Linux.

По задумке демон должен работать в фоне операционной системы и с установленной переодичностью
выполнять бэкап указанных папок. Затем данные папки должны автоматически выгружаться на удаленную систему. В планах написать реализацию для выгрузки данных на Яндекс Диск 
(используя python Yandex API) и на отдельный серверок, построенный на базе raspberry pi 
(предполагается делать это через ssh соединение).

### Requirements

```
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
python3 RunDemod.py start
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
- [ ] Написать файл взаиможейтсвия с YandexDisk API
- [ ] Сделать implementation демона на C
- [ ] Сделать implementations копирования дерикторий с помощью различных средств (python, c++, unix).
- [ ] Протестировать на скорость ращличные варианты работы программы 
- [ ] Написать нормальную сборку.