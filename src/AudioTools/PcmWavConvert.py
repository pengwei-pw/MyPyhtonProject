#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :PcmWavConvert.py
# @Time      :2024/11/15 15:10:53
# @Author    :PengWei

import os
import numpy as np
import soundfile as sf


PCM_ERROR_CODE_1 = 'empty pcm'
PCM_ERROR_CODE_2 = 'channel_number error'
PCM_OFFSET = 6


def load_wave(audio_path):
    audio, sr = sf.read(audio_path)
    audio = audio * 32768
    return audio, sr


def load_pcm(speech_path, channel_num):
    pcm_data = np.memmap(speech_path, dtype='h', mode='r')
    if len(pcm_data) == 0:
        return pcm_data, PCM_ERROR_CODE_1
    speech_length = len(pcm_data) // channel_num
    if (speech_length * channel_num) == len(pcm_data):
        pcm_data_final = pcm_data
    elif (speech_length * channel_num) == (len(pcm_data) - PCM_OFFSET):
        pcm_data_final = pcm_data[:(len(pcm_data) - PCM_OFFSET)]
    else:
        return pcm_data, PCM_ERROR_CODE_2
    speech_data = pcm_data_final.reshape((speech_length,channel_num))
    speech_data = speech_data
    return speech_data, 'success'


def output_wave(speech_path, speech, sr:int):
    speech = speech/32768
    sf.write(speech_path, speech, sr, 'PCM_16')


def output_pcm(output_pcm_path, speech):
    new_pcm = np.memmap(output_pcm_path, dtype='h', mode='w+', shape=speech.shape)
    new_pcm[:] = speech[:]


if __name__ == "__main__":
    pcm_path = r"D:\pw\唤醒识别\noise_cdx707\noise_r"
    wav_path = r"D:\pw\唤醒识别\noise_cdx707\noisewav"
    for file in os.listdir(pcm_path):
        pa = os.path.join(pcm_path, file)
        file_data, _ = load_pcm(pa, channel_num=8)
        wav_data = file_data[:, 0:2]
        output_wave(speech_path=pa.replace('.pcm', '.wav'), speech=wav_data, sr=16000)