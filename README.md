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

    ((b'ftyp', 32, 0), ('file',))
    ((b'moov', 8372, 32), ('file',))
    ((b'mvhd', 108, 40), ('file', b'moov'))
    ((b'trak', 5064, 148), ('file', b'moov'))
    ...
