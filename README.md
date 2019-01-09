**自己用的，没有充分测试！只可用于Windows，Linux下无效！**

需要python 3.6及以上版本。

1. set_jpg_timestamp.py

使用第三方库：ExifRead, pypiwin32

用法：`python set_jpg_timestamp.py "jpg文件夹路径（不包含结尾的/）"。`

2. set_mp4_timeftamp.py

使用第三方库：pypiwin32

用法：`python set_mp4_timestamp.py "mp4文件夹路径（不包含结尾的/）"`

3. mp4parse.py

用法：`python mp4parse.py "mp4文件"`

输出：文件中所有的box的信息(type, length, offset)和所属层次关系：

    ((b'ftyp', 24, 0), ('file',))
    ((b'moov', 9677, 24), ('file',))
    ((b'mvhd', 108, 32), ('file', 'moov'))
    ((b'trak', 2760, 164), ('file', 'moov'))
    ((b'tkhd', 92, 172), ('file', 'moov', 'trak'))
    ((b'mdia', 2660, 264), ('file', 'moov', 'trak'))
    ((b'mdhd', 32, 272), ('file', 'moov', 'trak', 'mdia'))
    ((b'hdlr', 33, 304), ('file', 'moov', 'trak', 'mdia'))
    ((b'minf', 2587, 337), ('file', 'moov', 'trak', 'mdia'))
    ((b'smhd', 16, 345), ('file', 'moov', 'trak', 'mdia', 'minf'))
    ((b'dinf', 36, 361), ('file', 'moov', 'trak', 'mdia', 'minf'))
    ((b'dref', 28, 369), ('file', 'moov', 'trak', 'mdia', 'minf', 'dinf'))
    ((b'stbl', 2527, 397), ('file', 'moov', 'trak', 'mdia', 'minf'))
    ((b'stsd', 103, 405), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stts', 24, 508), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stsz', 2284, 532), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stsc', 40, 2816), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stco', 68, 2856), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'trak', 6777, 2924), ('file', 'moov'))
    ((b'tkhd', 92, 2932), ('file', 'moov', 'trak'))
    ((b'mdia', 6677, 3024), ('file', 'moov', 'trak'))
    ((b'mdhd', 32, 3032), ('file', 'moov', 'trak', 'mdia'))
    ((b'hdlr', 33, 3064), ('file', 'moov', 'trak', 'mdia'))
    ((b'minf', 6604, 3097), ('file', 'moov', 'trak', 'mdia'))
    ((b'vmhd', 20, 3105), ('file', 'moov', 'trak', 'mdia', 'minf'))
    ((b'dinf', 36, 3125), ('file', 'moov', 'trak', 'mdia', 'minf'))
    ((b'dref', 28, 3133), ('file', 'moov', 'trak', 'mdia', 'minf', 'dinf'))
    ((b'stbl', 6540, 3161), ('file', 'moov', 'trak', 'mdia', 'minf'))
    ((b'stsd', 148, 3169), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stts', 1912, 3317), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stsz', 1456, 5229), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stsc', 40, 6685), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stco', 64, 6725), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'stss', 24, 6789), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'ctts', 2888, 6813), ('file', 'moov', 'trak', 'mdia', 'minf', 'stbl'))
    ((b'free', 136, 9701), ('file',))
    ((b'mdat', 1737642, 9837), ('file',))
    ((b'free', 136, 1747479), ('file',))
