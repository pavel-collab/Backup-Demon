from nbformat import read
import yadisk
import os
from datetime import datetime

def YD_GetDirInfo(y_disk, dir: str):
    info = list(y_disk.listdir(dir))
    
    result = []

    for item in info:
        obj_info = {}

        obj_info['URL'] = item.file
        obj_info['name'] = item.name
        obj_info['modified'] = item.modified
        obj_info['created'] = item.created
        obj_info['path'] = item.path
        obj_info['type'] = item.type
        obj_info['media_type'] = item.media_type
        obj_info['size'] = item.size

        result.append(obj_info)
    
    return result

def YD_PrintDirInfo(y_disk, dir: str):
    dir_info = YD_GetDirInfo(y_disk, dir)

    for item in dir_info:
        print('file %s:' %item['name'])
        print('\ttype: ', item['type'])
        print('\tmedia type: ', item['media_type'])
        print('\tpath: ', item['path'])
        print('\tsize: ', item['size'])
        print('\tcreated: ', item['created'])
        print('\tmodified: ', item['modified'])
        # print('\tURL: ', item['URL'])
        print()

def YD_FindObj(y_disk, dir: str, obj_name: str):
    dir_info = YD_GetDirInfo(y_disk, dir)

    objects = [item['name'] for item in dir_info]
    return obj_name in objects



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

    YD_PrintDirInfo(y, '/Recorded lesson (self)/')
    print(YD_FindObj(y, '/Recorded lesson (self)/', '2022-0-28 19-44-28.mkv'))