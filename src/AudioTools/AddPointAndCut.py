#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :AddPointAndCut.py
# @Time      :2024/6/2 17:35
# @Author    :pengweiaini123@163.com
from pydub import AudioSegment
from pydub.generators import Sine
import soundfile as sf


def create_signal():
    # 我们先创建一个特殊音频信号(例如脉冲信号)
    sample_rate = 44100
    duration = 5000  # milliseconds
    frequency = 440  # Hz
    sine_wave = Sine(frequency).to_audio_segment(duration=duration, volume=0)
    audio = sine_wave.set_frame_rate(sample_rate).set_channels(1)
    audio.export("./AudioPath/pulse_signal.wav", format="wav")
    pass


def cut_audio():
    # 找到音频中相同的信号，并将音频分割
    data, _ = sf.read("./AudioPath/pulse_signal.wav")
    print()
    pass


if __name__ == "__main__":
    # 创建脉冲信号
    # create_signal()
    # 读取脉冲和分割音频比较
    cut_audio()
    pass

