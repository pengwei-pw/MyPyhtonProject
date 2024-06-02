#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :SoundFileUtils.py
# @Time      :2024/6/1 17:41
# @Author    :pengweiaini123@163.com
import soundfile as sf
import numpy as np


def soundfile_read():
    """
    使用soundfile读取音频文件
    :return:
    """
    wav_path = r"./AudioPath/周杰伦 - 听妈妈的话.wav"  # sr=44100 ch=2 bit=2
    data1, sr = sf.read(wav_path)
    print(f"data1:{data1} \n sr:{sr}")
    rms = [np.sqrt(np.mean(block ** 2)) for block in
           sf.blocks(wav_path, blocksize=1024, overlap=512)]
    # list_data = []
    len_data = 0
    # 可以使用block按照blocksize大小读取，overlap是重叠大小
    for block in sf.blocks(wav_path, blocksize=1024, overlap=0):
        len_data += block.shape[0]
    # print(len_data)
    # print(data1.shape[0])
    # print(list_data)
    # print(data1 == list_data)
    # print(blocks.shape)
    # print(rms)
    # print(type(data1))
    pcm_path = r"./AudioPath/周杰伦 - 听妈妈的话.pcm"
    # 使用read读取pcm文件
    data2, sr = sf.read(pcm_path, samplerate=44100, format="RAW", subtype="PCM_16", channels=2, dtype="int16")
    # print(data2==data1)
    print(type(data1[0][0]))
    print(data2)
    print(data2[0][0])
    # sf.write(r'./AudioPath/stereo_file.wav', np.random.randn(10, 2), 44100, 'PCM_24')
    info_wav = sf.info(wav_path)
    info_pcm = sf.info(pcm_path)
    print(info_wav)
    print("*"*20)
    print(info_pcm)


if __name__ == "__main__":
    """
    https://python-soundfile.readthedocs.io/.
    The soundfile module can read and write sound files. File reading/writing is supported through libsndfile, 
    which is a free, cross-platform, open-source (LGPL) library for reading and writing many different sampled 
    sound file formats that runs on many platforms including Windows, OS X, and Unix. It is accessed through CFFI,
    which is a foreign function interface for Python calling C code. CFFI is supported for CPython 2.6+, 3.x
    and PyPy 2.0+. The soundfile module represents audio data as NumPy arrays.
    
    """
    soundfile_read()
