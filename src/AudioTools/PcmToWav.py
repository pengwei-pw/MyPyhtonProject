# author : PengWei
# function : 
# time : 2023/2/20 20:16

import numpy as np
import wave


def pcm_convert_wav(pcm_path: str, wav_path: str):
    pcm_data = np.fromfile(pcm_path, dtype = np.uint16)
    with wave.open(wav_path, "wb") as wav_file:
        wav_file.setparams((1, 2, 16000, 0, "NONE", "NONE"))
        wav_file.writeframesraw(pcm_data)

