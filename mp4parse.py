#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Written by - Picking@woft.name

'''用于解析符合ISO/IEC 14496-12标准的mp4文件的box层次结构
参考:
https://blog.csdn.net/PirateLeo/article/details/7590056
https://blog.csdn.net/pirateleo/article/details/7061452
https://l.web.umkc.edu/lizhu/teaching/2016sp.video-communication/ref/mp4.pdf
'''
import struct

from collections import deque


# From ISO/IEC 14496-12 2nd edition in the 3rd link above and is out of date now...wtf
# box的类型没有在boxes中，则整个box被忽略；
# box的类型没有在container中，则不深入解析
box = {b'ftyp', b'moov', b'mdat', b'trak', b'tref', b'hint', b'cdsc', b'mdia', b'minf', b'dinf', b'stbl',
       b'free', b'skip', b'edts', b'udta', b'mvex', b'moof', b'traf', b'mfra', b'sinf', b'schi', b'tims',
       b'tsro', b'snro', b'rtpo', b'hnti', b'rtpb', b'sdpb', b'hinf', b'trpy', b'nump', b'tpyl', b'totl',
       b'npck', b'tpay', b'maxr', b'dmed', b'dimm', b'drep', b'tmin', b'tmax', b'pmax', b'dmax', b'payt'}
fullbox = {b'mvhd', b'tkhd', b'mdhd', b'hdlr', b'vmhd', b'smhd', b'hmhd', b'nmhd', b'urlb', b'urnb', b'dref', b'stts',
           b'ctts', b'stsd', b'stsz', b'stz2', b'stsc', b'stco', b'co64', b'stss', b'stsh', b'stdp', b'padb', b'elst',
           b'cprt', b'mehd', b'trex', b'mfhd', b'tfhd', b'trun', b'tfra', b'mfro', b'sdtp', b'sbgp', b'sgpd', b'stsl',
           b'subs', b'pdin', b'meta', b'xmlb', b'bxml', b'iloc', b'pitm', b'ipro', b'infe', b'iinf', b'imif', b'ipmc',
           b'schm', b'srpp'}
container = {b'moov', b'trak', b'edts', b'mdia', b'minf', b'dinf', b'stbl', b'mvex',
             b'moof', b'traf', b'mfra', b'skip', b'udta', b'meta', b'ipro', b'sinf',
             b'srpp', b'srtp'}
boxes = box | fullbox | {b'uuid'}


def parser(s: deque, f, offset: int, size: int):
    '''box结构生成器，按深度优先方式遍历待解析数据段中的boxes，按顺序生成单一box信息和该box所在层次。
    s: box层结构栈；
    f: 读取数据的文件；
    offset: 起始解析点；
    size: 待解析数据长度；
    box信息: (box_type, box_len, box_offset(相对于offset))；
    box所在层次的copy：tuple(s)。
    '''
    box_offset = 0
    while True:
        if box_offset >= size:
            return

        f.seek(offset + box_offset)

        try:
            box_len = struct.unpack('>I', f.read(4))[0]
        except struct.error:
            raise ValueError('File corrupted. Stop parsing.')
        box_type = f.read(4)
        if len(box_type) != 4:
            raise ValueError('File corrupted. Stop parsing.')
        # box的类型没有在boxes中，则整个box被忽略；
        if box_type not in boxes:
            box_offset += box_len
            continue
        # data followed by header in normal box, assume the data is a sub_box
        sub_box_offset = 8
        # fullbox has an additional 1 byte of version and 3 bytes of flags
        if box_type in fullbox:
            # dummy read
            if len(f.read(4)) != 4:
                raise ValueError('File corrupted. Stop parsing.')
            sub_box_offset += 4
        # 0 size box means end of file
        if box_len == 0:
            return
        # box length determined by following 64bits largesize
        elif box_len == 1:
            try:
                box_len = struct.unpack('>Q', f.read(8))[0]
            except struct.error:
                raise ValueError('File corrupted. Stop parsing.')
            sub_box_offset += 8
        yield ((box_type, box_len, offset + box_offset), tuple(s))

        if box_type in container:
            # meta只有在最顶层的时候才是容器
            if box_type == b'meta' and len(s) != 1:
                pass
            else:
                s.append(box_type.decode())
                sub_box_parse = parser(
                    s, f, offset+box_offset+sub_box_offset, box_len-sub_box_offset)
                yield from sub_box_parse
                s.pop()
        box_offset += box_len


if __name__ == "__main__":
    from os.path import isdir, getsize
    import sys

    try:
        mp4file = sys.argv[1:][0]
    except IndexError:
        print(u'请在命令行附加要解析的文件。')
        sys.exit(1)
    if isdir(mp4file):
        print(u'请在命令行附加要解析的文件。')
        sys.exit(1)

    s = deque()
    s.append('file')
    with open(mp4file, 'rb') as f:
        g = parser(s, f, 0, getsize(mp4file))
        for box in g:
            print(box)
