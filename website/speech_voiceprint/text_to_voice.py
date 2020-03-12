from aip import AipSpeech


def text2voice(APP_ID, API_KEY, SECRET_KEY, text, file_path):
    """
    文字转换为语音
    :param APP_ID: 
    :param API_KEY: 
    :param SECRET_KEY: 
    :param text: 要转换的文字内容
    :param file_path: 音频文件存放的路径
    :return: 
    """
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
        'per': 4,
    })

    if not isinstance(result, dict):
        with open(file_path, 'wb') as f:
            f.write(result)

