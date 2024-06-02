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
    # print(blocks.shape)
    print(rms)
    print(type(data1))
    pcm_path = r""


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
