import miraicle
import requests
import random
import json

def get_yiyan():
    response = requests.get("http://v1.hitokoto.cn")
    response = json.loads(response.text)
    yiyan = "『"+response["hitokoto"]+"』-「"+response["from"]+"」"
    return yiyan

def get_dmoe():
    while True:
        seq = ["http://www.dmoe.cc/random.php", "http://api.mtyqx.cn/tapi/random.php", "http://api.mtyqx.cn/api/random.php"]
        dmoe = random.choice(seq)
        response = requests.get(dmoe, params={'return': 'json'})
        if response.ok:
            return response.json()['imgurl']

@miraicle.Mirai.receiver('NudgeEvent')
def nudge_handler(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    dmoe = get_dmoe()
    yiyan = get_yiyan()
    bot.send_group_msg(group=msg['subject']['id'], msg=[miraicle.At(qq=msg['fromId']),
                                                        miraicle.Plain("\n"+yiyan),
                                                        miraicle.Image.from_url(dmoe)])
    '''
    a   动画
    b	漫画
    c  	游戏
    d	文学
    e	原创
    f	来自网络
    g	其他
    h	影视
    i	诗词
    j	网易云
    k	哲学
    l	抖机灵
    其他	作为 动画 类型处理
    '''