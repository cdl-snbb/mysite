"""
机器人回答
"""
import requests
import json
# 图灵
from ..set import TULING_KEY
# 思知
from ..set import apiKey

# 图灵机器人
def answer(message):
    url = 'http://www.tuling123.com/openapi/api?key='+TULING_KEY+'&info='+message
    res = requests.get(url)
    res.encoding = 'utf-8'
    answer_message = json.loads(res.text)

    return answer_message


# 思知机器人API
def get_sizhi_response(msg):
    apiUrl = 'https://api.ownthink.com/bot'
    #apiUrl = 'https://www.ownthink.com/'
    data = {
        "spoken": msg,
        "appid": apiKey,
        "userid": 'user'  # 随便起的
    }
    # 必须是json
    headers = {'content-type': 'application/json'}

    try:
        req = requests.post(apiUrl, headers=headers, data=json.dumps(data))
        return req.json()
    except:
        return


# 处理思知机器人返回的json消息
def sizhi_msg(msg):
    # 设置一个默认回复。
    replyjson = get_sizhi_response(msg)

    if replyjson is None:
        return_msg = '我是个笨笨的机器人，我CPU好像挂了~_~!'
    elif replyjson['message'] == 'success':
        return_msg = replyjson['data']['info']['text'].replace('小思', '小思~').replace('思知机器人', '小思~')
        #print("思知机器人自动回复：" + return_msg)
    # a or b --》 如果a不为空就返回a，否则返回b
    else:
        return_msg = '我是个笨笨的机器人，我CPU好像挂了~_~!'
    return return_msg

