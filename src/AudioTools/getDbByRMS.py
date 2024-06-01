# author : PengWei
# function :
# time : 2023/2/21 22:57

import numpy as np
import soundfile as sf
import librosa
import librosa.display


PCM_ERROR_CODE_1 = 'empty pcm'
PCM_ERROR_CODE_2 = 'channel_number error'
PCM_OFFSET = 6


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


def calculate_rms(x, sr=44100, frame_length=0.025, hop_length=0.0125, center=True, pad_mode='reflect', begin_index=1,
                  end_index=-1):
    """

    :param x:
    :param sr:
    :param frame_length:
    :param hop_length:
    :param center:
    :param pad_mode:
    :param begin_index:
    :param end_index:
    :return:
    """
    frame_samples = int(sr * frame_length)
    hop_samples = int(sr * hop_length)
    begin_index = begin_index - 1
    if end_index == -1:
        end_index = len(x)
    y_temp = x[begin_index:end_index]
    if len(y_temp) < frame_samples:
        y = np.zeros(frame_samples)
    else:
        y = np.zeros(len(y_temp))
    print(y_temp.shape)
    y[0:len(y_temp)] = y_temp[:, 0]
    if center is True:
        print(int(frame_length//2))
        y = np.pad(y, int(frame_length//2), mode=pad_mode)
    y = librosa.util.frame(y, frame_length=frame_samples, hop_length=hop_samples)
    power = np.mean(np.abs(y) ** 2, axis=0, keepdims=True)
    power_result = np.array([])
    for i in range(power.shape[1]):
        if int(power[0, i]) == 0:
            power[0, i] = 1
        power_result = np.append(power_result, power[0, i])
    power_result = 20 * np.log10(np.sqrt(power_result))
    return power_result


def load_wave(audio_path):
    audio, sr = sf.read(audio_path)
    audio = audio * 32768
    return audio, sr


def get_RMSInfo(x):
    x_speech_db_sequence = calculate_rms(x)
    x_speech_db_mean = np.mean(x_speech_db_sequence)
    return x_speech_db_mean


def output_pcm(output_pcm_path, speech):
    new_pcm = np.memmap(output_pcm_path, dtype='h', mode='w+', shape=speech.shape)
    new_pcm[:] = speech[:]


def cc():
    in_audio = r"D:\PythonEnvironment\PyCharmWorkSpace\PythonAudio\src\musicAudio\周杰伦 - 听妈妈的话.wav"
    # ipd.Audio(in_audio)
    data, _ = load_wave(in_audio)
    data_1 = data[:, np.array([0])]
    print(data_1)
    dass, _ = librosa.effects.trim(data_1.reshape(len(data_1)), top_db=100)
    print(dass)
    output_pcm(r"D:\PythonEnvironment\PyCharmWorkSpace\PythonAudio\src\musicAudio\jjjj.pcm", dass)

if "__main__" == __name__:
    in_audio = r"D:\PythonEnvironment\PyCharmWorkSpace\PythonAudio\src\musicAudio\周杰伦 - 听妈妈的话.wav"
    out_audio = r"D:\PythonEnvironment\PyCharmWorkSpace\PythonAudio\src\musicAudio\周杰伦 - 听妈妈的话.pcm"
    data, _ = load_wave(in_audio)
    data_1 = data[:, np.array([0])]
    print(data_1)
    print(get_RMSInfo(data_1))
    output_pcm(out_audio, data)
    # cc()

