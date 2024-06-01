# author : PengWei
# function : 
# time : 2023/2/21 22:57
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


def output_wave(speech_path, speech, sr):
    speech = speech/32768
    sf.write(speech_path, speech, 'PCM_16')


def output_pcm(output_pcm_path, speech):
    new_pcm = np.memmap(output_pcm_path, dtype='h', mode='w+', shape=speech.shape)
    new_pcm[:] = speech[:]
