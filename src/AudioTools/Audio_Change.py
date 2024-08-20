#coding=gbk
# import glob
import os
import shutil

import numpy as np
from scipy.io import wavfile as wav
import wave
import librosa
import random
import soundfile as sf
import re
from pydub import AudioSegment

def pcm_wav(src_path, dst_path, channel=1, sampwidth=2, framerate=16000):
    file_list = os.listdir(src_path)
    channel = int(channel)
    sampwidth = int(sampwidth)
    framerate = int(framerate)
    for file in file_list:
        pcm_path = os.path.join(src_path, file)
        wav_path = os.path.join(dst_path, file[:-4] + '.wav')
        with open(pcm_path, 'rb') as pcm_file:
            pcm_data = pcm_file.read()
        with wave.open(wav_path, 'wb') as wav_file:
            wav_file.setparams((channel, sampwidth, framerate, 0, 'NONE', 'NONE'))
            wav_file.writeframesraw(pcm_data)

def change_sample(src_path):
    file_list = os.listdir(src_path)

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    # print(list)
    for i in file_list:
        path2 = os.path.join(src_path, i)
        path3 = os.path.join(dst_path, i)
        # path3 = path2.replace('mp3','wav')
        os.system(f'ffmpeg -y -i {path2} -ar 16000 {path3}')
        # os.system(f'ffmpeg -y -i {path2} -acodec pcm_s16le -ac 1 -ar 16000 {path3} -loglevel quiet')
        # print(f'ffmpeg -y -i {i}  -ac 1 -ar 16000  -b:a 512k  {i}')
            # ����Ƶ������תΪ˫����
            # ffmpeg -y -i demo.wav  -ac 2 demo.wav
            # ����Ƶ�����ʵ���Ϊ 44100Hz
            # ffmpeg -y -i demo.wav  -ar 44100  demo.wav
            # ��mp3��Ƶת��wav��Ƶ
            # ffmpeg -i 1.mp3 -acodec pcm_s16le -ac 1 -ar 16000 1.wav -loglevel quiet

def wav_pcm(src_path, dst_path):
    file_list = os.listdir(src_path)
    for file in file_list:
        if file.endswith('.wav'):
            wav_path = os.path.join(src_path, file)
            pcm_name = file[:-4] + '.pcm'
            pcm_path = os.path.join(dst_path, pcm_name)
            fs, signal = wav.read(wav_path)
            signal.tofile(pcm_path)

def mp3_wav(src_path, dst_path):
    file_list = os.listdir(src_path)

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    # print(list)
    for i in file_list:
        path2 = os.path.join(src_path, i)
        path3 = os.path.join(dst_path, i.replace('mp3','wav'))
        # path3 = path2.replace('mp3','wav')
        os.system(f'ffmpeg -y -i {path2} -acodec pcm_s16le -ac 1 -ar 16000 {path3} -loglevel quiet')

def mp3_to_wav(src_path, dst_path):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    # AudioSegment.converter = r'C:\07.Output\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe'
    # AudioSegment.ffprobe = r"C:\07.Output\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe"
    for filename in os.listdir(src_path):
        #ѭ������ԭʼmp3Ŀ¼�µ���Ƶ�ļ�
        if filename.endswith('.mp3'):
            file_path = os.path.join(src_path, filename)
            # print(os.path.splitext(filename)[0] + '.wav')
            sound = AudioSegment.from_mp3(file_path)
            ###ʹ��pydub����mp3��Ƶ
            ###�����µ�Ŀ��·�����ļ���
            dest_path = os.path.join(dst_path, os.path.splitext(filename)[0] + '.wav')
            # print(dest_path)
            ##����Ƶ���ݵ���Ϊwav��Ƶ�ļ�
            sound.export(dest_path, format="wav")

def audio_increase(src_path, dst_path):
    # Loop through all audio files in the input folder
    for file_name in os.listdir(src_path):
        if file_name.endswith(".wav"):  # Only work on WAV files
            # Load the audio file and apply a gain of 6 dB
            audio = AudioSegment.from_wav(os.path.join(src_path, file_name))
            louder_audio = audio + 6
            # 6��������ǿ��dbֵ
            output_file_name = file_name[:-4] + '_louder6.wav'
            louder_audio.export(os.path.join(dst_path, output_file_name), format="wav")

def merge_pcm(src_file, src_path):
    src_data = np.memmap(src_file, dtype='h', mode='r')
    src_data = src_data.reshape(-1, 1)
    file_list = os.listdir(src_path)
    root_path = os.path.abspath(os.path.dirname(src_path))
    dst_path = os.path.join(root_path, 'add')
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    for file in file_list:
        file_path = os.path.join(src_path, file)
        dst_file = os.path.join(dst_path, file)
        file_data = np.memmap(file_path, dtype='h', mode='r')
        file_data = src_data.reshape(-1, 1)
        dst_data = np.vstack((src_data, file_data))
        new_pcm = np.memmap(dst_file, dtype='h', mode='w+', shape=dst_data.shape)
        new_pcm[:] = dst_data[:]

def plus():
    sound1 = AudioSegment.from_file(r"C:\21.CX727 ICA\noise\noise-record-old\noise006.wav", format="wav")
    # sound2 = AudioSegment.from_file(r"C:\13.audio\CDX707-LV978\111-update\false-wakeup-test\ԭʼwav\quiet-46min.wav", format="wav")
    # sound3 = AudioSegment.from_file(r"C:\13.audio\CDX707-LV978\111-update\noise-real-wav\noise-chat002.wav", format="wav")
    # sound4 = AudioSegment.from_file(r"C:\13.audio\CDX707-LV978\111-update\noise-real-wav\noise-chat003.wav", format="wav")
    combined = sound1 + sound1 + sound1
    file_handle = combined.export(r"C:\21.CX727 ICA\noise\noise-record-old\noise006-use.wav", format="wav")

def combine_channels():
    audio1 = AudioSegment.from_wav(r'C:\21.CX727 ICA\noise\test\noise006-01.wav')
    audio2 = AudioSegment.from_wav(r'C:\21.CX727 ICA\noise\test\noise006-02.wav')
    audio3 = AudioSegment.from_wav(r'C:\21.CX727 ICA\noise\test\noise006-03.wav')
    audio4 = AudioSegment.from_wav(r'C:\21.CX727 ICA\noise\test\noise006-04.wav')
    audio5 = AudioSegment.from_wav(r'C:\21.CX727 ICA\noise\test\noise006-05.wav')
    audio6 = AudioSegment.from_wav(r'C:\21.CX727 ICA\noise\test\noise006-06.wav')
    audio7 = AudioSegment.from_wav(r'C:\21.CX727 ICA\noise\test\noise006-07.wav')
    output_final = AudioSegment.from_mono_audiosegments(audio1, audio2, audio3, audio4, audio5, audio6, audio7)
    output_final.export(r'C:\21.CX727 ICA\noise\test\111.wav', format="wav")

def audio_cut(src_path, dst_path):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    for file in os.listdir(src_path):
        file_path = os.path.join(src_path, file)
        sound = AudioSegment.from_file(file_path, format='wav')
        sound_cut = sound[53080:]
        # sound_cut_back = sound_cut[31000:]
        # sound_cut_final= sound_cut + sound_cut_back
        sound_cut.export(os.path.join(dst_path, file), format='wav')

def delete_channels(src_path, dst_path):
    # # ������phase4�ɼ���Ƶ����phase4�ɼ���Ƶ��7������
    # # 1��2����micԭʼ���ݡ�����&���ݡ�  3��4�����ý��ο��źš���&�ҡ�  5����TTS�ο��ź�  6��7��������micout���ݡ�����&���ݡ�
    for file_name in os.listdir(src_path):
        if file_name.endswith('.wav'):
            input_file = os.path.join(src_path, file_name)
            audio = AudioSegment.from_wav(input_file)
            ####micin��Ƶ���
            # channels_to_keep = [0, 1, 2, 3, 4]  # ����micin������Ҳ����ǰ��5������
            # new_channels = []
            # for i in range(audio.channels):
            #     if i in channels_to_keep:
            #         new_channels.append(audio.split_to_mono()[i])
            # output, output1, output2, output3, output4 = new_channels[0], new_channels[1], new_channels[2], new_channels[3], new_channels[4]
            # output_final = AudioSegment.from_mono_audiosegments(output, output1, output2, output3, output4)
            ####micout��Ƶ���
            channels_to_keep = [5, 6]  # ����micout����Ҳ���ǵ�6�͵�7����
            new_channels = []
            for i in range(audio.channels):
                if i in channels_to_keep:
                    new_channels.append(audio.split_to_mono()[i])
            output, output1 = new_channels[0], new_channels[1]
            output_final = AudioSegment.from_mono_audiosegments(output, output1)
            ######################
            output_file = os.path.join(dst_path, file_name)
            output_final.export(output_file, format="wav")


if __name__ == '__main__':
    src_path = r'C:\16.Phase 4\2.CD764ICA8155\Noise-PV360-1221'
    # src_file = r'C:\13.audio\plus\wav'
    dst_path = r'C:\16.Phase 4\2.CD764ICA8155\micin'
    # # # # mp3��Ƶת��wav��ʽ # # # #
    # mp3_wav(src_path, dst_path)
    # mp3_to_wav(src_path, dst_path)
    # merge_pcm(src_file, src_path)

    # plus()      # # # # ƴ����Ƶ # # # #
    # combine_channels()   # # # # �����������Ƶ���ϳ�һ�������� # # # #
    # # # # ��Ƶ����ǰ���¼�Ƶ�������� # # # #
    # audio_cut(src_path, dst_path)

    # # # # pcm��Ƶת��wav��ʽ # # # #
    #     # pcm_wav(src_path, dst_path, channel=1, sampwidth=2, framerate=16000)

    # # # # �ı���Ƶ���� # # # #
    # change_sample(src_path)

    # # # # wavת��pcm��Ƶ��ʽ # # # #
    # wav_pcm(src_path, dst_path)

    # # # # wav������ǿ # # # #
    # audio_increase(src_path, dst_path)

    # # # # aup3��ʽת����wav��ʽ # # # #
    # aup3_to_wav(src_path, dst_path)

    # # # # �ɼ���7��������Ƶ��ֻ����micin/micout��Ƶ
    delete_channels(src_path, dst_path)
