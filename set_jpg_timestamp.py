#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Written by - Picking@woft.name

import time
from os.path import getctime, split, splitext

import exifread
from pywintypes import Time

from win32file import (FILE_ATTRIBUTE_NORMAL, FILE_SHARE_WRITE, GENERIC_WRITE,
                       OPEN_EXISTING, CloseHandle, CreateFile, SetFileTime)


def set_jpg_timestamp(path):
    '''用保存在EXIF中的拍摄时间设置图片的创建时间和修改时间。

    如果目标时间与当前文件的创建时间一致（时间差小于1s）则不修改。
    '''
    f = open(path, 'rb')
    tags = exifread.process_file(f, details=False)
    f.close()

    new_timestamp = None

    # 尝试获取'Image DateTime'的时间
    try:
        new_timestamp = time.mktime(time.strptime(
            tags['Image DateTime'].values, '%Y:%m:%d %H:%M:%S'))
    except KeyError:
        print('No Image DateTime in "{}", try next method.'.format(path))

    # 尝试获取'EXIF DateTimeOriginal'的时间
    if not new_timestamp:
        try:
            new_timestamp = time.mktime(time.strptime(
                tags['EXIF DateTimeOriginal'].values, '%Y:%m:%d %H:%M:%S'))
        except KeyError:
            print('No EXIF DateTimeOriginal key in "{}", try next method.'.format(path))

    # 尝试获取'EXIF DateTimeDigitized'的时间
    if not new_timestamp:
        try:
            new_timestamp = time.mktime(time.strptime(
                tags['EXIF DateTimeDigitized'].values, '%Y:%m:%d %H:%M:%S'))
        except KeyError:
            print(
                'No EXIF DateTimeDigitized key in "{}", try next method.'.format(path))

    # 尝试从文件名获取时间，文件名需形如'XXX_YYYYmmdd_HHMMSS(_XXXXX).jp(e)g'
    if not new_timestamp:
        file_name_no_ext = splitext(split(path)[1])[0]
        try:
            time_strs = file_name_no_ext.split('_')[1:3]
            new_timestamp = time.mktime(time.strptime(
                ''.join(time_strs), '%Y%m%d%H%M%S'))
        except ValueError:
            print(
                'File name in "{}" contains no valid time info, nothing to try.'.format(path))

    if new_timestamp:
        old_timestamp = getctime(path)
        if abs(old_timestamp - new_timestamp) >= 1:
            ctime = Time(new_timestamp)
            handle = CreateFile(path, GENERIC_WRITE,
                                FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
            SetFileTime(handle, ctime, None, ctime)
            CloseHandle(handle)


if __name__ == "__main__":
    import os
    import sys
    from os.path import isdir, join

    try:
        path = sys.argv[1:][0]
    except IndexError:
        path = './'
    if not isdir(path):
        print(u'请在命令行附加要更改文件所在文件夹的正确路径。')
        sys.exit(1)

    for root, dirs, files in os.walk(path):
        for a_file in files:
            if splitext(a_file)[1] in ('.jpg', '.jpeg'):
                set_jpg_timestamp(join(root, a_file))
