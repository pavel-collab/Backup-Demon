from nbformat import read
import yadisk
import os
from datetime import datetime

with open('token', 'r') as Token:
    token = Token.read()

y = yadisk.YaDisk(token=token)

if y.check_token() != True:
    print('Access error')
else:
    print('Access ok')

    ## upload example
    # y.mkdir("/test/")                                   # Создать папку
    # y.upload("./test_dir/file1", "/test/file1.txt") # Загружает первый файл
    # y.upload("./test_dir/file2", "/test/file2.txt") # Загружает второй файл

    # # Получает общую информацию о диске
    # # возможно можно написать парсер для этого вывода 
    # # и использовать полученную информацию
    # print(y.get_disk_info())
    # print()

    # Выводит содержимое "/some/path"
    # print(list(y.listdir("/CV/")))
    # print()
    # print(list(y.listdir("/Recorded lesson (self)/")))
    # print()
    info = list(y.listdir("/Recorded lesson (self)/"))

    for item in info:
        print(item.size)
    # with open('local_info.txt', 'w') as Info:
    #     Info.write(str(info))
    # print(list(y.listdir("/Portfolio - Filippenko/")))