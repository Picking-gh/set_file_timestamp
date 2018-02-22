import os
import time
from os.path import join, splitext, split

import exifread
from pywintypes import Time

from win32file import (FILE_ATTRIBUTE_NORMAL, FILE_SHARE_WRITE, GENERIC_WRITE,
                       OPEN_EXISTING, CloseHandle, CreateFile, SetFileTime)


def set_jpg_time_stamp(path):
    '''用保存在EXIF中的拍摄时间设置图片的创建时间和修改时间
    '''
    f = open(path, 'rb')
    tags = exifread.process_file(f, details=False)
    f.close()

    ctime = None

    # 尝试获取'Image DateTime'的时间
    try:
        ctime = Time(time.mktime(time.strptime(
            tags['Image DateTime'].values, '%Y:%m:%d %H:%M:%S')))
    except KeyError:
        print('No Image DateTime in "{}", try next method.'.format(path))

    # 尝试获取'EXIF DateTimeOriginal'的时间
    if not ctime:
        try:
            ctime = Time(time.mktime(time.strptime(
                tags['EXIF DateTimeOriginal'].values, '%Y:%m:%d %H:%M:%S')))
        except KeyError:
            print('No EXIF DateTimeOriginal key in "{}", try next method.'.format(path))

    # 尝试获取'EXIF DateTimeDigitized'的时间
    if not ctime:
        try:
            ctime = Time(time.mktime(time.strptime(
                tags['EXIF DateTimeDigitized'].values, '%Y:%m:%d %H:%M:%S')))
        except KeyError:
            print(
                'No EXIF DateTimeDigitized key in "{}", try next method.'.format(path))

    # 尝试从文件名获取时间，文件名需形如'XXX_YYYYmmdd_HHMMSS(_XXXXX).jp(e)g'
    if not ctime:
        file_name_no_ext = splitext(split(path)[1])[0]
        try:
            time_str_1, time_str_2 = file_name_no_ext.split('_')[1:3]
            ctime = Time(time.mktime(time.strptime(
                time_str_1 + time_str_2, '%Y%m%d%H%M%S')))
        except ValueError:
            print(
                'File name in "{}" contains no valid time info, nothing to try.'.format(path))

    if ctime:
        handle = CreateFile(path, GENERIC_WRITE,
                            FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        SetFileTime(handle, ctime, None, ctime)
        CloseHandle(handle)


for root, dirs, files in os.walk(u'r:/Pictures & Videos/WeiXin - honor 7/'):
    for a_file in files:
        if splitext(a_file)[1] in ('.jpg', '.jpeg'):
            set_jpg_time_stamp(join(root, a_file))
