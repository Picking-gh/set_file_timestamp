#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Written by - Picking@woft.name

import struct
import time
from collections import deque
from datetime import datetime, timedelta, timezone
from os.path import getctime, getmtime, getsize

from pywintypes import Time

from win32file import (FILE_ATTRIBUTE_NORMAL, FILE_SHARE_WRITE, GENERIC_WRITE,
                       OPEN_EXISTING, CloseHandle, CreateFile, SetFileTime)

from mp4parse import parser


def get_mvhd(path):
    '''Returns the whole mvhd box content including the box length.

    A mp4 file must contain only one mvhd box. So we get one or none.
    '''
    s = deque()
    with open(path, 'rb') as f:
        g = parser(s, f, 0, getsize(path))
        while True:
            try:
                box_info, _ = next(g)
                if box_info[0] == 'mvhd':
                    f.seek(box_info[2])
                    return f.read(box_info[1])
            except StopIteration:
                return b''


def get_datetime(n: int):
    '''Returns a datetime object that is n seconds after the midnight, Jan. 1, 1904, in local time.
    '''
    # January 1st, 1904 at midnight, UTC time
    start_point = datetime(1904, 1, 1).replace(tzinfo=timezone.utc)
    delta = timedelta(seconds=n)
    # 设置本地时区，暂时只针对不使用DST的地区。time.timezone在东半球为负值，故需要加个负号
    tz_adj = timezone(timedelta(seconds=-time.timezone))
    return (start_point + delta).astimezone(tz_adj)


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
        version = mvhd[8:9]
        if version == b'\x00':
            creation_time = struct.unpack('>I', mvhd[12:16])[0]
            modification_time = struct.unpack('>I', mvhd[16:20])[0]
        elif version == b'\x01':
            creation_time = struct.unpack('>Q', mvhd[12:20])[0]
            modification_time = struct.unpack('>Q', mvhd[20:28])[0]
    except (IndexError, struct.error):
        print(
            f'{path} contains no valid mvhd box. May not be a valid mp4 file. Skip it.')
        return
    if creation_time + modification_time == 0:
        print(f'{path} contains no creation_time or modification_time. Skip it.')
        return
    if creation_time == 0:
        creation_time = modification_time
    if modification_time == 0:
        modification_time = creation_time
    new_ctimestamp = time.mktime(get_datetime(creation_time).timetuple())
    new_mtimestamp = time.mktime(get_datetime(modification_time).timetuple())

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


if __name__ == "__main__":
    import os
    import sys

    from os.path import isdir, join, splitext

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
