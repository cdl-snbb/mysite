from aip import AipSpeech


def voice2text(APP_ID, API_KEY, SECRET_KEY, file_path):
    """
    语音转换为文字
    :param APP_ID: 
    :param API_KEY: 
    :param SECRET_KEY: 
    :param file_path: 音频文件路径
    :return: 一个包含文字内容的列表
    """
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    ret = client.asr(get_data(file_path), 'pcm', 16000, {'dev_pid': 1536}, )
    return ret['result']


def get_data(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()
