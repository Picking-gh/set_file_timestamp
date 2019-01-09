**自己用的，没有充分测试！1和2只可用于Windows，Linux下无效！**

需要python 3.6及以上版本。

1. set_jpg_timestamp.py

用法（需使用第三方库：ExifRead, pypiwin32）：

    python set_jpg_timestamp.py "jpg文件夹路径（不包含结尾的/）"。

2. set_mp4_timeftamp.py

用法（需使用第三方库：pypiwin32）：

    python set_mp4_timestamp.py "mp4文件夹路径（不包含结尾的/）"

3. mp4parse.py

用法1：

    from collections import deque
    from os.path import getsize
    
    from mp4parse import parser
    
    mp4file = 'xxx'
    s = deque()
    with open(mp4file, 'rb') as f:
        g = parser(s, f, 0, getsize(mp4file))
        for box_info, box_stacks in g:
            pass
        
用法2（需使用第三方库：asciitree）：

    python mp4parse.py "mp4文件"

输出："mp4文件"中所有的box的信息及层次关系，每个节点格式为：box_type (@offset, length)

    .\tmp\19283803011996511a580271.mp4
    +-- ftyp (@0, 32)
    +-- moov (@32, 8372)
    |   +-- mvhd (@40, 108)
    |   +-- trak (@148, 5064)
    |   |   +-- tkhd (@156, 92)
    |   |   +-- edts (@248, 36)
    |   |   |   +-- elst (@256, 28)
    |   |   +-- mdia (@284, 4928)
    |   |       +-- mdhd (@292, 32)
    |   |       +-- hdlr (@324, 45)
    |   |       +-- minf (@369, 4843)
    |   |           +-- smhd (@377, 16)
    |   |           +-- dinf (@393, 36)
    |   |           |   +-- dref (@401, 28)
    |   |           +-- stbl (@429, 4783)
    |   |               +-- stsd (@437, 103)
    |   |               +-- stts (@540, 24)
    |   |               +-- stsc (@564, 892)
    |   |               +-- stsz (@1456, 2772)
    |   |               +-- stco (@4228, 984)
    |   +-- trak (@5212, 2679)
    |   |   +-- tkhd (@5220, 92)
    |   |   +-- edts (@5312, 36)
    |   |   |   +-- elst (@5320, 28)
    |   |   +-- mdia (@5348, 2543)
    |   |       +-- mdhd (@5356, 32)
    |   |       +-- hdlr (@5388, 45)
    |   |       +-- minf (@5433, 2458)
    |   |           +-- vmhd (@5441, 20)
    |   |           +-- dinf (@5461, 36)
    |   |           |   +-- dref (@5469, 28)
    |   |           +-- stbl (@5497, 2394)
    |   |               +-- stsd (@5505, 138)
    |   |               +-- stts (@5643, 200)
    |   |               +-- stss (@5843, 20)
    |   |               +-- stsc (@5863, 40)
    |   |               +-- stsz (@5903, 1004)
    |   |               +-- stco (@6907, 984)
    |   +-- udta (@7891, 513)
    |       +-- meta (@7899, 90)
    +-- mdat (@8404, 2386598)
