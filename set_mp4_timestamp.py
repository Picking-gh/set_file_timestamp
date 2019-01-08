#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Written by - Picking@woft.name

'''参考:
https://blog.csdn.net/PirateLeo/article/details/7590056
https://blog.csdn.net/pirateleo/article/details/7061452
'''
import os
import sys
import struct
import time
from datetime import datetime, timedelta
from os.path import getctime, getmtime, isdir, join, split, splitext

from pywintypes import Time

from win32file import (FILE_ATTRIBUTE_NORMAL, FILE_SHARE_WRITE, GENERIC_WRITE,
                       OPEN_EXISTING, CloseHandle, CreateFile, SetFileTime)


def get_a_mp4_box_body(path):
    # get len
    # get header
    with open(path, 'rb') as f:
        try:
            box_len = struct.unpack('>I', f.read(4))[0]
        except struct.error:
            raise ValueError(
                'File corrupted. This may not be a valid mp4 file.')
        first_box_body = f.read(box_len - 4)
        if len(first_box_body) != box_len - 4:
            raise ValueError(
                'File corrupted. This may not be a valid mp4 file.')
        if first_box_body[0:4] != b'ftyp':
            raise ValueError(
                'No ftypbox found. This may not be a valid mp4 file.')
        while True:
            try:
                box_len = struct.unpack('>I', f.read(4))[0]
            except struct.error:
                raise ValueError(
                    'File corrupted. This may not be a valid mp4 file.')
            # hit the last box
            if box_len == 0:
                return
            # box size to be large
            if box_len == 1:
                # this 12 bytes box_body_1 contains the box type(4) and the large-size(8)
                box_body_1 = f.read(12)
                try:
                    box_len = struct.unpack('>Q', box_body_1[4:])[0]
                except struct.error:
                    raise ValueError(
                        'File corrupted. This may not be a valid mp4 file.')                
                box_body_2_len = box_len - 16
            # box size is less than 0xFFFFFFFF
            else:
                box_body_1 = b''
                box_body_2_len = box_len - 4
            box_body_2 = f.read(box_body_2_len)
            # hit the end of file. file maybe interrupted
            if len(box_body_2) != box_body_2_len:
                return box_body_1 + box_body_2
            # finally the box_body!
            yield box_body_1 + box_body_2


def get_mvhd(path):
    '''A mp4 file contains only one mvhdbox. So we get one or none
    '''
    g = get_a_mp4_box_body(path)
    while True:
        try:
            box_body = next(g)
            if box_body[0:4] == 'mvhd':
                return box_body
        except StopIteration:
            return b''


def get_datetime(n: int):
    '''n: creation_time or modification_time in the mvhd.
    Tihs is an integer in seconds since midnight, Jan. 1, 1904, in UTC time
    Make this integer a datetime object.
    '''
    start_point = datetime(1904, 1, 1)  # January 1st, 1904 at midnight
    delta = timedelta(seconds=n)
    return start_point + delta


def set_mp4_timestamp(path):
    '''用mvhd中的creation_time和modification_time设置mp4文件的创建时间和修改时间。
    如果目标时间与当前文件的创建时间一致（时间差小于1s）则不修改。
    如果creation_time和modification_time之中有1个为0，则用另一个赋值，都为零则不修改文件时间。
    '''
    try:
        mvhd = get_mvhd(path)
    except ValueError as error:
        print(f'When processing {path} a error occurs: {error}. Skip it.')
        return

    # mvhd is FullBox，是Box的扩展，Box结构的基础上在Header中增加8bits version和24bits flags
    try:
        version = mvhd[4:5]
        if version == b'0':
            creation_time = get_datetime(struct.unpack('>I', mvhd[8:12])[0])
            modification_time = get_datetime(struct.unpack('>I', mvhd[12:16])[0])
        else:
            creation_time = get_datetime(struct.unpack('>Q', mvhd[8:16])[0])
            modification_time = get_datetime(struct.unpack('>Q', mvhd[16:24])[0])
    except (IndexError, struct.error):
        print(f'{path} contains no valid mvhd box. Skip it.')
        return
    new_ctimestamp = time.mktime(creation_time.timetuple())
    new_mtimestamp = time.mktime(modification_time.timetuple())
    if new_ctimestamp + new_mtimestamp == 0:
        print(f'{path} contains no creation_time or modification_time. Skip it.')
        return
    if new_ctimestamp == 0:
        new_ctimestamp = new_mtimestamp
    if new_mtimestamp == 0:
        new_mtimestamp = new_ctimestamp

    mod_flag = False
    old_mtimestamp = getmtime(path)
    mtime = Time(old_mtimestamp)
    if abs(old_mtimestamp - new_mtimestamp) >= 1:
        mtime = Time(new_mtimestamp)
        mod_flag = True

    old_ctimestamp = getctime(path)
    ctime = Time(old_ctimestamp)
    if abs(old_ctimestamp - new_ctimestamp) >= 1:
        ctime = Time(new_ctimestamp)
        mod_flag = True

    if mod_flag:
        handle = CreateFile(path, GENERIC_WRITE,
                            FILE_SHARE_WRITE, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        SetFileTime(handle, ctime, None, mtime)
        CloseHandle(handle)


try:
    path = sys.argv[1:][0]
except IndexError:
    path = './'
if not isdir(path):
    print(u'请在命令行附加要更改文件所在文件夹的正确路径。')
    sys.exit(1)

for root, dirs, files in os.walk(path):
    for a_file in files:
        if splitext(a_file)[1] in ('.mp4',):
            set_mp4_timestamp(join(root, a_file))
