"""
声纹验证
"""
import os
import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
import warnings
from pydub import AudioSegment
from sklearn import preprocessing
import python_speech_features as mfcc


def trans_mp3_to_wav(filepath):
    """
    把mp3格式音频转化为wav格式
    :param filepath: 文件路径
    :return: 
    """
    Audio = AudioSegment.from_mp3(filepath)
    filename = filepath.split(".mp3")[0]

    sound = Audio.set_frame_rate(16000)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)

    sound.export(filename + '.wav', format='wav')
    sr, audio = read(filename + '.wav')
    return sr, audio


def check_voice(speaker_paths, models_path):
    """
    声纹验证
    :return: 1:验证通过，0:验证不通过
    """
    check = False
    warnings.filterwarnings("ignore")

    gmm_files = [os.path.join(models_path, fname) for fname in
                 os.listdir(models_path) if fname.endswith('.gmm')]

    models = [cPickle.load(open(fname, 'rb')) for fname in gmm_files]

    file_paths = os.listdir(speaker_paths)
    for path in file_paths:
        # 格式转化
        if (speaker_paths + path).endswith(".mp3"):
            sr, audio = trans_mp3_to_wav(speaker_paths + path)
        else:
            sr, audio = read(speaker_paths + path)
        #提取声学特征
        vector = extract_features(audio, sr)

        log_likelihood = np.zeros(len(models))
        #比对声学模型，并打分
        for i in range(len(models)):
            gmm = models[i]
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()
            if log_likelihood[i] > -23:
                # 验证通过
                check = True
                break
        if check:
            return 1
        else:
            # 验证失败
            return 0


def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix"""

    rows, cols = array.shape
    deltas = np.zeros((rows, 20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i - j < 0:
                first = 0
            else:
                first = i - j
            if i + j > rows - 1:
                second = rows - 1
            else:
                second = i + j
            index.append((second, first))
            j += 1
        deltas[i] = (array[index[0][0]] - array[index[0][1]] + (2 * (array[index[1][0]] - array[index[1][1]]))) / 10
    return deltas


def extract_features(audio, rate):
    """extract 20 dim mfcc features from an audio, performs CMS and combines
    delta to make it 40 dim feature vector"""

    mfcc_feat = mfcc.mfcc(audio, rate, 0.025, 0.01, 20, appendEnergy=True)

    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)
    combined = np.hstack((mfcc_feat, delta))
    return combined
