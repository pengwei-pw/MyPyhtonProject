# _*_ coding=utf-8 _*_
# author : PengWei
# function : 将MP3格式的音频转为wav格式
# time : 2023/2/19 13:14

import os
from pydub import AudioSegment

"""
function:mp3->wav
mp3_path:mp3原始文件路径
out_path:转换wav文件路径
"""


def mp3_wav(mp3_path : str, out_path : str) -> None:
    if mp3_path.endswith(".mp3"):
        try:
            sound = AudioSegment.from_file(mp3_path)
            path = os.path.join(out_path, os.path.basename(mp3_path).replace(mp3_path[mp3_path.rindex("."):], "wav"))
            sound.export(path, format = "wav")
        except:
            print(mp3_path, "转换异常！")
    else:
        print("转换原始文件不为mp3文件")


"""
function:wav->mp3
mp3_path:wav原始文件路径
out_path:转换mp3文件路径
"""


def wav_mp3(wav_path: str, out_path: str) -> None:
    if wav_path.endswith(".wav"):
        try:
            sound = AudioSegment.from_file(wav_path)
            path = os.path.join(out_path, os.path.basename(wav_path).replace(wav_path[wav_path.rindex("."):], "mp3"))
            sound.export(path, format="mp3")
        except:
            print(wav_path, "转换异常！")
    else:
        print("转换原始文件不为wav文件")
