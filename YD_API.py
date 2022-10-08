import yadisk
import os

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