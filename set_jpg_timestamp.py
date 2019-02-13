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

    # new_ctimestamp1 for timestamp found in file tags, new_ctimestamp2 for timestamp found in file name.
    new_ctimestamp1 = None
    new_ctimestamp2 = None

    file_name = split(path)[1]
    print(f' [{file_name}]')

    # 尝试获取'Image DateTime'的时间
    try:
        new_ctimestamp1 = time.mktime(time.strptime(
            tags['Image DateTime'].values, '%Y:%m:%d %H:%M:%S'))
        print('  └─Found "Image DateTime"', end='')
    except KeyError:
        print('  └─"Image DateTime" not found, try next method.')
    except ValueError:
        print('  └─"Image DateTime" is not valid, try next method.')

    # 尝试获取'EXIF DateTimeOriginal'的时间
    if not new_ctimestamp1:
        try:
            new_ctimestamp1 = time.mktime(time.strptime(
                tags['EXIF DateTimeOriginal'].values, '%Y:%m:%d %H:%M:%S'))
            print('  └─Found "EXIF DateTimeOriginal"', end='')
        except KeyError:
            print('  └─"EXIF DateTimeOriginal" not found, try next method.')
        except ValueError:
            print('  └─"EXIF DateTimeOriginal" is not valid, try next method.')

    # 尝试获取'EXIF DateTimeDigitized'的时间
    if not new_ctimestamp1:
        try:
            new_ctimestamp1 = time.mktime(time.strptime(
                tags['EXIF DateTimeDigitized'].values, '%Y:%m:%d %H:%M:%S'))
            print('  └─Found "EXIF DateTimeDigitized"', end='')
        except KeyError:
            print('  └─"EXIF DateTimeDigitized" not found, try next method.')
        except ValueError:
            print('  └─"EXIF DateTimeDigitized" is not valid, try next method.')

    # 尝试从文件名获取时间，文件名需形如'XXX_YYYYmmdd_HHMMSS(_XXXXX).jp(e)g'
    file_name_no_ext = splitext(split(path)[1])[0]
    try:
        time_strs = file_name_no_ext.split('_')[1:3]
        new_ctimestamp2 = time.mktime(time.strptime(
            ''.join(time_strs), '%Y%m%d%H%M%S'))
        if new_ctimestamp1:
            print(' and file name contains timestamp', end='')
        else:
            print('  └─File name contains timestamp', end='')
    except (ValueError, OverflowError):
        if not new_ctimestamp1:
            print(
                '  └─File name dose not match XXX_YYYYmmdd_HHMMSS(_XXXXX).jp(e)g format.')

    if new_ctimestamp1 or new_ctimestamp2:
        if new_ctimestamp1 is None:
            new_ctimestamp = new_ctimestamp2
        elif new_ctimestamp2 is None:
            new_ctimestamp = new_ctimestamp1
        else:
            new_ctimestamp = new_ctimestamp1 if new_ctimestamp1 < new_ctimestamp2 else new_ctimestamp2
        old_ctimestamp = getctime(path)

        if abs(old_ctimestamp - new_ctimestamp) >= 1:
            ctime = Time(new_ctimestamp)
            try:
                handle = CreateFile(path, GENERIC_WRITE,
                                    FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
                SetFileTime(handle, ctime, None, ctime)
                CloseHandle(handle)
                print('. Done.')
            except:
                print(
                    '. Can not change ctime and mtime. Make sure you have right permission. Skip it.')
        else:
            print('. No need to change. Skip it.')
    else:
        print('  └─No valid timestamp found. Skip it.')


if __name__ == "__main__":
    import os
    import sys
    from os.path import isdir, join

    try:
        path = sys.argv[1:][0]
    except IndexError:
        path = './'
    if not isdir(path):
        print('请在命令行附加要更改文件所在文件夹的正确路径。')
        sys.exit(1)

    for root, dirs, files in os.walk(path):
        print(f'Processin dir [{root}]')
        for a_file in files:
            if splitext(a_file)[1] in ('.jpg', '.jpeg'):
                set_jpg_timestamp(join(root, a_file))
