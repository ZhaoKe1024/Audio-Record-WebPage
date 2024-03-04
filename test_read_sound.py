# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-03-04 23:12
from audio import AudioSegment


def test_read():
    sound_path = "D:/DATAS/UrbanSound8K/UrbanSound8K/audio/fold1/50901-0-1-1.wav"
    audio_seg = AudioSegment.from_file(sound_path)
    print(audio_seg)


if __name__ == '__main__':
    test_read()
