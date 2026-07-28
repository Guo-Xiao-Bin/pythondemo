import base64
import hashlib
import hmac
import time
import urllib
import requests


def generate_sign():
    """
    签名计算
    :return:
    """
    timestamp = str(round(time.time() * 1000))
    # 钉钉机器人生成的密钥
    secret = 'SECe5e586db17c36f7bfba9e1db5856a0ae0f691cdbba4d17883055d649345b7943'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_dingding_msg(content, at_all=True):
    """
    向钉钉群机器人推送结果
    :param content: 推送内容
    :param at_all: @钉钉群里全部人，默认为True
    :return:
    """
    timestamp_sign = generate_sign()
    # 首先要拿到钉钉机器人的webhook地址+timestamp+密钥
    url = f'https://oapi.dingtalk.com/robot/send?access_token=2089c9018a1c4745144895f6b8fbe91e3e6153f8b9ac73d9e081d8d2df35560d&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    req_data = {
        'msgtype': 'text',
        'text': {
            'content': content
        },
        'at': {
            'isAtAll': at_all
        }
    }
    res = requests.post(url=url, json=req_data, headers=headers)
    return res.text


if __name__ == '__main__':
    content = """
    各位好，本次电商项目的测试报告执行结果如下：
    测试用例总共：110
    通过：100
    失败：3
    跳过：4
    异常：7
    点击查看测试报告：www.baidu.com
    """
    print(send_dingding_msg(content))
